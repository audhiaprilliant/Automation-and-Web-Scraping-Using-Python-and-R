#!/usr/bin/env python
# coding: utf-8
# author: audhiaprilliant

# Module for web scraping
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
# Module for data manipulation
import pandas as pd
# Import module for passing variable
import sys
# Module for file management
from pathlib import Path
import os
# Module for regular expression
import re
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
# Read JSON object as a dictionary for Telegram bot
with open(root_path + '/config/telegram.json') as tele_data:
    telegram_bot = json.load(tele_data)
telegram_chatid = telegram_bot['result'][0]['message']['chat']['id']
telegram_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# Main program
if __name__ == '__main__':
	# 1 Load the Chromedriver and get the url
	driver = webdriver.Chrome(executable_path = DRIVER_PATH)
	driver.get('https://sig-dev.bps.go.id/webgis/pencariankodenama')
	time.sleep(2)
	# 2 Select the BPS-Kemendagri page
	dropdownPanel = driver.find_element_by_class_name('panel-title')
	# Click the main panel
	dropdownPanel.click()
	time.sleep(1)
	mainPanel = driver.find_element_by_id('collapse1')
	bpsMendagriPanel = mainPanel.find_elements_by_tag_name('li')[0]
	# Click the BPS-Kemendagri page
	bpsMendagriPanel.click()
	time.sleep(1)

	# 3 Select the historical records - dropdown
	dropdownRecords = driver.find_element_by_id('periode1-bridg')
	selectorRecords = Select(dropdownRecords)
	# List of dropdown list
	listDropdownRecords = []
	options = selectorRecords.options
	for index in range(len(options)):
	    listDropdownRecords.append(options[index].text)
	# Select by visible text - last records
	selectorRecords.select_by_visible_text(listDropdownRecords[len(listDropdownRecords) - 1])
	time.sleep(2)
	# 4 Get the province data
	tableProvince = driver.find_element_by_id('data-table')
	time.sleep(1)
	# Get column for headers
	fileDataProvince = []
	fileHeaderProvince = []
	headLineProvince = tableProvince.find_elements_by_tag_name('tr')
	time.sleep(1)
	headers = headLineProvince[1].find_elements_by_tag_name('th')
	for header in headers:
	    header_text_raw = header.text
	    fileHeaderProvince.append(header_text_raw)
	fileDataProvince.append(';'.join(fileHeaderProvince))
	# Get the rows
	bodyRowsProvince = tableProvince.find_elements_by_tag_name('tr')
	for row in bodyRowsProvince:
	    data = row.find_elements_by_tag_name('td')
	    file_row = []
	    for datum in data:
	        datum_text_byte = datum.text.encode('utf8')
	        datum_text_raw = datum_text_byte.decode('utf-8')
	        file_row.append(datum_text_raw)
	    fileDataProvince.append(';'.join(file_row))
	# Remove indexes which are header
	del(fileDataProvince[1:3])
	# Convert to dataframe
	dataProvinces = pd.DataFrame(columns = fileDataProvince[0].split(';'), data=[row.split(';') for row in fileDataProvince[1:]])
	dataProvinces.rename(columns = {'-':'No'}, inplace = True)
	# Regular expression
	dataProvinces.replace('/', '_', regex = True, inplace = True)
	# Save the provinces data
	provPath = DATA_PATH + '/' + 'INDONESIA'
	Path(provPath).mkdir(parents = True, exist_ok = True)
	dataProvinces.to_csv(provPath + '/PROVINSI INDONESIA.csv', sep = ';', index = False)
	time.sleep(1)

	# 5 Get the distric data
	dropdownProvinces = driver.find_element_by_id('provinsi-dropdown-bridg')
	selectorProvinces = Select(dropdownProvinces)
	# List of provinces
	listDropdownProvince = []
	options = selectorProvinces.options
	for index in range(len(options)):
	    listDropdownProvince.append(options[index].text)
	# Remove the first element of list
	del listDropdownProvince[0]
	# Monitoring - provinces
	monitor.printProgressBar(0, len(listDropdownProvince), prefix = 'Progress:', suffix = 'Complete', length = 50)
	# Select by visible text
	for indexProv, provElem in enumerate(listDropdownProvince[19:]):
		# Get the district data
		selectorProvinces.select_by_visible_text(provElem)
		time.sleep(2)
		# Get the district table
		tableDistrict = driver.find_element_by_id('data-table')
		time.sleep(1)
		# Get column for headers
		fileDataDistrict = []
		fileHeaderDistrict = []
		headLineDistrict = tableDistrict.find_elements_by_tag_name('tr')
		time.sleep(1)
		headers = headLineDistrict[1].find_elements_by_tag_name('th')
		for header in headers:
		    header_text_raw = header.text
		    fileHeaderDistrict.append(header_text_raw)
		fileDataDistrict.append(';'.join(fileHeaderDistrict))
		# Get the rows
		bodyRowsDistrict = tableDistrict.find_elements_by_tag_name('tr')
		for row in bodyRowsDistrict:
		    data = row.find_elements_by_tag_name('td')    
		    file_row = []
		    for datum in data:
		        datum_text_byte = datum.text.encode('utf8')
		        datum_text_raw = datum_text_byte.decode('utf-8')
		        file_row.append(datum_text_raw)
		    fileDataDistrict.append(';'.join(file_row))
		# Remove indexes which are header
		del(fileDataDistrict[1:3])
		# Convert to dataframe
		dataDistrict = pd.DataFrame(columns = fileDataDistrict[0].split(';'), data = [row.split(';') for row in fileDataDistrict[1:]])
		dataDistrict.rename(columns = {'-':'No'}, inplace = True)
		# Regular expression
		dataDistrict.replace('/', '_', regex = True, inplace = True)
		# Save the districts data
		distrPath = provPath + '/' + provElem.replace('/', '_')
		Path(distrPath).mkdir(parents = True, exist_ok = True)
		dataDistrict.to_csv(distrPath + '/{} - DISTRICTS.csv'.format(provElem.replace('/', '_')), sep = ';', index = False)
		time.sleep(1)

		# 6 Get the subdistrict data
		dropdownDistricts = driver.find_element_by_id('kabupaten-dropdown-bridg')
		selectorDistricts = Select(dropdownDistricts)
		# List of district
		listDropdownDistrict = []
		options = selectorDistricts.options
		for index in range(len(options)):
		    listDropdownDistrict.append(options[index].text)
		# Remove the first element of list
		del listDropdownDistrict[0]
		# Select by visible text
		for indexDistr, distrElem in enumerate(listDropdownDistrict):
			# Get the subdistrict data
			selectorDistricts.select_by_visible_text(distrElem)
			time.sleep(2)
			# Get the subdistrict table
			tableSubdistrict = driver.find_element_by_id('data-table')
			time.sleep(1)
			# Get column for headers
			fileDataSubdistrict = []
			fileHeaderSubdistrict = []
			headLineSubdistrict = tableSubdistrict.find_elements_by_tag_name('tr')
			time.sleep(1)
			headers = headLineSubdistrict[1].find_elements_by_tag_name('th')
			for header in headers:
			    header_text_raw = header.text
			    fileHeaderSubdistrict.append(header_text_raw)
			fileDataSubdistrict.append(';'.join(fileHeaderSubdistrict))
			# Get the rows
			bodyRowsSubdistrict = tableSubdistrict.find_elements_by_tag_name('tr')
			for row in bodyRowsSubdistrict:
			    data = row.find_elements_by_tag_name('td')    
			    file_row = []
			    for datum in data:
			        datum_text_byte = datum.text.encode('utf8')
			        datum_text_raw = datum_text_byte.decode('utf-8')
			        file_row.append(datum_text_raw)
			    fileDataSubdistrict.append(';'.join(file_row))
			# Remove indexes which are header
			del(fileDataSubdistrict[1:3])
			# Convert to dataframe
			dataSubdistrict = pd.DataFrame(columns = fileDataSubdistrict[0].split(';'), data = [row.split(';') for row in fileDataSubdistrict[1:]])
			dataSubdistrict.rename(columns = {'-':'No'}, inplace = True)
			# Regular expression
			dataSubdistrict.replace('/', '_', regex = True, inplace = True)
			# Save the subdistricts data
			subdistrPath = distrPath + '/' + distrElem.replace('/', '_')
			Path(subdistrPath).mkdir(parents = True, exist_ok = True)
			dataSubdistrict.to_csv(subdistrPath + '/{} - SUBDISTRICTS.csv'.format(distrElem.replace('/', '_')), sep = ';', index = False)
			time.sleep(1)

			# 7 Get the village data
			dropdownSubdistricts = driver.find_element_by_id('kecamatan-dropdown-bridg')
			selectorSubdistricts = Select(dropdownSubdistricts)
			# List of subdistrict
			listDropdownSubdistrict = []
			options = selectorSubdistricts.options
			for index in range(len(options)):
			    listDropdownSubdistrict.append(options[index].text)
			# Remove the first element of list
			del listDropdownSubdistrict[0]
			# Select by visible text
			for indexSubdistr, subdistrElem in enumerate(listDropdownSubdistrict):
				# Get the subdistrict data
				selectorSubdistricts.select_by_visible_text(subdistrElem)
				time.sleep(3)
				# Get the subdistrict table
				try:
					tableVillage = driver.find_element_by_id('data-table')
					time.sleep(2)
					# Get column for headers
					fileDataVillage = []
					fileHeaderVillage = []
					headLineVillage = tableVillage.find_elements_by_tag_name('tr')
					time.sleep(1)
					headers = headLineVillage[1].find_elements_by_tag_name('th')
					for header in headers:
					    header_text_raw = header.text
					    fileHeaderVillage.append(header_text_raw)
					fileDataVillage.append(';'.join(fileHeaderVillage))
					# Get the rows
					bodyRowsVillage = tableVillage.find_elements_by_tag_name('tr')
					for row in bodyRowsVillage:
					    data = row.find_elements_by_tag_name('td')    
					    file_row = []
					    for datum in data:
					        datum_text_byte = datum.text.encode('utf8')
					        datum_text_raw = datum_text_byte.decode('utf-8')
					        file_row.append(datum_text_raw)
					    fileDataVillage.append(';'.join(file_row))
					# Remove indexes which are header
					del(fileDataVillage[1:3])
					# Convert to dataframe
					dataVillage = pd.DataFrame(columns = fileDataVillage[0].split(';'), data = [row.split(';') for row in fileDataVillage[1:]])
					dataVillage.rename(columns = {'-':'No'}, inplace = True)
					# Regular expression
					dataVillage.replace('/', '_', regex = True, inplace = True)
					# Save the village data
					villagePath = subdistrPath + '/' + subdistrElem.replace('/', '_')
					Path(villagePath).mkdir(parents = True, exist_ok = True)
					dataVillage.to_csv(villagePath + '/{} - VILLAGES.csv'.format(subdistrElem.replace('/', '_')), sep = ';', index = False)
					time.sleep(1)
				except:
					# Telegram notification
					message = 'WARNING! {province}-{district} data is not successfully scraped on {scraped_date} at {scraped_time}'.format(province = provElem,
						district = distrElem,
						scraped_date = pd.to_datetime('today').strftime('%m-%d-%Y'),
						scraped_time = pd.to_datetime('today').strftime('%H:%M:%S'))
					# Send text message
					send_text = 'https://api.telegram.org/bot'+bot_token+'/sendMessage?chat_id='+bot_chatID+'&parse_mode=Markdown&text='+message
					requests.get(send_text)
					time.sleep(1)
					continue
			# Telegram notification
			message = '{province}-{district} data is successfully scraped on {scraped_date} at {scraped_time}'.format(province = provElem,
				district = distrElem,
				scraped_date = pd.to_datetime('today').strftime('%m-%d-%Y'),
				scraped_time = pd.to_datetime('today').strftime('%H:%M:%S'))
			# Send text message
			send_text = 'https://api.telegram.org/bot'+bot_token+'/sendMessage?chat_id='+bot_chatID+'&parse_mode=Markdown&text='+message
			requests.get(send_text)
			time.sleep(1)

		# Monitoring - provinces
		time.sleep(0.1)
		monitor.printProgressBar(indexProv + 1, len(listDropdownProvince), prefix = 'Progress:', suffix = 'Complete', length = 50)
