#%% Import libraries and classes
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import csv

#%% Initialize global variables
keyword = "milo"
lazada_url = 'https://www.lazada.com.my/catalog/?q='+keyword+'&_keyori=ss&from=input&spm=a2o4k.home.search.go.75f82e7eBY54d3'
# %%
def run():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') 
    options.add_argument('start-maximized') 
    options.add_argument('disable-infobars')
    options.add_argument('--disable-extensions')

    # Open browser
    browser = webdriver.Chrome(options=options)
    browser.get(lazada_url)

    time.sleep(1)

    file = open(keyword+"_lazada.csv","w",newline='',encoding='utf-8')
    header = ['prod_name','prod_price']

    with file:
        writer = csv.writer(file)
        writer.writerow(header)
        titles = browser.find_elements_by_class_name('GridItem__title___8JShU')
        prices = browser.find_elements_by_class_name('GridItem__price___LY2Vk')
        for i in range(len(titles)):
            temp = []
            temp.append(titles[i])
            temp.append(prices[i])
            writer.writerow(temp)

    print("Successful")
#%%
if __name__ == '__main__':
    run()
# %%
