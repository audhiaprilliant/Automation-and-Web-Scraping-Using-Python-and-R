
#!/usr/bin/env python
# coding: utf-8
# author: audhiaprilliant

# Module for web scraping
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# Module for data manipulation
import pandas as pd
# Import module for passing variable
import sys
# Module for file management
import os

# Configuration of Chromedriver and Knapsack Family site
DRIVER_PATH = '/home/audhi/github/Web-Scraping-Using-Python-and-R/Python/chromedriver'
options = Options()
options.add_argument('--headless')
# Local directory for saving data
dir_path = os.getcwd() + '/data'
# List of species
species_list = pd.read_csv(sys.argv[1],header = None)


if __name__ == '__main__':
    # Dataframe
    data_full = pd.DataFrame()

    # Looping
    for species in list(species_list[0]):
        driver = webdriver.Chrome(executable_path = DRIVER_PATH,options=options)
        driver.get('http://www.knapsackfamily.com/MetaboliteActivity/top.php')
        # Get the web elemnt corresponding to the targeted species (Text field)
        element_species = driver.find_elements_by_name('targetsp')[0]
        # Send value to the text input of species name
        element_species.send_keys(species)
        # Click on target species checkbox
        species_checkbox = driver.find_element_by_name('sname4')
        species_checkbox.click()
        # Clik on list button
        list_button = driver.find_element_by_name('search')
        list_button.click()
        # Switch to active tab - RESULT
        driver.switch_to.window(driver.window_handles[1])

        # Scraping data
        try:
            table = driver.find_element_by_xpath('/html/body/table[2]/tbody')
            file_data = []
            file_header = []
            # Get header column
            head_line = table.find_element_by_tag_name('tr')
            headers = head_line.find_elements_by_tag_name('th')
            for header in headers:
                header_text_byte = header.text.encode('utf-8')
                header_text_raw = header_text_byte.decode('utf-8')
                file_header.append(header_text_raw)
            file_data.append(';'.join(file_header))
            # Get rows content
            body_rows = table.find_elements_by_tag_name('tr')
            for row in body_rows:
                data = row.find_elements_by_tag_name('td')    
                file_row = []
                for datum in data:
                    datum_text_byte = datum.text.encode('utf8')
                    datum_text_raw = datum_text_byte.decode('utf-8')
                    file_row.append(datum_text_raw)
                file_data.append(';'.join(file_row))
            
            # Remove indexes which are header
            del(file_data[1:3])
            # Convert to dataframe
            data_knapsack = pd.DataFrame(columns = file_data[0].split(';'),data = [row.split(';') for row in file_data[1:]])
            
            # Get link to inspect
            elems = table.find_elements_by_tag_name('a')
            link_data = []
            for elem in elems:
                link = elem.get_attribute('href')
                link_data.append(link)
            
            # Get the species column
            species_col = [''.join(species)] * data_knapsack.shape[0]
            
            # Get the whole data
            data_knapsack.insert(loc=0,column='Species',value=species_col)
            data_knapsack_url = pd.concat([data_knapsack,pd.Series(data = link_data,name = 'Link')],axis=1)

            # Append to the data
            data_full = data_full.append(data_knapsack_url, ignore_index=True)
            data_full = pd.concat([data_full,data_knapsack_url],axis=0)

            # Chromedriver quit!            
            driver.quit()
        except:
            print('Oops!', sys.exc_info()[0], 'occurred. ', species, 'Not found!')
    
    # Save to local
    current_date = pd.to_datetime('today').strftime('%Y-%m-%d %H:%M:%S')
    data_full.to_csv(dir_path+'/'+current_date+'.csv',index=False)