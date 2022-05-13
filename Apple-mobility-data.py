'''
install requirements on google colab

!apt-get update
!apt install chromium-chromedriver
!cp /usr/lib/chromium-browser/chromedriver /usr/bin
!pip install selenium

@Author : Ghassene Tanabene | ghassene.tanabene@gmail.com
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver',options=options)

URL = 'https://covid19.apple.com/mobility'

def download_csv_file(csv_url, fileName):

    req = requests.get(csv_url)
    url_content = req.content
    csv_file = open(fileName, 'wb')
    csv_file.write(url_content)
    csv_file.close()

def scrape_csv_file():

    try:
        driver.get(URL)
        all_a_tags = driver.find_elements(by=By.TAG_NAME, value = "a")
        links = [elt.get_attribute('href') for elt in all_a_tags]
        
        for link in links: 
            if link.endswith(".csv"):
                csv_url = link
        if csv_url:
            download_csv_file(csv_url, 'Apple-mobility-data.csv')
        driver.quit()
    except:
        driver.quit()
        print("ERROR")

def create_new_dataframe():

    # Scraping data
    scrape_csv_file()

    df = pd.read_csv('Apple-mobility-data.csv',index_col=False)

    # Dataframe preprocessing 
    new_df = df.melt(id_vars=["geo_type", "region", "transportation_type", "alternative_name", "sub-region", "country"], 
            var_name="Date", 
            value_name="Value")
        
    return new_df

#my_df = create_new_dataframe()
#my_df.to_csv("new_dataset.csv", index=False)
