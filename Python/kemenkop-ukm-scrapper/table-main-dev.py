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
# Configuration of Chromedriver
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

	# 3 Loop the main dropdown
	statProvince = True
	idxProv = 32
	while statProvince:
		try:
			
			# 5 Select the one element in dropdown
			statDistrict = True
			idxDistrict = 0
			while statDistrict:
				try:
					# Access to the main page
					driver.get('http://nik.depkop.go.id/')
					time.sleep(2)

					# Dropdown of province
					try:
						provElem = listDropdownMain[idxProv]
					except:
						statProvince = False

					# Get the dropdown object
					dropdownMain = driver.find_element_by_id('MainContent_DropDownList1')
					# Select the dropdown object
					selectorMain = Select(dropdownMain)

					# Select the province
					selectorMain.select_by_visible_text(provElem)

					# Create the folder
					provincePath = DATA_PATH + '/' + str(idxProv) + ' ' + provElem.replace('/', '_')
					Path(provincePath).mkdir(parents = True, exist_ok = True)

					# Logging
					print(provElem)
					
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

					# Dropdown of districts
					try:
						districtElem = listDropdownSubmain[idxDistrict]
					except:
						statDistrict = False
					
					# Logging
					print(districtElem)

					# Data in JSON
					df_json = {}

					# Get the dropdown object
					dropdownSubmain = driver.find_element_by_id('MainContent_DropDownList2')
					# Select the dropdown object
					selectorSubmain = Select(dropdownSubmain)

					# Select the district
					selectorSubmain.select_by_visible_text(districtElem)

					# 7 Pagination
					try:
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

						# Object of pagination
						pageObj = tableObj.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[0]
						# Pagination
						pages = pageObj.find_elements_by_tag_name('a')
						# Active pages
						activePages = pages[0:]
						l = []
						for i in activePages:
							l.append(i.text)

						# Loop
						print(l)
						lastPage = 1
						last = 0
						
						while lastPage != last:

							if l[len(l) - 1] == '...':
								
								pageCount = int(l[0])
								print('Up', pageCount)

								while pageCount <= int(l[len(l) - 2]):

									# Get the table object
									tableObj = driver.find_element_by_id('MainContent_GridView1')

									# Sleep
									time.sleep(2)

									# Data collections
									dataCollection = tableObj.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')

									# Filter the data
									dataColFilter = dataCollection[3:len(dataCollection) - 2]

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
									# Increase page_count value on each iteration on +1
									pageCount += 1

								# Last index
								try:
									driver.find_elements_by_link_text(l[len(l) - 1])[1].click()
								except:
									driver.find_elements_by_link_text(l[len(l) - 1])[0].click()
						        
								# Object of pagination
								tableObj = driver.find_element_by_id('MainContent_GridView1')
								pageObj = tableObj.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[0]
								# Pagination
								pages = pageObj.find_elements_by_tag_name('a')

								# Active pages
								activePages = pages[0:]
								k = []
								for i in activePages:
									k.append(i.text)

								# Complement of two lists
								k = sorted(list(set(k[:len(k) - 1]) - set(l))) + [k[len(k) - 1]]
								# Special case of pagination
								if len(k) == 1:
									k[0] = str(int(k[0]) + 1)

								l = k
								lastPage = l[len(l) - 1]

							else:
								lastPage = l[len(l) - 1]
								pageCount = int(l[0])

								while True:
									print('Bottom', pageCount)
									# Get the table object
									tableObj = driver.find_element_by_id('MainContent_GridView1')

									# Sleep
									time.sleep(2)

									# Data collections
									dataCollection = tableObj.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')

									# Filter the data
									dataColFilter = dataCollection[3:len(dataCollection) - 2]

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
									
									# Increase page_count value on each iteration on +1
									pageCount += 1

								# Last index
								last = l[len(l) - 1]

					except:
						# Get the table object
						tableObj = driver.find_element_by_id('MainContent_GridView1')
						# Object for column names
						colNames = tableObj.find_elements_by_tag_name('tr')[0].find_elements_by_tag_name('th')
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

						try:
							# 6 Get the column names
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
						except:
							pass

					# 8 Concate the data
					df_json = {**df_json, **dict_init}

					# 9 Create a folder
					districtPath = provincePath + '/' + str(idxDistrict) + ' ' + districtElem.replace('/', '_')
					Path(districtPath).mkdir(parents = True, exist_ok = True)

					# 10 Serialize JSON
					json_object = json.dumps(df_json, indent = 4)
					
					# 11 Write to JSON
					filename = districtPath + '/{dist} - District.json'.format(dist = districtElem)
					with open(filename, 'w') as outfile:
						outfile.write(json_object)

					# Add the index
					idxDistrict += 1

				except:
					print('Warning! Failed to scrape (district): {}'.format(listDropdownSubmain[idxDistrict]))
					pass

			# Add the index
			idxProv += 1

		except:
			print('Warning! Failed to scrape (province): {}'.format(listDropdownMain[idxProv]))
			pass