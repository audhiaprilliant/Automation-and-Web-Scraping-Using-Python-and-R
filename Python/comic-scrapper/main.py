# Web scraping
from selenium import webdriver
from selenium.webdriver.common.by import By
# Dropdown selector
from selenium.webdriver.support.ui import Select
# Set a timeout
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Access website
import urllib
# Data manipulation
import pandas as pd
# Regular expression
import re
import string
# File management
import os
# Parse JSON
import json
# Timing
import time
# Parser
import sys

# Declare webdriver
driver = webdriver.Edge()

# Main url
url = 'https://readcomiconline.li/Comic/101-Ways-to-End-the-Clone-Saga'

# Waiting time
max_wait_time = 10

# Access to main url
driver.get(url)
# Wait for the presence of a specific element
WebDriverWait(driver, max_wait_time).until(EC.presence_of_element_located((By.CLASS_NAME, 'bigChar')))
# Status log
print('Comic page is opened successfully')

## Core Procedure

### 0 Comic identity
comic_id = {
    'title': None,
    'chapter': []
    }

### 1 Get comic title
# Get comic title and its abbreviation
comic_title = re.sub(pattern = r'[^\w\s]', repl = '', string = driver.find_element(By.CLASS_NAME, 'bigChar').text)
if len(comic_title) > 5:
    comic_abbrv = ''.join(e[0] for e in comic_title.split())
else:
    comic_abbrv = comic_title
# Update comic identity
comic_id['title'] = comic_title
# Create folder of comic
comic_main_dir = os.path.join('data', comic_title)
os.mkdir(comic_main_dir)
# Status log
print('Get comic title')

### 2 Get URLs for each chapter
# Element of table
table_chapter = driver.find_element(By.TAG_NAME, 'table')
# List of chapter name
list_chapter = reversed([{element.text: element.get_property('href')} for element in table_chapter.find_elements(By.TAG_NAME, 'a')])
# Status log
print('Get list of comic chapters')

### 3 Open each URL
for idx, chapter in enumerate(list_chapter):
    # Chapter name and chapter url
    chapter_name, chapter_url = re.sub(pattern = r'[^\w\s]', repl = '', string = list(chapter.keys())[0]), list(chapter.values())[0]

    # Create subfolder of comic
    comic_main_subdir = os.path.join(comic_main_dir, chapter_name)
    os.mkdir(comic_main_subdir)
    # Update comic identity
    comic_id['chapter'].append({chapter_name: {'url': chapter_url}})
    # Access chapter page
    driver.get(chapter_url)
    # Wait for the presence of a specific element
    WebDriverWait(driver, max_wait_time).until(EC.presence_of_element_located((By.ID, 'divImage')))
    # Status log
    print('Comic chapter {t} is opened successfully'.format(t = chapter_name))

    ### 4 Switch read mode to full page
    # Dropdown object
    dropdown_obj = Select(driver.find_element(By.ID, 'selectReadType'))
    # List of dropdown list
    dropdown_values = []
    options = dropdown_obj.options
    for index in range(len(options)):
        dropdown_values.append(options[index].text)
    # Select by visible text
    dropdown_obj.select_by_visible_text(dropdown_values[len(dropdown_values) - 1])

    ### 5 Scroll down page
    # Document scrollHeight
    scroll_height = driver.execute_script('return document.documentElement.scrollHeight;')
    # Status log
    print('Start scrolling down the comic page')
    # Scroll down slowly
    scroll_height = driver.execute_script('return document.documentElement.scrollHeight;')
    for iters in range(0, scroll_height, 1000):
        driver.execute_script('window.scrollTo(0, {});'.format(iters))
        time.sleep(1)
    # Status log
    print('Finish scrolling down the comic page')
    
    ### 6 Download the images
    # Image section object
    image_obj = driver.find_element(By.ID, 'divImage')
    # List of images
    list_images = [{comic_abbrv + '-' + str(idx) + '-' + str(i): j.get_attribute('src')} for i, j in enumerate(image_obj.find_elements(By.TAG_NAME, 'img'))]
    # Update comic identity
    l = [list(key.keys())[0] for key in comic_id['chapter']]
    idx_chapter = l.index(chapter_name)
    comic_id['chapter'][idx_chapter][chapter_name]['images'] = {'list_images': list_images, 'total_images': len(list_images)}

    # Status log
    print('Start downloading the images')
    for image in list_images:
        # URL
        image_url = image[list(image.keys())[0]]

        # Object name
        image_name = list(image.keys())[0] + '.jpg'

        # Download the image
        urllib.request.urlretrieve(url = image_url, filename = os.path.join(comic_main_subdir, image_name))
    # Status log
    print('Download is completed\n')

# Store comic identity
with open(comic_main_dir + '/' + comic_abbrv + '.json', 'w') as f:
    json.dump(comic_id, f)