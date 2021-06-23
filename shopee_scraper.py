#%% Import libraries and classes
from shopee_product import Seller,Product
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import csv

#%% Initialize global variables
keyword = "shin ramen"
start_page = 0
max_page = 0
max_item = 50
shopee_url = "https://shopee.com.my/search?keyword="+keyword+"&page="+str(start_page)+"sortBy=relevancy"

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
def navigate_item(browser,count,url):
    scroll_down(browser)

    item_xpath = '//*[@id="main"]/div/div[3]/div/div[2]/div/div[2]/div[' + str(count) + ']'
    try:
        item = browser.find_element_by_xpath(item_xpath)
        item.click()
    except:
        success = False
        # Retry
        for i in range(3):
            try:
                browser.get(url)
                time.sleep(3)
                scroll_down(browser)

                item = browser.find_element_by_xpath(item_xpath)
                item.click()
            except:
                pass
            else:
                success = True
                break
        
        if not success:
            print("Item " + str(count) + " failed.")
            browser.get(url)
            return None,None

    time.sleep(3)

    return retrieve_product_info(browser), retrieve_seller_info(browser)

def find_element(browser,element_xpath):

    res = ""

    try:
        res = browser.find_element_by_xpath(element_xpath).text
    except NoSuchElementException:
        # Retry again 5 times
        count = 1
        while res == "" and count < 5:
            time.sleep(1)
            try:
                res = browser.find_element_by_xpath(element_xpath)
            except NoSuchElementException:
                count += 1 
    return res 

def find_sell_element(browser,first,second):
    res = ""

    sell_count = 1

    element_xpath = first+str(sell_count)+second
    try:
        res = browser.find_element_by_xpath(element_xpath).text
    except NoSuchElementException:
        while res == "" and sell_count < 5:
            time.sleep(1)
            sell_count += 1
            element_xpath = first+str(sell_count)+second
            try:
                res = browser.find_element_by_xpath(element_xpath)
            except NoSuchElementException:
                pass
    
    return res

def retrieve_product_info(browser):

    # Retrieve all xpath manually 
    prod_name_xpath = '//*[@id="main"]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[1]/span'
    prod_desc_xpath = '//*[@id="main"]/div/div[2]/div[2]/div[2]/div[3]/div[2]/div[1]/div[1]/div[2]/div[2]/div/span'
    prod_rating_xpath = '//*[@id="main"]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[2]/div[1]/div[1]'
    prod_no_rating_xpath = '//*[@id="main"]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[2]/div[2]/div[1]'
    prod_no_sold_xpath = '//*[@id="main"]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[2]/div[3]/div[1]'
    prod_pref_xpath = '//*[@id="main"]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[1]/div'

    # Scrape data
    prod_name = find_element(browser,prod_name_xpath)
    prod_desc = find_element(browser,prod_desc_xpath)
    prod_rating = find_element(browser,prod_rating_xpath)

    # Do not add product with no rating
    if prod_rating == "":
        return None

    prod_no_rating = find_element(browser, prod_no_rating_xpath)
    prod_no_sold = find_element(browser, prod_no_sold_xpath)

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

    sell_name_first = '//*[@id="main"]/div/div[2]/div[2]/div[2]/div[3]/div['


    sell_name_xpath = ']/div[1]/div/div[1]'
    sell_rating_xpath = ']/div[2]/div[1]/div/span'
    sell_prod_xpath = ']/div[2]/div[1]/a/span'
    sell_resprate_xpath = ']/div[2]/div[2]/div[1]/span'
    sell_resptime_xpath = ']/div[2]/div[2]/div[2]/span'
    sell_follower_xpath = ']/div[2]/div[3]/div[2]/span'
    sell_joined_xpath = ']/div[2]/div[3]/div[1]/span'


    # Assign data to variables
    sell_name = find_sell_element(browser,sell_name_first,sell_name_xpath)
    sell_rating = find_sell_element(browser,sell_name_first,sell_rating_xpath)
    sell_prod = find_sell_element(browser,sell_name_first,sell_prod_xpath)
    sell_resprate = find_sell_element(browser,sell_name_first,sell_resprate_xpath)
    sell_resptime = find_sell_element(browser,sell_name_first,sell_resptime_xpath)
    sell_follower = find_sell_element(browser,sell_name_first,sell_follower_xpath)
    sell_joined = find_sell_element(browser,sell_name_first,sell_joined_xpath)
    
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

    browser = webdriver.Chrome(options=options)
    browser.get(shopee_url)

    time.sleep(4)

    popup = browser.find_element_by_xpath('//*[@id="modal"]/div[1]/div[1]/div/div[3]/div[1]')
    popup.click()

    time.sleep(2)
    
    max_page = int(get_max_page(browser))

    file = open(keyword+"_shopee.csv","w",newline='',encoding='utf-8')
    header = ['prod_name','prod_desc','prod_rating','prod_no_rating','prod_no_sold','prod_pref','sell_name','sell_rating','sell_no_products','sell_resprate','sell_resptime','sell_follower','sell_joined']

    with file:
        writer = csv.writer(file)
        writer.writerow(header)
        for page in range(max_page):
            new_url = shopee_url
            if page != 0: # Navigate to the next page
                new_url = "https://shopee.com.my/search?keyword="+keyword+"&page="+str(page)+"sortBy=relevancy"
                browser.get(new_url)
                time.sleep(3)
            for item in range(max_item): # Loop through each item
                print(item+1)
                product,seller = navigate_item(browser,item+1,new_url)
                if product is not None:
                    writer.writerow(product.get_list()+seller.get_list())
                time.sleep(2)
                
                if seller is not None:
                    browser.back()
    
# %%
if __name__ == '__main__':
    run()

# %%
