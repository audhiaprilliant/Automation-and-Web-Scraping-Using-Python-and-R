# IMPORT MODULES
# Web scraping
from selenium import webdriver
# Data manipulation
import pandas as pd
from bs4 import BeautifulSoup
# Dropdown selector
from selenium.webdriver.support.ui import Select
# JSON settings
import json
# Date and time settings
from datetime import datetime
import time
# Argument settings
import sys
# Dictionary setting
from collections import defaultdict
# Regular expression
import re

# ARGUMENTS
data_location = sys.argv[1]
data_type = sys.argv[2]

# FILTER
# FILTER PAGES
# Main link
main_link = {
    'Aktif': 'https://inaproc.id/daftar-hitam?page={page}#{id}',
    'Tidak Aktif': 'https://inaproc.id/daftar-hitam/non-aktif?page={page}#{id}'
}
# Filter
link = main_link['Aktif']
if data_type == 'AKTIF':
	link = main_link['Aktif']
elif data_type == 'TIDAK AKTIF':
	link = main_link['Tidak Aktif']

# OPEN JSON FILE
with open(data_location) as file:
	file_json = json.load(file)

# OPEN CHROME DRIVER
DRIVER_PATH = 'bin/chromedriver'
driver = webdriver.Chrome(executable_path = DRIVER_PATH)

# GET THE DATA
df_json = {}
link_stat = 0
for key in file_json.keys():
	current_page = file_json[key]['Halaman']
	try:
		# Access to url
		driver.get(link.format(page = current_page, id = key))
		time.sleep(3)
		# Data collection
		dataCollection = driver.find_element_by_id('injunctions').find_element_by_tag_name('tbody')
		# Prepare blank dictionary for full data set
		dict_init = {}
		# Length of rows in page
		lenMax = dataCollection.find_elements_by_tag_name('td')
		lengthRows = dataCollection.find_elements_by_class_name('item')
		indexFinal = int(len(lenMax) / len(lengthRows))

		# Number of law
		lawList = []
		for elem in dataCollection.find_elements_by_tag_name('td')[0::int(indexFinal)]:
			string = elem.text
			lawList.append(string)

		for row in range(len(lengthRows)):
			# Get data for first column
			valVioHeader = dataCollection.find_elements_by_class_name('header')[row].text
			valVioContent = dataCollection.find_elements_by_class_name('description')[row].text
			# Key-value for first column
			dict_val_first = {
				'Judul Pelanggaran': valVioHeader,
				'Isi Pelanggaran': valVioContent,
				'SK Penetapan': lawList[row]
			}
			# Get data for second column
			elemDeep = dataCollection.find_elements_by_tag_name('tbody')[row].find_elements_by_tag_name('td')
			colList, valList = [], []
			elemCol, elemVal = elemDeep[0::2], elemDeep[1::2]
			for col, val in zip(elemCol, elemVal):
				elemColSub, elemValSub = col.text, val.text
				colList.append(elemColSub)
				valList.append(elemValSub)
		    
			# Append between two columns
			data_row = {**dict_val_first, **dict(zip(colList, valList))}
			# Append the dictionary
			dict_init = {**dict_init, **{
					row: data_row
				}
			}
		# Dictionary for data
		dict_full = {
			key: dict_init
		}
		df_json = {**df_json, **dict_full}
		# Logs
		print("Hey, we're now in link {}".format(link_stat))
		link_stat += 1
	except:
		continue

# SAVE DATA INTO JSON FILE
# Serialize json 
json_object = json.dumps(df_json, indent = 4)
# Write to JSON
now = datetime.today().strftime('%y-%m-%d %H-%M-%S')
# Filter
filename = 'data/raw/LPSE Blacklist Detailed Aktif Data - {now}.json'.format(now = now)
if data_type == 'AKTIF':
	filename = 'data/raw/LPSE Blacklist Detailed Aktif Data - {now}.json'.format(now = now)
elif data_type == 'TIDAK AKTIF':
	filename = 'data/raw/LPSE Blacklist Detailed Tidak Aktif Data - {now}.json'.format(now = now)
# Save file
with open(filename, 'w') as outfile:
	outfile.write(json_object)