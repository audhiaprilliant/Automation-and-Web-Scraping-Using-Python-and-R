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

# ARGUMENTS
start_page = sys.argv[1]
end_page = sys.argv[2]

# MAIN PAGES IN LPSE
main_links = {
	'Tender': 'https://lpse.lkpp.go.id/eproc4/lelang',
	'Non Tender': 'https://lpse.lkpp.go.id/eproc4/nontender',
	'Pencatatan Non Tender': 'https://lpse.lkpp.go.id/eproc4/pencatatan',
	'Pencatatan Swakelola': 'https://lpse.lkpp.go.id/eproc4/swakelola',
	'Pencatatan Pengadaan Darurat': 'https://lpse.lkpp.go.id/eproc4/darurat'
}

# ACCESS TO MAIN URL
DRIVER_PATH = 'bin/chromedriver'
driver = webdriver.Chrome(executable_path = DRIVER_PATH)
driver.get(main_links['Tender'])

# SELECT MATCH CATEGORY
# 1 Tender type
dropdownTenders = driver.find_element_by_name('kategoriId')
selectorTenders = Select(dropdownTenders)
# List of dropdown list
listTenderType = []
options = selectorTenders.options
for index in range(len(options)):
	listTenderType.append(options[index].text)
# Clean categories
listTenderTypeClean = listTenderType[1: len(listTenderType)]
# Select by visible text
selectorTenders.select_by_visible_text(listTenderTypeClean[len(listTenderTypeClean) - 1])
# 2 Institutions
dropdownInstitution = driver.find_element_by_name('instansiId')
selectorInstitution = Select(dropdownInstitution)
# List of dropdown list
listInstitutions = []
options = selectorInstitution.options
for index in range(len(options)):
	listInstitutions.append(options[index].text)
# Clean categories
listInstitutionsClean = listInstitutions[1: len(listInstitutions)]
# Select by visible text
selectorInstitution.select_by_visible_text(listInstitutionsClean[len(listInstitutionsClean) - 1])
# 3 Fiscal year
dropdownYear = driver.find_element_by_name('tahun')
selectorYear = Select(dropdownYear)
# List of dropdown list
listYears = []
options = selectorYear.options
for index in range(len(options)):
	listYears.append(options[index].text)
# Clean categories
listYearsClean = listYears[1: len(listYears)]
# Select by visible text
selectorYear.select_by_visible_text(listYearsClean[len(listYearsClean) - 1])

# LOOPING
# Find final page
elemPage = driver.find_element_by_class_name('pagination').find_elements_by_tag_name('li')
final_page = elemPage[len(elemPage) - 3].text
# Start page
if start_page == 'start':
	start_page = 0
else:
	start_page = start_page
# Final page
if end_page == 'end':
	final_page = final_page
else:
	final_page = end_page
# Extract the data
df_json = {}
page = 0
while page < int(final_page):
	if page >= int(start_page):
		try:
			# Get the column elements
			tenderSummaryData = driver.find_element_by_id('tbllelang')
			# element for column names
			colNames = tenderSummaryData.find_element_by_tag_name('thead').find_elements_by_tag_name('th')
			# Column names
			listCols = []
			for elem in colNames:
				col_raw = elem.text
				listCols.append(col_raw)
			# Result
			listCols = [i.replace('\n', ' ') for i in listCols]
			# Data collections
			dataCollection = tenderSummaryData.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
			# Dictionary with blank list
			dict_init = {key: [] for key in listCols}
			# Get data
			for row in dataCollection:
				elemValues = row.find_elements_by_tag_name('td')
				for col in range(len(elemValues)):
					try:
						value = elemValues[col].find_elements_by_tag_name('a')[0].text
					except:
						value = elemValues[col].text
					# Append values
					dict_init[list(dict_init.keys())[col]].append(value)
			# Link
			listLinkTitle = []
			for idx in range(len(dataCollection)):
				linkTitleElement = dataCollection[idx].find_elements_by_tag_name('td')[1]
				link_title_text_raw = linkTitleElement.find_elements_by_tag_name('a')[0].get_attribute('href')
				listLinkTitle.append(link_title_text_raw)
			# Subtitle
			listSubtitle = []
			for idx in range(len(dataCollection)):
				subtitleElement = dataCollection[idx].find_elements_by_tag_name('td')[1]
				subtitle_text_raw = subtitleElement.find_elements_by_tag_name('p')[1].text
				listSubtitle.append(subtitle_text_raw)
			# Captions
			listCaption = []
			for idx in range(len(dataCollection)):
				captionElement = dataCollection[idx].find_elements_by_tag_name('td')[1]
				caption_text_raw = captionElement.find_elements_by_tag_name('p')[2].text
				listCaption.append(caption_text_raw)
			# Annotation
			listAnnotation = []
			for idx in range(len(dataCollection)):
				annotationElement = dataCollection[idx].find_elements_by_tag_name('td')[1]
				annotationElements = annotationElement.find_elements_by_tag_name('span')
				listInAnnotation = []
				for j in range(len(annotationElements)):
					annotation_text_raw = annotationElements[j].text
					listInAnnotation.append(annotation_text_raw)
				listAnnotation.append(listInAnnotation)
			# Tender schedule
			listLinkStatus = []
			for idx in range(len(dataCollection)):
				linkStatusElement = dataCollection[idx].find_elements_by_tag_name('td')[3]
				links_status_text_raw = linkStatusElement.find_elements_by_tag_name('a')[0].get_attribute('href')
				listLinkStatus.append(links_status_text_raw)
			# Append dictionary
			dict_init['Link Paket'] = listLinkTitle
			dict_init['Penjelasan Singkat Paket'] = listSubtitle
			dict_init['Status Harga Paket'] = listCaption
			dict_init['Spesifikasi Paket'] = listAnnotation
			dict_init['Link Tahapan Paket'] = listLinkStatus
			# Add tender's code as identifier
			code_tender = page
			dict_full = {
				code_tender: dict_init
			}
			df_json = {**df_json, **dict_full}
			# Next page
			print("Hey, we're now in page {}".format(page))
			nextPage = driver.find_element_by_class_name('pagination').find_element_by_id('tbllelang_next')
			driver.execute_script('arguments[0].click();', nextPage)
			time.sleep(2)
			# Move to next page
			page += 1
		except:
			continue
	else:
		nextPage = driver.find_element_by_class_name('pagination').find_element_by_id('tbllelang_next')
		driver.execute_script('arguments[0].click();', nextPage)
		time.sleep(2)
		# Move to next page
		page += 1

# SAVE DATA INTO JSON FILE
# Serialize json 
json_object = json.dumps(df_json, indent = 4)
# Write to JSON
now = datetime.today().strftime('%y-%m-%d %H-%M-%S')
filename = 'data/raw/LPSE Tender Data - Page {start} to {end} - {now}.json'.format(
	start = start_page,
	end = final_page,
	now = now
)
with open(filename, 'w') as outfile:
	outfile.write(json_object)