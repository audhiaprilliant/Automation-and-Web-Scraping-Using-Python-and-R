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
from src.data import data_validator as validator
# Module for monitoring
import time
from src.tools import monitor as monitor
# Module for parsing JSON
import json
# Module for csv file export
import csv
# Module for randomizer
import random

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
url = 'https://shopee.co.id/search?keyword='
# Configuration for Telegram bot
bot_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
content = requests.get("https://api.telegram.org/bot{}/getUpdates".format(bot_token))
telegram_bot = json.loads(content.content)
telegram_chatid = telegram_bot['result'][0]['message']['chat']['id']
bot_chatID = str(telegram_chatid)

# Main program
if __name__ == '__main__':
	# 1 Load the Chromedriver and get the url
	driver = webdriver.Chrome(executable_path = DRIVER_PATH, options = options)
	# 2 Load the csv file for scraping
	df = pd.read_csv(DATA_PATH + '/raw/' + sys.argv[1], sep = ';')
	product_category = pd.read_csv(DATA_PATH + '/external/product_category.csv', sep = ';')
	for index in range(len(df)):
		# 3 Determine the keyword and length
		keyword = df['keyword'][index]
		category = product_category[product_category['category'] == keyword]['subdomain'].values[0]
		maximumLength = df['length'][index]
		# 4 Concat the keyword into main URL
		query_encode = requote_uri(category.strip('').lower())
		url_query = url + query_encode
		driver.get(url_query)
		time.sleep(2)
		# 5 Add the blank list for the data
		usernameList = []
		usernameBisect = []
		reviewerList = []
		productsList = []
		statusList = []
		responsePercentageList = []
		responseCategoryList = []
		lengthofStayList = []
		followersList = []
		categoryList = []
		addressList = []
		ratingList = []
		# Randomizer
		randomizer = [i for i in range(100)]
		random.shuffle(randomizer)
		page = 0
		lengthData = 0
		# 6 Try to satisfy the length of sellers
		while lengthData < int(maximumLength):
			# Create a new URL for looping
			url_loops = url_query + '?page={}'.format(randomizer[page])
			# Access to the URL
			driver.get(url_loops)
			time.sleep(2)
			# Scroll down the page slowly
			scroll_height = driver.execute_script('return document.documentElement.scrollHeight;')
			for iters in range(0, scroll_height, 200):
				driver.execute_script('window.scrollTo(0, {});'.format(iters))
				time.sleep(1)
			# Get the div of URL
			product_list = driver.find_elements_by_class_name('row.shopee-search-item-result__items')
			# Get the URL by looping the elements
			links = product_list[0].find_elements_by_tag_name('a')
			links_list = []
			for elem in links:
				link = elem.get_attribute('href')
				links_list.append(link)
			# Loop to get the seller identity
			indexLoop = 0
			indexURL = 0
			while (lengthData + indexLoop) < int(maximumLength) and indexURL < 50:
				try:
					driver.get(links_list[indexURL])
					time.sleep(5)
					driver.execute_script('window.scrollTo(0, {});'.format(1000))
					# Username
					usernameSeller = driver.find_element_by_class_name('_3uf2ae').text
					# Check username in the list using binary search
					if validator.BinSearch(usernameBisect, usernameSeller) == False:
						print(usernameSeller, indexLoop, indexURL)
						usernameList.append(usernameSeller)
						bisect.insort(usernameBisect, usernameSeller)
						# Number of reviewers
						reviewerSeller = driver.find_elements_by_class_name('ssFdmZ')[0].find_elements_by_tag_name('span')[0].text
						reviewerList.append(reviewerSeller)
						# Number of products
						productsSeller = driver.find_elements_by_class_name('ssFdmZ')[0].find_elements_by_tag_name('span')[1].text
						productsList.append(productsSeller)
						# Chat response - percentage
						responsePercentageSeller = driver.find_elements_by_class_name('ssFdmZ')[1].find_elements_by_tag_name('span')[0].text
						responsePercentageList.append(responsePercentageSeller)
						# Chat response - category
						responseCategorySeller = driver.find_elements_by_class_name('ssFdmZ')[1].find_elements_by_tag_name('span')[1].text
						responseCategoryList.append(responseCategorySeller)
						# Length of stay
						lengthofStaySeller = driver.find_elements_by_class_name('ssFdmZ')[2].find_elements_by_tag_name('span')[0].text
						lengthofStayList.append(lengthofStaySeller)
						# Number of followers
						followersSeller = driver.find_elements_by_class_name('ssFdmZ')[2].find_elements_by_tag_name('span')[1].text
						followersList.append(followersSeller)
						# Seller's category
						categorySeller = driver.find_elements_by_class_name('aPKXeO')[0].find_elements_by_tag_name('div')[0].find_elements_by_tag_name('a')[1].text
						categoryList.append(categorySeller)
						# Seller's address
						length_element = len(driver.find_elements_by_class_name('aPKXeO'))
						addressSeller = driver.find_elements_by_class_name('aPKXeO')[length_element - 1].find_elements_by_tag_name('div')[0].text
						addressList.append(addressSeller)
						# Seller's status
						try:
							statusSeller = driver.find_element_by_class_name('SK--cp').find_elements_by_tag_name('div')[0].text
							if statusSeller == '':
								statusSeller = 'Shopee Mall'
							statusList.append(statusSeller)
						except:
							statusSeller = 'Regular'
							statusList.append(statusSeller)
						# URL into seller page
						seller_page = driver.find_element_by_class_name('btn.btn-light.btn--s.btn--inline.btn-light--link._3IQTrY')
						seller_link = seller_page.get_attribute('href')
						driver.get(seller_link)
						time.sleep(2)
						# Seller's rating
						ratingSeller = driver.find_elements_by_class_name('section-seller-overview__item-text-value')[8].text
						ratingList.append(ratingSeller)
						# Telegram notification
						message = '{cat}-{user} data is successfully scraped on {scraped_date} at {scraped_time}. Total data successfully scraped is {num}'.format(
							cat = keyword,
							user = usernameSeller,
							scraped_date = pd.to_datetime('today').strftime('%m-%d-%Y'),
							scraped_time = pd.to_datetime('today').strftime('%H:%M:%S'),
							num = len(usernameList))
						# Send text message
						send_text = 'https://api.telegram.org/bot'+bot_token+'/sendMessage?chat_id='+bot_chatID+'&parse_mode=Markdown&text='+message
						requests.get(send_text)
						time.sleep(1)
						# Dump the data into database
						df_dump = pd.DataFrame(
										{
											'Username': usernameSeller,
											'Number of Review': reviewerSeller,
											'Number of Product': productsSeller,
											'Response Chat (Percentage)': responsePercentageSeller,
											'Response Chat (Category)': responseCategorySeller,
											'Length of Stay': lengthofStaySeller,
											'Number of Follower': followersSeller,
											'Product Category': categorySeller,
											'Address': addressSeller,
											'Rating': ratingSeller,
											'Status': statusSeller,
											'Category': [keyword],
											'Page': [page]
										}
									)
						with open(DATA_PATH + '/raw/' + 'dump_data_seller.csv', 'a', newline = '') as ff:
							df_dump.to_csv(ff, header = False, sep = ';', index = False, encoding = 'utf-8', quotechar = '"', quoting = csv.QUOTE_ALL)
							ff.close()
						# Index for iteration
						indexLoop += 1
						indexURL += 1
					else:
						# Index for iteration
						indexLoop += 0
						indexURL += 1
				except:
					# Telegram notification
					message = 'WARNING! one seller - {cat} is not successfully scraped on {scraped_date} at {scraped_time}'.format(
						cat = keyword,
						scraped_date = pd.to_datetime('today').strftime('%m-%d-%Y'),
						scraped_time = pd.to_datetime('today').strftime('%H:%M:%S'))
					# Send text message
					send_text = 'https://api.telegram.org/bot'+bot_token+'/sendMessage?chat_id='+bot_chatID+'&parse_mode=Markdown&text='+message
					requests.get(send_text)
					time.sleep(1)
					# Index for iteration
					indexLoop += 0
					indexURL += 1
					continue
			# Add the page
			page += 1
			# Index for iteration
			lengthData = (lengthData + indexLoop)
		# 7 Create a dataframe
		df_result = pd.DataFrame(
						{
							'Username': usernameList,
							'Number of Review': reviewerList,
							'Number of Product': productsList,
							'Response Chat (Percentage)': responsePercentageList,
							'Response Chat (Category)': responseCategoryList,
							'Length of Stay': lengthofStayList,
							'Number of Follower': followersList,
							'Product Category': categoryList,
							'Address': addressList,
							'Rating': ratingList,
							'Status': statusList
						}
					)
		# 8 Filename for csv file
		current_date = pd.to_datetime('today').strftime('%Y-%m-%d_%H-%M-%S')
		filename = keyword + '_' + current_date + '.csv'
		# 9 Save the data into csv file
		df_result.to_csv(DATA_PATH + '/interim/' + filename, sep = ';', index = False, encoding = 'utf-8', quotechar = '"', quoting = csv.QUOTE_ALL)