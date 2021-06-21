#%% Import libraries and classes
from product import Seller,Product
from selenium import webdriver
from selenium.common.exceptions import *
import time
import pandas as pd

#%% Initialize global variables
keyword = "milo"
page = 0
shopee_url = "https://shopee.com.my/search?keyword="+keyword+"&page="+str(page)

#%% Set up and launch web browser
def launch():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') 
    options.add_argument('start-maximized') 
    options.add_argument('disable-infobars')
    options.add_argument('--disable-extensions')

    browser = webdriver.Chrome()
    browser.get(shopee_url)

    time.sleep(4)

    popup = browser.find_element_by_xpath('//*[@id="modal"]/div[1]/div[1]/div/div[3]/div[1]')
    popup.click()

    time.sleep(2)

    test = browser.find_element_by_xpath('//*[@id="main"]/div/div[3]/div/div[2]/div/div[2]/div[50]')
    test.click()

# %%
