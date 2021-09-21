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
# Last page
driver.get(link.format(1))
pageElem = driver.find_element_by_class_name('pagination').find_elements_by_tag_name('a')
lastPage = pageElem[len(pageElem) - 1].text
for idx in range(1, int(lastPage) + 2):
	try:
		# Current page
		current_page = idx
		driver.get(link.format(current_page))
		# element for column names - 1
		colNamesfirst = driver.find_element_by_tag_name('thead').find_elements_by_tag_name('th')
		# Column names - 1
		listColsFirst = []
		for elem in colNamesfirst:
			col_raw = elem.text
			listColsFirst.append(col_raw)
		# Result
		listColsFirst = [i.replace('\n', ' ') for i in listColsFirst]
		# element for column names - 2
		colNamesElem = driver.find_element_by_tag_name('tbody').find_elements_by_tag_name('tbody')[0]
		colNamesSecond = colNamesElem.find_elements_by_tag_name('td')
		# Column names
		listColsSecond = []
		for elem in colNamesSecond[0::2]:
			col_raw = elem.text
			listColsSecond.append(col_raw)
		# Result
		listColsSecond = [i.replace('\n', ' ') for i in listColsSecond]
		# Data collections
		dataCollection = driver.find_element_by_tag_name('tbody')
		# Prepare blank dictionary for columns
		first_column = {'Data ID': [], 'Penyedia': [], 'NPWP': [], 'Alamat': [], 'Alamat Lengkap': []}
		# Length of rows in page
		lengthRows = dataCollection.find_elements_by_tag_name('h5')
		for row in range(len(lengthRows)):
			# Get data
			valVendor = dataCollection.find_elements_by_tag_name('h5')[row].text
			valNPWP = dataCollection.find_elements_by_class_name('npwp')[row].text
			valAddessGen = dataCollection.find_elements_by_class_name('header')[row].text
			valAddessDesc = dataCollection.find_elements_by_class_name('description')[row].text
			valId = dataCollection.find_elements_by_tag_name('a')[row].get_attribute('data-id')
			# Key-value
			dict_val = {'data_id': valId, 'vendor': valVendor, 'npwp': valNPWP, 'address_gen': valAddessGen, 'address_desc': valAddessDesc}
			# Parse into list
			for col in range(len(dict_val.keys())):
				value = dict_val[list(dict_val.keys())[col]]
				first_column[list(first_column.keys())[col]].append(value)
		# Second column
		second_column = {key: [] for key in listColsSecond}
		for elem in dataCollection.find_elements_by_tag_name('tbody'):
			elemValues = elem.find_elements_by_tag_name('tr')
			for col in range(len(elemValues)):
				value = elemValues[col].text
				# Append values
				second_column[list(second_column.keys())[col]].append(value)
		# Dictionary for data
		dict_full = dict_full = {
			current_page: {
				**first_column,
				**second_column
			}
		}
		df_json = {**df_json, **dict_full}
		# Logs
		print("Hey, we're now in link {}".format(idx))
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