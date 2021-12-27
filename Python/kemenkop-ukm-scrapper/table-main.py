#!/usr/bin/env python
# coding: utf-8
# author: audhiaprilliant

# Module for web scraping
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
# Module for data manipulation
import pandas as pd
# Module for passing variable
import sys
# Module for file management
from pathlib import Path
import os
# Module for monitoring
import time
from src.tools import monitor as monitor
# Module for parsing JSON
import json

# Local directory for running the script
root_path = os.getcwd()
# Configuration of Chromedriver and BPS site
DRIVER_PATH = root_path + '/bin/chromedriver'
DATA_PATH = root_path + '/data/raw'
# Configuration for headless Selenium
options = Options()
options.add_argument('--headless')

# Main program
if __name__ == '__main__':
	# 1 Load the Chromedriver and get the url
	driver = webdriver.Chrome(executable_path = DRIVER_PATH)
	driver.get('http://nik.depkop.go.id/')
	time.sleep(2)

	# 2 Get main dropdown
	# Get the dropdown object
	dropdownMain = driver.find_element_by_id('MainContent_DropDownList1')
	# Select the dropdown object
	selectorMain = Select(dropdownMain)
	# List of dropdown list
	listDropdownMain = []
	# Get elements in dropdown
	optionsMain = selectorMain.options
	for index in range(len(optionsMain)):
		listDropdownMain.append(optionsMain[index].text)

	# Monitoring - provinces
	monitor.printProgressBar(0, len(listDropdownMain), prefix = 'Progress:', suffix = 'Complete', length = 50)

	# 3 Loop the main dropdown
	for indexProv, provElem in enumerate(listDropdownMain):
		# Select the province
		selectorMain.select_by_visible_text(provElem)

		# Create the folder
		provincePath = DATA_PATH + '/' + provElem.replace('/', '_')
		Path(provincePath).mkdir(parents = True, exist_ok = True)
		
		# 4 Get sub-main dropdown
		# Get the dropdown object
		dropdownSubmain = driver.find_element_by_id('MainContent_DropDownList2')
		# Select the dropdown object
		selectorSubmain = Select(dropdownSubmain)
		# List of dropdown list
		listDropdownSubmain = []
		# Get elements in dropdown
		optionsSubmain = selectorSubmain.options
		for index in range(len(optionsSubmain)):
			listDropdownSubmain.append(optionsSubmain[index].text)
		
		# 5 Select the one element in dropdown
		for districtElem in listDropdownSubmain:
			# Data in JSON
			df_json = {}

			# Select the district
			selectorSubmain.select_by_visible_text(districtElem)

			# 6 Get the column names
			# Get the table object
			tableObj = driver.find_element_by_id('MainContent_GridView1')
			# Object for column names
			colNames = tableObj.find_elements_by_tag_name('tr')[2].find_elements_by_tag_name('th')
			# Column names
			listCols = []
			# Get the column names
			for elem in colNames:
				col_raw = elem.text
				listCols.append(col_raw)
			
			# Column names
			listCols = [i.replace('\n', ' ') for i in listCols]
			# Rename the first element
			listCols[0] = 'Links'
			# Dictionary with blank list
			dict_init = {key: [] for key in listCols}

			# 7 Pagination
			pageCount = 1
			while True:
				# Increase pageCount value on each iteration on +1
				pageCount += 1

				# Get the table object
				tableObj = driver.find_element_by_id('MainContent_GridView1')

				# Data collections
				dataCollection = tableObj.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')

				# Filter the data
				dataColFilter = dataCollection[3:len(dataCollection) - 3]

				# Get the data
				for idx, elem in enumerate(dataColFilter):
				    # Get values with href
				    elemHref = elem.find_element_by_tag_name('a')
				    href = elemHref.get_attribute('href')
				    # Append values
				    dict_init[list(dict_init.keys())[0]].append(href)
				    
				    # Get values without href
				    elemValues = elem.find_elements_by_tag_name('td')
				    for col in range(1, len(elemValues)):
				        value = elemValues[col].text
				        # Append values
				        dict_init[list(dict_init.keys())[col]].append(value)

				try:
					# Clicking on "2" on pagination on first iteration, "3" on second...
					driver.find_element_by_link_text(str(pageCount)).click()
				except NoSuchElementException:
					# Stop loop if no more page available
					break

				# 8 Concate the data
				df_json = {**df_json, **dict_init}

				# 9 Create a folder
				districtPath = provincePath + '/' + districtElem.replace('/', '_')
				Path(districtPath).mkdir(parents = True, exist_ok = True)

				# 10 Serialize JSON
				json_object = json.dumps(df_json, indent = 4)
				
				# 11 Write to JSON
				filename = districtPath + '/{dist} - District.json'.format(dist = districtElem)
				with open(filename, 'w') as outfile:
					outfile.write(json_object)

		# Monitoring - provinces
		time.sleep(0.1)
		monitor.printProgressBar(indexProv + 1, len(listDropdownMain), prefix = 'Progress:', suffix = 'Complete', length = 50)