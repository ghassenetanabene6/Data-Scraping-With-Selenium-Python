'''
install requirements on google colab

!apt-get update
!apt install chromium-chromedriver
!cp /usr/lib/chromium-browser/chromedriver /usr/bin
!pip install selenium

@Author : Ghassene Tanabene | ghassene.tanabene@gmail.com
'''

import io
import requests
import glob, os
import pandas as pd
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver',options=options)

URL = 'https://www.fsa.usda.gov/news-room/efoia/electronic-reading-room/frequently-requested-information/crop-acreage-data/index'


def download_and_unzip(url, extract_to='.'):
    
    http_response = urlopen(url)
    zipfile = ZipFile(BytesIO(http_response.read()))
    zipfile.extractall(path=extract_to)

def create_county_datasets(list_of_years):

    for year in list_of_years:
        
        try:
            driver.get(URL)
            all_a_tags = driver.find_elements(by=By.TAG_NAME, value = "a") 
            #all_zip_files_links = [elt.get_attribute('href') for elt in all_a_tags if str(elt.get_attribute('href')).endswith(".zip") and elt.text.startswith(year)]
            county_zip_files_links = [elt.get_attribute('href') for elt in all_a_tags if str(elt.get_attribute('href')).endswith(".zip") and elt.text.startswith(year) and "county" in elt.text]
            
            # Download and unzip zip files
            for url in county_zip_files_links:
                download_and_unzip(url)
                
            driver.quit()
        except:
            driver.quit()
            print("ERROR")

    for excel_file in glob.glob("*.xlsx"):
        
            #print(excel_file.split('_')[-1].replace(".xlsx",''))
            df = pd.read_excel(excel_file)
            df['Publication Date'] = excel_file.split('_')[0]       
            df.to_csv(excel_file.replace(".xlsx",'') + '.csv', index=False)
