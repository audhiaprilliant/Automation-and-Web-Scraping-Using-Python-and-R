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
data_type = sys.argv[1]

# FILTER PAGES
# Main link
main_link = {
    'Aktif': 'https://inaproc.id/daftar-hitam?page={}',
    'Tidak Aktif': 'https://inaproc.id/daftar-hitam/non-aktif?page={}'
}
# Filter
link = main_link['Aktif']
if data_type == 'AKTIF':
	link = main_link['Aktif']
elif data_type == 'TIDAK AKTIF':
	link = main_link['Tidak Aktif']

# OPEN CHROME DRIVER
DRIVER_PATH = 'bin/chromedriver'
driver = webdriver.Chrome(executable_path = DRIVER_PATH)

# GET THE DATA
df_json = {}
link_stat = 0
# Last page
driver.get(link.format(1))
pageElem = driver.find_element_by_class_name('pagination').find_elements_by_tag_name('a')
lastPage = pageElem[len(pageElem) - 1].text
for idx in range(1, int(lastPage) + 2):
	try:
		# Current page
		current_page = idx
		driver.get(link.format(current_page))
		# Data collections
		dataCollection = driver.find_element_by_tag_name('tbody')
		# Prepare blank dictionary for full data set
		dict_init = {}
		# Length of rows in page
		lengthRows = dataCollection.find_elements_by_tag_name('h5')
		for row in range(len(lengthRows)):
			# Prepare blank dictionary for columns
			# Get data
			valVendor = dataCollection.find_elements_by_tag_name('h5')[row].text
			valNPWP = dataCollection.find_elements_by_class_name('npwp')[row].text
			valAddessGen = dataCollection.find_elements_by_class_name('header')[row].text
			valAddessDesc = dataCollection.find_elements_by_class_name('description')[row].text
			valId = dataCollection.find_elements_by_tag_name('a')[row].get_attribute('data-id')
			# Key-value for first column
			dict_val_first = {
				'Data ID': valId,
				'Penyedia': valVendor,
				'NPWP': valNPWP,
				'Alamat': valAddessGen,
				'Alamat Lengkap': valAddessDesc
			}
			# Key-value for second column
			colNamesElem = dataCollection.find_elements_by_tag_name('tbody')[row]
			colNamesSecond = colNamesElem.find_elements_by_tag_name('td')
			# Column names
			listColsSecond = []
			for elem in colNamesSecond[0::2]:
				col_raw = elem.text
				listColsSecond.append(col_raw)
			listColsSecond = [i.replace('\n', ' ') for i in listColsSecond]
			# Get the value
			valSecondColumn = []
			elemValues = colNamesElem.find_elements_by_tag_name('tr')
			for col in range(len(elemValues)):
				value = elemValues[col].text
				valSecondColumn.append(value)
			# Append between two columns
			data_row = {
				**dict_val_first, 
				**dict(zip(
					listColsSecond,
					valSecondColumn
					)
				)
			}
			data_row['Halaman'] = idx
			# Dictionary for data
			dict_init = {**dict_init, **{
				valId: data_row
				}
			}
			df_json = {**df_json, **dict_init}
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
filename = 'data/raw/LPSE Blacklist Aktif Data - {now}.json'.format(now = now)
if data_type == 'AKTIF':
	filename = 'data/raw/LPSE Blacklist Aktif Data - {now}.json'.format(now = now)
elif data_type == 'TIDAK AKTIF':
	filename = 'data/raw/LPSE Blacklist Tidak Aktif Data - {now}.json'.format(now = now)
# Save file
with open(filename, 'w') as outfile:
	outfile.write(json_object)