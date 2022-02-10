#!/usr/bin/env python
# coding: utf-8
# author: audhiaprilliant

# Web scraping
from selenium import webdriver
from bs4 import BeautifulSoup
# Data manipulation
import pandas as pd
# Regular expression
import re
# Timing
import time
# JSON
import json

# Open the driver
DRIVER_PATH = 'bin/chromedriver'
driver = webdriver.Chrome(executable_path = DRIVER_PATH)

# Current time
now = time.strftime('%Y%m%d%H%M%S')

# Data set in JSON
df_json = {}

# Status
status = True
# Initial page
page = 0
while status:
	try:
		# Main link
		main_link = 'https://dibi.bnpb.go.id/xdibi?pr=&kb=&jn=&th=&bl=&tb=2&st=3&kf=0&start={page}'.format(page = page)
		time.sleep(3)
		
		# Access to main link
		driver.get(main_link)

		# GET COLUMN NAMES
		# Column data collections
		dataCollection = driver.find_element_by_class_name('col-md-12')
		
		# Get the column elements
		columnCollection = dataCollection.find_element_by_tag_name('thead').find_elements_by_tag_name('th')
		
		# Get column names
		listColNames = []
		for elemCol in columnCollection:
			listColNames.append(elemCol.text)
		
		# Result
		listCols = [re.sub('[^a-zA-Z\d]', '', x) for x in listColNames]
		listCols[len(listCols) - 1] = 'Links'
		
		# Dictionary with blank list
		dict_init = {key: [] for key in listCols}

		# GET THE VALUES IN TABLE
		# Data collections
		valueCollection = dataCollection.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')

		# Get the values in table for non-span object
		for row in valueCollection:
			elemValues = row.find_elements_by_tag_name('td')
			for col in range(len(elemValues)):
				try:
					value = elemValues[col].text
				except:
					value = None
				# Append values
				dict_init[list(dict_init.keys())[col]].append(value)

		# Get links
		links = driver.find_elements_by_class_name('btn.btn-info.btn-xs')
		listLink = [link.get_attribute('href') for link in links]

		# Get the values in table for span object
		spanDetailed = []
		for i in dataCollection.find_elements_by_tag_name('span'):
			# Get the span type
			spanType = i.get_attribute('data-toggle')
			# Select only popover
			if spanType == 'popover':
				classValue = i.get_attribute('data-original-title')
				if re.sub('[^a-zA-Z\d]', '', classValue) in ['Keterangan', 'Korban', 'Kerusakan']:
					spanDetailed.append(i)

		# Detailed values
		listDetailed = []
		for idx in range(3, len(spanDetailed) + 3, 3):
			# Dictionary for storing data
			dictDetailed = {}
			# Looping per 3 object
			for j in range(idx - 3, idx):
				classValue = re.sub('[^a-zA-Z\d]', '', spanDetailed[j].get_attribute('data-original-title'))
				# Get the values
				if classValue != None:
					dictDetailed.update(
						{
							classValue: spanDetailed[j].get_attribute('data-content')
						}
					)
				else:
					dictDetailed.update(
						{
							classValue: None
						}
					)
			# Append the dictionary
			listDetailed.append(dictDetailed)

		# Update the dictionary
		dict_init.update(
			{
				'Detail': listDetailed,
				'Links': listLink
			}
		)

		# Append the dictionary
		df_json.update(
			{
				str(page): dict_init
			}
		)

		# Status
		print('Scraping in page {page} is done, continue to page {next}'.format(page = page, next = page + 10))

		# Move to next page
		page += 10

	except:
		# Status
		print('Error in page {page}, continue to page {next}'.format(page = page, next = page + 10))

		# Move to next page
		page += 10

		# Update stop criteria
		status = False

# SAVE DATA INTO JSON FILE
# Serialize json 
json_object = json.dumps(df_json, indent = 4)
# Write to JSON
filename = 'data/raw/bnpb-data-{date}.json'.format(
	date = now
)
with open(filename, 'w') as outfile:
	outfile.write(json_object)