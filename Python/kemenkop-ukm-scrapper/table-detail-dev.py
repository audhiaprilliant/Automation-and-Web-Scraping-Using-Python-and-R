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
# Module for regular expression
import re
# Module for JSON
import json
# Module for folders
import os

# Local directory for running the script
root_path = os.getcwd()
# Configuration of Chromedriver
DRIVER_PATH = root_path + '/bin/chromedriver'
DATA_PATH = root_path + '/data/raw'
# Configuration for headless Selenium
options = Options()
options.add_argument('--headless')
# Get all directories in our base path.
folder = sorted(os.listdir(DATA_PATH), key = lambda x: int(x[0:2]))
folder = folder[25:30]

# Main program
if __name__ == '__main__':
	# Load the Chromedriver and get the url
	driver = webdriver.Chrome(executable_path = DRIVER_PATH)
	# Traverse each folders in base path
	for dir_ in folder:
		# Subfolders
		subfolders = os.path.join(DATA_PATH, dir_)

		# Logging
		print('===========================')
		
		# Files in subfolders
		subsubfolders = sorted(os.listdir(subfolders), key = lambda x: int(x[0:2]))
		subsubfolders = subsubfolders[:]
		for subsubfolder in subsubfolders:
			subsubsufolders = os.path.join(subfolders, subsubfolder)
			
			# Files in subfolders
			files = os.listdir(subsubsufolders)
			for file in files:
				data_dir = os.path.join(subsubsufolders, file)
				
				# Logging
				print(subsubsufolders)

				# OPEN JSON FILE
				with open(data_dir) as f:
					file_json = json.load(f)
				
				# Data
				df_json = {}

				# Links
				links = file_json['Links']
				for link in links:
					# Get the url
					driver.get(link)
					
					try:
						# Get the table elements
						tableObj = driver.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
						
						# Column names
						listVal = {}

						# Get the column names
						for elem in tableObj:
							val = elem.find_elements_by_tag_name('td')
							
							# Get the key and value
							if val[0].text not in ['DATA KOPERASI', 'DATA PENGURUS', 'DATA KELEMBAGAAN', 'DATA LAINNYA']:
								key = val[0].text
								value = val[1].text

								# Update the dictionary
								listVal.update(
									{
										key: value
									}
								)
							else:
								pass

						# Store the data
						# NIK
						ids = re.findall(pattern = '(\d+)', string = link)
						# The data
						df = {
							str(ids[0]): listVal
						}
						
						# Concate the data
						df_json = {**df_json, **df}

					except:
						print('Warning! Failed to scrape (link): {}'.format(link = link))
						pass

				# Serialize JSON
				json_object = json.dumps(df_json, indent = 4)
				
				# Write to JSON
				filename = subsubsufolders + '/{dist} - Detail.json'.format(dist = file.replace(' - District.json', ''))
				with open(filename, 'w') as outfile:
					outfile.write(json_object)