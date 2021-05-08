#!/usr/bin/env python
# coding: utf-8
# author: audhiaprilliant

# Module for web scraping
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
# URL encoding
from requests.utils import requote_uri
# Module for data manipulation
import pandas as pd
# Import module for passing variable
import sys
# Module for file management
import os
# Module for regular expression
import re
# Module for binary search and sorting
import bisect
from src.data import data_validator as validator
# Module for monitoring
import time
from src.tools import monitor as monitor
# Module for parsing JSON
import json
# Module for csv file export
import csv

# Local directory for running the script
root_path = os.getcwd()
# Configuration of Chromedriver and BPS site
DRIVER_PATH = root_path + '/bin/chromedriver'
DATA_PATH = root_path + '/data'
# Configuration for headless Selenium
options = Options()
#options.add_argument('--headless')
options.add_argument('--start-maximized')
options.add_argument('window-size=2560,1440')
# Configuration for the URL
# Main URL
url = 'https://shopee.co.id/'
# Configuration for Telegram bot
bot_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
content = requests.get("https://api.telegram.org/bot{}/getUpdates".format(bot_token))
telegram_bot = json.loads(content.content)
telegram_chatid = telegram_bot['result'][0]['message']['chat']['id']
bot_chatID = str(telegram_chatid)

# Main program
if __name__ == '__main__':
	# Load the Chromedriver and get the url
	driver = webdriver.Chrome(executable_path = DRIVER_PATH, options = options)
	# Load the csv file for scraping
	df = pd.read_csv(DATA_PATH + '/interim/' + sys.argv[1], sep = ';')
	for index in range(len(df)):
		username = df['Username'][index]
		# Access to the URL
		url_query = url + username
		driver.get(url_query)
		time.sleep(2)
		# List for product
		linkProduct = []
		nameProduct = []
		priceProduct = []
		ratingProduct = []
		soldProduct = []
		placeProduct = []
		reviewProduct = []
		favProduct = []
		specProduct = []
		descProduct = []
		# Product category
		categoryList = []
		try:
			category = driver.find_elements_by_class_name('_3yjqG-')
			for i in range(1, len(category)):
				categoryList.append(category[i].text)
		except:
			categoryList = ['']
			continue
		catProduct = str(categoryList)
		# Scroll down the page slowly
		scroll_height = driver.execute_script('return document.documentElement.scrollHeight;')
		for iters in range(0, scroll_height, 200):
			driver.execute_script('window.scrollTo(0, {});'.format(iters))
			time.sleep(1)
		maxPage = driver.find_element_by_class_name('shopee-mini-page-controller__total').text
		for page in range(int(maxPage)):
			try:
				# The URL
				url_page = 'https://shopee.co.id/' + username + '?page=' + str(page) + '&sortBy=pop'
				driver.get(url_page)
				time.sleep(2)
				driver.execute_script('window.scrollTo(0, {});'.format(1000))
				# Links
				product_list = driver.find_elements_by_class_name('shop-search-result-view')
				link = product_list[0].find_elements_by_tag_name('a')
				linkProductTemp = []
				for elem in link:
					link_elem = elem.get_attribute('href')
					linkProductTemp.append(link_elem)
				linkProduct += linkProductTemp
				# Product name
				product = product_list[0].find_elements_by_class_name('PFM7lj')
				for elem in product:
					name_elem = elem.text
					nameProduct.append(name_elem)
				# Product price
				price = product_list[0].find_elements_by_class_name('_32hnQt')
				for elem in price:
					price_elem = elem.text
					priceProduct.append(price_elem)
				# Product rating
				rating = product_list[0].find_elements_by_class_name('_3dC36C')
				for elem in rating:
					rating_elem = len(elem.find_elements_by_class_name('shopee-rating-stars__star-wrapper'))
					ratingProduct.append(rating_elem)
				# Product sold out
				sold = product_list[0].find_elements_by_class_name('go5yPW')
				for elem in sold:
					sold_elem = elem.text
					soldProduct.append(sold_elem)
				# Product place
				place = product_list[0].find_elements_by_class_name('_2CWevj')
				for elem in place:
					place_elem = elem.text
					placeProduct.append(place_elem)
				# Dive into product details
				for i in range(len(linkProductTemp)):
					driver.get(linkProductTemp[i])
					time.sleep(2)
					driver.execute_script('window.scrollTo(0, {});'.format(1000))
					# Product review
					try:
						review = driver.find_elements_by_class_name('OitLRu')[1].text
					except:
						review = ''
					reviewProduct.append(review)
					# Product fav
					try:
						fav = driver.find_elements_by_class_name('_39mrb_')[1].text
					except:
						fav = ''
					favProduct.append(fav)
					# Product specification
					length_element = len(driver.find_elements_by_class_name('aPKXeO'))
					specification = {}
					for index in range(length_element):
						key = driver.find_elements_by_class_name('aPKXeO')[index].find_elements_by_class_name('SFJkS3')[0].text
						try:
							value = driver.find_elements_by_class_name('aPKXeO')[index].find_elements_by_tag_name('div')[0].text
						except:
							value = ''
						specification.update({key: value})
					specProduct.append(str(specification))
					# Product description
					try:
						desc = driver.find_element_by_class_name('_3yZnxJ').text.encode('utf-8')
					except:
						desc = ''
					descProduct.append(desc)
				# Telegram notification
				message = 'The {user} data on page {page}/{max_page} is successfully scraped on {scraped_date} at {scraped_time}. Total data successfully scraped is {num}'.format(
					user = username,
					page = page,
					max_page = maxPage,
					scraped_date = pd.to_datetime('today').strftime('%m-%d-%Y'),
					scraped_time = pd.to_datetime('today').strftime('%H:%M:%S'),
					num = len(linkProduct))
				# Dump the data into database
				df_dump = pd.DataFrame(
								{
									'Username': [username] * len(linkProduct),
									'Category': [catProduct] * len(linkProduct),
									'Place': placeProduct,
									'Product Link': linkProduct,
									'Product Name': nameProduct,
									'Product Price': priceProduct,
									'Product Rating': ratingProduct,
									'Product Sold Out': soldProduct,
									'Number of Product Review': reviewProduct,
									'Number of Product Favorite': favProduct,
									'Product Specification': specProduct,
									'Product Description': descProduct
								}
							)
				with open(DATA_PATH + '/raw/' + 'dump_data_product.csv', 'w', newline = '') as ff:
					df_dump.to_csv(ff, header = True, sep = ';', index = False, encoding = 'utf-8', quotechar = '"', quoting = csv.QUOTE_ALL)
					ff.close()
			except:
				# Telegram notification
				message = 'WARNING! The {user} data on page {page}/{max_page} is not successfully scraped on {scraped_date} at {scraped_time}'.format(
					user = username,
					page = page,
					max_page = maxPage,
					scraped_date = pd.to_datetime('today').strftime('%m-%d-%Y'),
					scraped_time = pd.to_datetime('today').strftime('%H:%M:%S'))
				# Send text message
				send_text = 'https://api.telegram.org/bot'+bot_token+'/sendMessage?chat_id='+bot_chatID+'&parse_mode=Markdown&text='+message
				requests.get(send_text)
				time.sleep(1)
				continue
			# Iteration monitoring
			print('{username} - {page}/{max_page}'.format(
				username = username,
				page = page,
				max_page = maxPage))
		# Create a dataframe
		df_result = pd.DataFrame(
						{
								'Username': [username] * len(linkProduct),
								'Category': [catProduct] * len(linkProduct),
								'Place': placeProduct,
								'Product Link': linkProduct,
								'Product Name': nameProduct,
								'Product Price': priceProduct,
								'Product Rating': ratingProduct,
								'Product Sold Out': soldProduct,
								'Number of Product Review': reviewProduct,
								'Number of Product Favorite': favProduct,
								'Product Specification': specProduct,
								'Product Description': descProduct
							}
					)
		# Filename for csv file
		current_date = pd.to_datetime('today').strftime('%Y-%m-%d %H-%M-%S')
		filename = username + '_' + current_date + '.csv'
		# Save the data into csv file
		df_result.to_csv(DATA_PATH + '/interim/' + filename, sep = ';', index = False, encoding = 'utf-8', quotechar = '"', quoting = csv.QUOTE_ALL)