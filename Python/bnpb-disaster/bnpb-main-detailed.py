#!/usr/bin/env python
# coding: utf-8
# author: audhiaprilliant

# Web scraping
from selenium import webdriver
from bs4 import BeautifulSoup
# Data manipulation
import pandas as pd
# Timing
import time
# JSON
import json
# System management
import sys

# Argument
data_location = sys.argv[1]

# Open the JSON data
with open(data_location) as file:
    file_json = json.load(file)

# Get list of links
links = []
for key in file_json.keys():
	links += file_json[key]['Links']

# Open the driver
DRIVER_PATH = 'bin/chromedriver'
driver = webdriver.Chrome(executable_path = DRIVER_PATH)

# Current time
now = time.strftime('%Y%m%d%H%M%S')

# Data set in JSON
df_json = {}

# Collect the data
for link in links:
	try:
		# Access to main link
		driver.get(link)
		time.sleep(1.5)

		# Dictionary
		dict_init = {
			'latitude': None,
			'longitude': None,
			'keterangan': None,
			'sumber': None,
			'tgl': None,
			'id_jenis_bencana': None,
			'prop': None,
			'kab': None
		}

		# Get the values
		for key in dict_init.keys():
			# Get the value
			try:
				value = driver.find_element_by_name(key).get_attribute('value')
			except:
				value = None

			# Update the dictionary
			dict_init.update(
					{
						key: value
					}
				)

		# Append the dictionary
		df_json.update(
				{
					str(link): dict_init
				}
			)

		# Status
		print('Scraping for {link} is done, continue to the next page'.format(link = link))

	except:
		# Status
		print('Error for {link}'.format(link = link))

# SAVE DATA INTO JSON FILE
# Serialize json 
json_object = json.dumps(df_json, indent = 4)
# Write to JSON
filename = 'data/raw/bnpb-data-detailed-{date}.json'.format(
	date = now
)
with open(filename, 'w') as outfile:
	outfile.write(json_object)