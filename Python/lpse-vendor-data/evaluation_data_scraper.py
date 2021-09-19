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
			# Link of evaluation
			linkEvaluation = dictLink['Hasil Evaluasi']
			# Access to evaluation's link
			driver.get(linkEvaluation)
			# Get the column elements
			evaluationSummaryData = driver.find_element_by_class_name('content')
			# element for column names
			colNames = evaluationSummaryData.find_element_by_tag_name('thead').find_elements_by_tag_name('th')
			# Column names
			listCols = []
			for elem in colNames:
				col_raw = elem.text
				listCols.append(col_raw)
			# Result
			listCols = [i.replace('\n', ' ') for i in listCols]
			# Data collections
			dataCollection = evaluationSummaryData.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
			# Dictionary with blank list
			dict_init = {key: [] for key in listCols}
			# Get a data from table
			for row in dataCollection:
				elemValues = []
				for elem in row.find_elements_by_css_selector('*'):
					elemChoosen = elem.tag_name
					if elemChoosen in ['i', 'img']:
						continue
					else:
						elemValues.append(elem)

				for col in range(len(elemValues)):
					try:
						value = elemValues[col].text
						if value == '':
							try:
								val = elemValues[col].find_element_by_tag_name('img').get_attribute('src')
								if val == 'https://lpse.lkpp.go.id/eproc4/public/images/star.gif':
									value = 'Star'
								else:
									value = None
							except:
								try:
									val = elemValues[col].find_element_by_tag_name('i').get_attribute('class')
									if val == 'fa fa-check':
										value = 'Checklist'
									elif val == 'fa fa-close':
										value = 'Blacklist'
									elif val == 'fa fa-minus':
										value = 'Strip'
								except:
									value = None
					except:
						value = None
					# Append values
					dict_init[list(dict_init.keys())[col]].append(value)
			# Add tender's code as identifier
			code_tender = re.findall(pattern = 'https://lpse.lkpp.go.id/eproc4/evaluasi/(.*)/hasil', string = linkEvaluation)[0]
			dict_full = {
				code_tender: dict_init
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
filename = 'data/raw/LPSE Evaluation Data - Page {start} to {end} - {now}.json'.format(
	start = start_page,
	end = final_page,
	now = now
)
with open(filename, 'w') as outfile:
	outfile.write(json_object)