#%% Import libraries and classes
from product import Seller,Product
from selenium import webdriver
from selenium.common.exceptions import *
import time
import pandas as pd

#%% Initialize global variables
keyword = "milo"
page = 0
max_page = 0
max_item = 50
shopee_url = "https://shopee.com.my/search?keyword="+keyword+"&page="+str(page)+"sortBy=relevancy"

test = '//*[@id="main"]/div/div[3]/div/div[2]/div/div[2]/div[1]'

#%%
def get_max_page(browser):
    try:
        res = browser.find_element_by_xpath('//*[@id="main"]/div/div[3]/div/div[2]/div/div[1]/div[2]/div/span[2]').text
    except:
        print("Maximum page number not found.")
        res = 0 
    
    time.sleep(0.5)

    return res

#%%
def navigate_item(browser,count):
    item_xpath = '//*[@id="main"]/div/div[3]/div/div[2]/div/div[2]/div[' + str(count) + ']'
    item = browser.find_element_by_xpath(item_xpath)
    item.click()

    time.sleep(3)

    return retrieve_product_info(browser), retrieve_seller_info(browser)

def retrieve_product_info(browser):
    pass

def retrieve_seller_info(browser):
    pass

#%% Set up and launch web browser
def run():
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
    
    max_page = get_max_page(browser)

    product,seller = navigate_item(browser,50)

    browser.back()

    # TODO Write to a csv file
    #  

    # for page in range(max_page):
    #     if page != 0:
    #         # TODO Navigate to the next page
    #         pass

    #     for item in range(max_item):
    #         # TODO Navigate and press item
    #         # TODO Retrieve item_info
    #         pass 

# %%
if __name__ == '__main__':
    run()
# %%
