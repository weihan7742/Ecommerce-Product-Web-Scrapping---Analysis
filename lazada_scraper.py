#%% Import libraries and classes
from product import Seller,Product
from selenium import webdriver
from selenium.common.exceptions import *
import pandas as pd

#%% Initialize global variables
lazada_url = ""

#%% Set up and lauunch web browser

options = webdriver.ChromeOptions()
options.add_argument('--headless') 
options.add_argument('start-maximized') 
options.add_argument('disable-infobars')
options.add_argument('--disable-extensions')

browser = webdriver.Chrome()
browser.get(lazada_url)