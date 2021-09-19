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
start_page = sys.argv[2]
end_page = sys.argv[3]

# OPEN JSON FILE
with open(data_location) as file:
	file_json = json.load(file)

# FILTER PAGES
length_keys = len(file_json.keys())
# Start page
if start_page == 'start':
	start_page = 0
else:
	start_page = start_page
# Final page
if end_page == 'end':
	final_page = length_keys
else:
	final_page = end_page
# Filter data
keys = list(map(str, range(int(start_page), int(final_page))))
file_json_filter = {key: file_json[key] for key in keys}

# OPEN CHROME DRIVER
DRIVER_PATH = 'bin/chromedriver'
driver = webdriver.Chrome(executable_path = DRIVER_PATH)

# GET THE DATA
df_json = {}
link_stat = 0
for key in file_json_filter.keys():
	links = file_json_filter[key]['Link Paket']
	for link in links:
		try:
			# Access to main link
			driver.get(link)
			# Get links
			list_links = driver.find_elements_by_class_name('nav-link')
			listLink = [link_val.get_attribute('href') for link_val in list_links]
			# List of link
			navName = ['Pengumuman', 'Peserta', 'Hasil Evaluasi', 'Pemenang', 'Pemenang Berkontrak']
			dictLink = dict(zip(navName, listLink))
			# Link of winners
			linkWinner = dictLink['Pemenang']
			# Access to winner's link
			driver.get(linkWinner)
			# Get the column elements
			winnerSummaryData = driver.find_element_by_class_name('content')
			# Data collections - 1
			dataCollectionFirst = winnerSummaryData.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
			# Get column names - 1
			listColNamesFirst = []
			for idx in range(len(dataCollectionFirst) - 3):
				colNames = dataCollectionFirst[idx].find_elements_by_tag_name('th')[0].text
				listColNamesFirst.append(colNames)
			# Get values - 1
			listValuesFirst = []
			for idx in range(len(dataCollectionFirst) - 3):
				value = dataCollectionFirst[idx].find_elements_by_tag_name('td')[0].text
				listValuesFirst.append(value)
			# Data collections - 2
			dataCollectionSecond = winnerSummaryData.find_element_by_tag_name('tbody').find_element_by_tag_name('tbody')
			# Get column names - 2
			listColNamesSecond = []
			dataCollectionSecondCol = dataCollectionSecond.find_elements_by_tag_name('th')
			for elem in dataCollectionSecondCol:
				colNames = elem.text
				listColNamesSecond.append(colNames)
			# Get values - 2
			listValuesSecond = []
			dataCollectionSecondVal = dataCollectionSecond.find_elements_by_tag_name('td')
			for val in dataCollectionSecondVal:
				value = val.text
				listValuesSecond.append(value)
			# Column names - full
			listColNamesFull = listColNamesFirst + listColNamesSecond
			# Values - full
			listValuesFull = listValuesFirst + listValuesSecond
			# Add tender's code as identifier
			code_tender = re.findall(pattern = 'https://lpse.lkpp.go.id/eproc4/evaluasi/(.*)/pemenang', string = linkWinner)[0]
			dict_full = {
				code_tender: dict(zip(
					listColNamesFull,
					listValuesFull
					)
				)
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
filename = 'data/raw/LPSE Winner Data - Page {start} to {end} - {now}.json'.format(
	start = start_page,
	end = final_page,
	now = now
)
with open(filename, 'w') as outfile:
	outfile.write(json_object)