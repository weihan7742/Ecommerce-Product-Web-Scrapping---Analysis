#%% Import libraries and classes
from product import Seller,Product
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
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
def scroll_down(driver):
    count = 0 
    html = driver.find_element_by_tag_name('html')
    while count < 5:
        html.send_keys(Keys.PAGE_DOWN)
        count += 1
        time.sleep(1)
#%%
def get_max_page(browser):
    try:
        res = browser.find_element_by_xpath('//*[@id="main"]/div/div[3]/div/div[2]/div/div[1]/div[2]/div/span[2]').text
    except:
        print("Maximum page number not found.")
        res = 0 
    
    return res

#%%
def navigate_item(browser,count):
    scroll_down(browser)

    item_xpath = '//*[@id="main"]/div/div[3]/div/div[2]/div/div[2]/div[' + str(count) + ']'
    item = browser.find_element_by_xpath(item_xpath)
    item.click()

    time.sleep(3)

    return retrieve_product_info(browser), retrieve_seller_info(browser)

def retrieve_product_info(browser):

    # Retrieve all xpath manually 
    prod_name_xpath = '//*[@id="main"]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[1]/span'
    prod_desc_xpath = '//*[@id="main"]/div/div[2]/div[2]/div[2]/div[3]/div[2]/div[1]/div[1]/div[2]/div[2]/div/span'
    prod_rating_xpath = '//*[@id="main"]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[2]/div[1]/div[1]'
    prod_no_rating_xpath = '//*[@id="main"]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[2]/div[2]/div[1]'
    prod_no_sold_xpath = '//*[@id="main"]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[2]/div[3]/div[1]'
    prod_pref_xpath = '//*[@id="main"]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[1]/div'

    prod_xrating_xpath = '//*[@id="main"]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[2]/div[1]' # if product has no rating

    # Scrape data
    prod_name = browser.find_element_by_xpath(prod_name_xpath).text
    prod_desc = browser.find_element_by_xpath(prod_desc_xpath).text

    # Handle items with no ratings
    got_rating = True

    try:
        prod_rating = browser.find_element_by_xpath(prod_rating_xpath).text
    except:
        prod_rating = None
        got_rating = False

    if got_rating:
        prod_no_sold = browser.find_element_by_xpath(prod_no_sold_xpath).text
        prod_no_rating = browser.find_element_by_xpath(prod_no_rating_xpath).text
    else: 
        prod_no_sold = browser.find_element_by_xpath(prod_no_rating_xpath).text
        prod_no_rating = '0'

    # Retrieved preferred
    try:
        prod_pref = browser.find_element_by_xpath(prod_pref_xpath).text
    except:
        prod_pref = False # Does not exist
    else:
        prod_pref = True # Exist

    # Compile all info into Product object
    product = Product(prod_name,prod_desc,prod_rating,prod_no_rating,prod_no_sold,prod_pref)

    return product    

def retrieve_seller_info(browser):

    # Retrieve all xpath manually
    sell_name_xpath = '//*[@id="main"]/div/div[2]/div[2]/div[2]/div[3]/div[1]/div[1]/div/div[1]'
    sell_rating_xpath = '//*[@id="main"]/div/div[2]/div[2]/div[2]/div[3]/div[1]/div[2]/div[1]/div/span'
    sell_prod_xpath = '//*[@id="main"]/div/div[2]/div[2]/div[2]/div[3]/div[1]/div[2]/div[1]/a/span'
    sell_resprate_xpath = '//*[@id="main"]/div/div[2]/div[2]/div[2]/div[3]/div[1]/div[2]/div[2]/div[1]/span'
    sell_resptime_xpath = '//*[@id="main"]/div/div[2]/div[2]/div[2]/div[3]/div[1]/div[2]/div[2]/div[2]/span'
    sell_follower_xpath = '//*[@id="main"]/div/div[2]/div[2]/div[2]/div[3]/div[1]/div[2]/div[3]/div[2]/span'
    sell_joined_xpath = '//*[@id="main"]/div/div[2]/div[2]/div[2]/div[3]/div[1]/div[2]/div[3]/div[1]/span'


    # Assign data to variables
    sell_name = browser.find_element_by_xpath(sell_name_xpath).text
    sell_rating = browser.find_element_by_xpath(sell_rating_xpath).text
    sell_prod = browser.find_element_by_xpath(sell_prod_xpath).text
    sell_resprate = browser.find_element_by_xpath(sell_resprate_xpath).text
    sell_resptime = browser.find_element_by_xpath(sell_resptime_xpath).text
    sell_follower = browser.find_element_by_xpath(sell_follower_xpath).text
    sell_joined = browser.find_element_by_xpath(sell_joined_xpath).text

    
    # Compile all info into Seller object
    seller = Seller(sell_name,sell_rating,sell_prod,sell_resprate,sell_resptime,sell_follower,sell_joined)

    return seller

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

    product,seller = navigate_item(browser,30)

    print(product.get_list())
    print(seller.get_list())

    time.sleep(10)
    
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
