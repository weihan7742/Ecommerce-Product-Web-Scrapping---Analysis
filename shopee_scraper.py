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

    res1 = None
    res2 = None

    try:
        res1 = retrieve_product_info(browser)
    except:
        for i in range(3):
            try: 
                res1 = retrieve_product_info(browser)
            except:
                pass
            else:
                break

    try:
        res2 = retrieve_seller_info(browser)
    except:
        for i in range(3):
            try: 
                res2 = retrieve_seller_info(browser)
            except:
                pass
            else:
                break

    return res1, res2

# %%
def find_by_class(browser,class_name):
    
    res = ["n/a"]

    try:
        res = browser.find_elements_by_class_name(class_name)
    except NoSuchElementException:
        # Retry again 3 times
        count = 1
        while res == ["n/a"] and count < 3:
            time.sleep(1)
            try:
                res = browser.find_elements_by_class_name(class_name)
            except NoSuchElementException:
                count += 1

    return res

def retrieve_product_info(browser):

    # Retrieve all xpath manually 
    class_prod_name = 'attM6y'
    class_prod_rating = '_1mYa1t' # Might not exist
    class_prod_no_rating = 'OitLRu'
    class_prod_no_sold = 'aca9MM'
    class_prod_price = '_3e_UQT'
    class_prod_desc = '_3yZnxJ'

    # Handle prod_name
    prod_name = ""
    temp_prod_name = find_by_class(browser,class_prod_name)
    for item in temp_prod_name:
        prod_name += item.text

    x_rating = False
    # Handle prod_rating
    try:
        prod_rating = find_by_class(browser,class_prod_rating)[0].text
    except:
        prod_rating = "n/a"
        x_rating = True
        print("No Rating.")
        
    # Handle prod_no_rating
    if x_rating:
        prod_no_rating = "0"
    else:
        prod_no_rating = find_by_class(browser,class_prod_no_rating)[1].text

    # Handle prod_no_sold
    prod_no_sold = find_by_class(browser,class_prod_no_sold)[0].text

    prod_price = find_by_class(browser,class_prod_price)[0].text

    prod_desc = find_by_class(browser,class_prod_desc)[0].text    

    product = Product(prod_name,prod_desc,prod_price,prod_rating,prod_no_rating,prod_no_sold)

    return product    

def retrieve_seller_info(browser):

    class_sell_name = '_3uf2ae'
    class_sell_info = 'zw2E3N'

    sell_name = find_by_class(browser,class_sell_name)[0].text
    temp_sell_info = find_by_class(browser,class_sell_info)

    sell_rating = temp_sell_info[0].text
    sell_no_products = temp_sell_info[1].text
    sell_resprate = temp_sell_info[2].text
    sell_resptime = temp_sell_info[3].text
    sell_follower = temp_sell_info[4].text
    sell_joined = temp_sell_info[5].text

    seller = Seller(sell_name,sell_rating,sell_no_products,sell_resprate,sell_resptime,sell_follower,sell_joined)

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
    
    max_page = int(get_max_page(browser))

    file = open(keyword+"_shopee.csv","w",newline='',encoding='utf-8')
    header = ['prod_name','prod_desc','prod_price','prod_rating','prod_no_rating','prod_no_sold','sell_name','sell_rating','sell_no_products','sell_resprate','sell_resptime','sell_follower','sell_joined']

    with file:
        writer = csv.writer(file)
        writer.writerow(header)
        for page in range(max_page):
            print("####### Current page: " + str(page+1))
            new_url = shopee_url
            if page != 0: # Navigate to the next page
                new_url = "https://shopee.com.my/search?keyword="+keyword+"&page="+str(page)+"sortBy=relevancy"
                browser.get(new_url)
                time.sleep(3)
            for item in range(max_item): # Loop through each item
                print("Item: " + str(item+1))
                product,seller = navigate_item(browser,item+1,new_url)
                if product is not None and seller is not None:
                    writer.writerow(product.get_list()+seller.get_list())
                time.sleep(2)
                
                if seller is not None:
                    browser.back()
    
# %%
if __name__ == '__main__':
    run()

#%%
from shopee_product import Seller,Product
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import csv

test_url3 = 'https://shopee.com.my/NongShim-Shin-Ramyun-Ramen-Kimchi-Neoguri-i.62424108.5441223724'

class_prod_name = 'attM6y'
class_prod_rating = '_1mYa1t' # Might not exist
class_prod_no_rating = 'OitLRu'
class_prod_no_sold = 'aca9MM'
class_prod_price = '_3e_UQT'
class_prod_desc = '_3yZnxJ'

class_prod_x_rating = '_119xyB'

class_sell_name = '_3uf2ae'
class_sell_info = 'zw2E3N'

browser = webdriver.Chrome()
browser.get(test_url3)

time.sleep(5)

popup = browser.find_element_by_xpath('//*[@id="modal"]/div[1]/div[1]/div/div[3]/div[1]')
popup.click()

time.sleep(2)

# Handle prod_name
prod_name = ""
temp_prod_name = find_by_class(browser,class_prod_name)
for item in temp_prod_name:
    prod_name += item.text

x_rating = False
# Handle prod_rating
try:
    prod_rating = find_by_class(browser,class_prod_rating)[0].text
except:
    prod_rating = "n/a"
    x_rating = True
    
# Handle prod_no_rating
if x_rating:
    prod_no_rating = "0"
else:
    prod_no_rating = find_by_class(browser,class_prod_no_rating)[1].text

# Handle prod_no_sold
prod_no_sold = find_by_class(browser,class_prod_no_sold)[0].text

prod_price = find_by_class(browser,class_prod_price)[0].text

prod_desc = find_by_class(browser,class_prod_desc)[0].text    

product = Product(prod_name,prod_desc,prod_price,prod_rating,prod_no_rating,prod_no_sold)
print(product.get_list())

sell_name = find_by_class(browser,'_3uf2ae')[0].text
temp_sell_info = find_by_class(browser,'zw2E3N')

sell_rating = temp_sell_info[0].text
sell_no_products = temp_sell_info[1].text
sell_resprate = temp_sell_info[2].text
sell_resptime = temp_sell_info[3].text
sell_follower = temp_sell_info[4].text
sell_joined = temp_sell_info[5].text

seller = Seller(sell_name,sell_rating,sell_no_products,sell_resprate,sell_resptime,sell_follower,sell_joined)

print(seller.get_list())

# %%
