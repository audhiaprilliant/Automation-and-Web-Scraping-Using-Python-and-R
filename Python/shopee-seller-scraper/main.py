#!/usr/bin/env python
# coding: utf-8
# author: audhiaprilliant

# Module for web scraping
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
bot_token = '1118050102:AAEtuVVsT9Es4_QC2ibIFYzzjshDnEFi5zA'
#content = requests.get("https://api.telegram.org/bot{}/getUpdates".format(bot_token))
#telegram_bot = json.loads(content.content)
#telegram_chatid = telegram_bot['result'][0]['message']['chat']['id']
#bot_chatID = str(telegram_chatid)

# Main program
if __name__ == '__main__':
	# 1 Load the Chromedriver and get the url
	driver = webdriver.Chrome(executable_path = DRIVER_PATH, options = options)
	# 2 Load the csv file for scraping
	df = pd.read_csv(DATA_PATH + '/raw/' + sys.argv[1], sep = ';')
	for index in range(len(df)):
		# 4 Determine the keyword and length
		keyword = df['keyword'][index]
		maximumLength = df['length'][index]
		# 3 Filename for csv file
		current_date = pd.to_datetime('today').strftime('%Y-%m-%d %H-%M-%S')
		filename = keyword + '_' + current_date + '.csv'
		try:
			df_seller = pd.read_csv(filename)
			usernameDataframe = list(df_seller['Username'].sort_values())
			lengthDataframe = len(df_seller)
		except:
			usernameDataframe = []
			lengthDataframe = ''
		# 2 Concat the keyword into main URL
		query_encode = requote_uri(keyword.strip('').lower())
		url_query = url + query_encode
		driver.get(url_query)
		time.sleep(2)
		# 3 Add the blank list for the data
		usernameList = []
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
		page = 0
		# 4 Try to satisfy the length of sellers
		while len(lengthDataframe) < maximumLength:
			# 4.1 Create a new URL for looping
		    url_loops = url_query + '&page={}'.format(page)
		    # 4.2 Access to the URL
		    driver.get(url_loops)
		    time.sleep(2)
		    # 4.3 Look the height of page
		    scroll_height = driver.execute_script('return document.documentElement.scrollHeight;') # Document scrollHeight
		    # 4.4 Scroll down the page slowly
		    scroll_height = driver.execute_script('return document.documentElement.scrollHeight;')
		    for iters in range(0, scroll_height, 200):
		        driver.execute_script('window.scrollTo(0, {});'.format(iters))
		        time.sleep(1)
		    # 4.5 Get the div of URL
		    product_list = driver.find_elements_by_class_name('row.shopee-search-item-result__items')
		    # 4.6 Get the URL by looping the elements
		    links = product_list[0].find_elements_by_tag_name('a')
		    for elem in links:
		        link = elem.get_attribute('href')
		        # 4.6.1 Determine the main window
		        main_window = driver.current_window_handle
		        # 4.6.2 Open a new tab
		        driver.execute_script('window.open();')
		        driver.switch_to.window(driver.window_handles[1])
		        # 4.6.3 Access the URL
		        driver.get(link)
		        time.sleep(2)
		        # 4.6.4 Get the values
	        	usernameSeller = driver.find_element_by_class_name('_3uf2ae').text
	        	if validator.BinSearch(usernameDataframe, usernameSeller) == False:
	        		# 4.6.4.1 Username
		        	bisect.insort(usernameList, usernameSeller)
			        # 4.6.4.2 Number of reviewers
			        reviewerSeller = driver.find_elements_by_class_name('ssFdmZ')[0].find_elements_by_tag_name('span')[0].text
			        reviewerList.append(reviewerSeller)
			        # 4.6.4.3 Number of products
			        productsSeller = driver.find_elements_by_class_name('ssFdmZ')[0].find_elements_by_tag_name('span')[1].text
			        productsList.append(productsSeller)
			        # 4.6.4.4 Chat response - percentage
			        responsePercentageSeller = driver.find_elements_by_class_name('ssFdmZ')[1].find_elements_by_tag_name('span')[0].text
			        responsePercentageList.append(responsePercentageSeller)
			        # 4.6.4.5 Chat response - category
			        responseCategorySeller = driver.find_elements_by_class_name('ssFdmZ')[1].find_elements_by_tag_name('span')[1].text
			        responseCategoryList.append(responseCategorySeller)
			        # 4.6.4.6 Length of stay
			        lengthofStaySeller = driver.find_elements_by_class_name('ssFdmZ')[2].find_elements_by_tag_name('span')[0].text
			        lengthofStayList.append(lengthofStaySeller)
			        # 4.6.4.7 Number of followers
			        followersSeller = driver.find_elements_by_class_name('ssFdmZ')[2].find_elements_by_tag_name('span')[1].text
			        followersList.append(followersSeller)
			        # 4.6.4.8 Seller's category
			        categorySeller = driver.find_elements_by_class_name('aPKXeO')[0].find_elements_by_tag_name('div')[0].find_elements_by_tag_name('a')[1].text
			        categoryList.append(categorySeller)
			        # 4.6.4.9 Seller's address
			        length_element = len(driver.find_elements_by_class_name('aPKXeO'))
			        addressSeller = driver.find_elements_by_class_name('aPKXeO')[length_element - 1].find_elements_by_tag_name('div')[0].text
			        addressList.append(addressSeller)
			        # 4.6.4.10 Seller's status
			        try:
			        	statusSeller = driver.find_element_by_class_name('SK--cp').find_elements_by_tag_name('div')[0].text
			        	statusList.append(statusSeller)
			        except:
			        	statusList.append('Regular')
			        # 4.6.4.11.1 URL into seller page
			        seller_page = driver.find_element_by_class_name('btn.btn-light.btn--s.btn--inline.btn-light--link._3IQTrY')
			        seller_link = seller_page.get_attribute('href')
			        # 4.6.4.11.2 Open a new tab
			        driver.execute_script('window.open();')
			        driver.switch_to.window(driver.window_handles[2])
			        driver.get(seller_link)
			        time.sleep(2)
			        # 4.6.4.11.3 Seller's rating
			        ratingSeller = driver.find_elements_by_class_name('section-seller-overview__item-text-value')[8].text
			        ratingList.append(ratingSeller)
			        # 4.6.4.11.4 Close a seller page and enter into the previous page
			        driver.close()
			        driver.switch_to.window(driver.window_handles[1])
			        driver.close()
			        driver.switch_to.window(driver.window_handles[0])
			        # 4.7 Save into csv file
			        # 4.7.1 Create a dataframe
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
			        statFile = os.path.exists(DATA_PATH + '/interim/' + filename)
			        if statFile:
			        	with open(DATA_PATH + '\\interim\\' + filename, 'a', newline = '') as ff:
			        		df_result.to_csv(ff, header = False, sep = ';', index = False, encoding = 'utf-8')
			        		ff.close()
			        else:
			        	df_result.to_csv(DATA_PATH + '/interim/' + filename, sep = ';', index = False, encoding = 'utf-8')
		        else:
		        	pass
		    # 4.7 Add the page
		    page += 1