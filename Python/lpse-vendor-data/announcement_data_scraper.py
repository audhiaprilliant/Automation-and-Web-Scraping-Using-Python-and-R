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
			# Link of announcement
			linkAnnounce = dictLink['Pengumuman']
			# Access to evaluation's link
			driver.get(linkAnnounce)
			# Get column names
			announceSummaryData = driver.find_element_by_class_name('content')
			dataCollection = announceSummaryData.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
			# Data collections
			dataCollection = announceSummaryData.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
			# Get column names
			dictColNamesFirst = {}
			for idx in range(len(dataCollection)):
				try:
					colNames = dataCollection[idx].find_elements_by_tag_name('th')[0].text
				except:
					continue
				dictColNamesFirst.update({str(idx): colNames})
			# Get values
			dictValuesFirst = {}
			for idx in range(len(dataCollection)):
				try:
					value = dataCollection[idx].find_elements_by_tag_name('td')[0].text
				except:
					continue
				dictValuesFirst.update({str(idx): value})
			# Concate two dictionaries
			dictColVal = defaultdict(list)
			for d in (dictColNamesFirst, dictValuesFirst):
				for key, value in d.items():
					dictColVal[key].append(value)
			# Final dictionary
			dict_full = {}
			for key in dictColVal.keys():
				if len(dictColVal[key]) == 2 and dictColVal[key][0] != '' and dictColVal[key][0] != '':
					dict_full.update({dictColVal[key][0]: dictColVal[key][1]})
			# Add tender's code as identifier
			code_tender = dict_full['Kode Tender']
			dict_full = {
				code_tender: dict_full
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
filename = 'data/raw/LPSE Announcement Data - Page {start} to {end} - {now}.json'.format(
	start = start_page,
	end = final_page,
	now = now
)
with open(filename, 'w') as outfile:
	outfile.write(json_object)