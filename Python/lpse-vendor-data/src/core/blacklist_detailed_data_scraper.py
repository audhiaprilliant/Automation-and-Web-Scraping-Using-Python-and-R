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
    'Aktif': 'https://inaproc.id/daftar-hitam?page={}#{}',
    'Tidak Aktif': 'https://inaproc.id/daftar-hitam/non-aktif?page={}#{}'
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
	current_page = key
	idDataList = file_json[key]['Data ID']
	for ids in idDataList:
		try:
			# Access to url
			driver.get(link.format(current_page, ids))
			time.sleep(3)
			# Data collection
			dataCollection = driver.find_element_by_id('injunctions').find_element_by_tag_name('tbody')
			# Prepare blank dictionary for columns
			third_column = {
				'Judul Pelanggaran': [],
				'Isi Pelanggaran': [],
				'Nama KLPD': [],
				'Nama Satker': [],
				'Masa Berlaku Sanksi': [],
			    'Tanggal Penayangan': []
			}
			# Length of rows in page
			lengthRows = dataCollection.find_elements_by_class_name('item')
			for row in range(len(lengthRows)):
				# Get data
				valVioHeader = dataCollection.find_elements_by_class_name('header')[row].text
				valVioContent = dataCollection.find_elements_by_class_name('description')[row].text
				valList = []
				elemVal = dataCollection.find_elements_by_tag_name('tbody')[row].find_elements_by_tag_name('td')[1::2]
				for elem in elemVal:
					elemValSub = elem.text
					valList.append(elemValSub)
				# Key-value
				dict_val = {
					'vio_header': valVioHeader,
					'vio_content': valVioContent,
					'sub_institution': valList[0],
					'sub_name': valList[1],
					'sub_expire': valList[2],
					'sub_show': valList[3]
				}
				# Parse into list
				for col in range(len(dict_val.keys())):
					value = dict_val[list(dict_val.keys())[col]]
					third_column[list(third_column.keys())[col]].append(value)
			# Number of law
			lawList = []
			for element in dataCollection.find_elements_by_tag_name('td'):
				string = element.text
				try:
					value = re.match(pattern = 'No+ : \S+\d+$', string = string)[0]
				except:
					continue
				# Append to list
				lawList.append(value)
			# Add number of law into dictionary
			third_column['SK Penetapan'] = lawList
			# Dictionary for data
			current_data = ids
			dict_full = {
				current_data: third_column
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