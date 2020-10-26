# -*- coding: utf-8 -*-
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|r|e|d|a|n|d|g|r|e|e|n|.|c|o|.|u|k|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# ! Firefox has been used for webdriver #


import os
import json
import time

from selenium import webdriver

from scrapy.crawler import CrawlerProcess
from scrapy import Spider, Request
from scrapy.http import FormRequest
from scrapy.settings import Settings
from scrapy import Selector
from scrapy.loader import ItemLoader
from items import abcdeMbItem

from dotenv import load_dotenv
load_dotenv()

# Load sitemap & Parse with flatten_json

with open ('sitemap.json') as j:
    abcdedict = json.load(j)

def flatten_json(jsondict):
    d = {}
    l = []
    mylist = abcdedict['categories']
    for names in mylist:
        dictnames = (names['subCategories'])
        for i in dictnames:
            for k,v in i.items():
            	l.append(v)
                
    return(l)

# print("...Dict has been flattened...")
cat_codes = (flatten_json(abcdedict)[::2]) # These are the Category Codes
print(cat_codes)
time.sleep(1)
cat_names = (flatten_json(abcdedict)[1::2]) # These are the Category Names
print(cat_names)
time.sleep(1)
	
class abcdeProductList(Spider):

    name = "abcde_mb"
    custom_settings = {"FEEDS": {"abcde1.csv":{"format":"csv"}}}
    allowed_domains = ["abcde.co.uk"]
    start_urls = ['https://www.abcde.co.uk/home.aspx']
    
    try:
        os.remove("abcde1.csv")
    except OSError:
        pass
    
    def __init__(self):
    
        self.driver = webdriver.Firefox()
        
        self.driver.get('https://www.abcde.co.uk/home.aspx')
        self.driver.find_element_by_id ('OutsideHomePageControl_CustomerNumber').send_keys(os.getenv("abcde_ACCOUNT"))
        self.driver.find_element_by_id('OutsideHomePageControl_cmdCustomerNumber').click()

        time.sleep(2)
             
        self.driver.find_element_by_id ('LoginControl_EmailSingle').send_keys(os.getenv('abcde_EMAIL'))
        self.driver.find_element_by_id ('LoginControl_PasswordSingle').send_keys(os.getenv('abcde_PASSWORD'))
        self.driver.find_element_by_id('LoginControl_EnterEmailPasswordSubmit').click()
        
        self.cookie = self.driver.get_cookie("ASP.NET_SessionId")
        self.parse(response=self.driver.page_source) # This is where Selenium chanegs to Scrapy!!
        #self.driver.quit()
        
        # From here onwards Selenium hands back to Scrapy
        
    def parse(self, response):

        print('### Logged IN ###')
        
        products="https://www.abcde.co.uk/catalog/products.aspx"
        next_url = products
        
        headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': f"ASP.NET_SessionId={self.cookie['value']}",
            'Host': 'www.abcde.co.uk',
            'Referer': 'https://www.abcde.co.uk/catalog/myabcde.aspx',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
            }
                
        request = FormRequest(url=next_url, headers=headers ,callback=self.parse2)
        yield request      
             
             
    def parse2(self, response):
    
        print("\n## Now on Products Page of 24 thumbnails menu ##")
        
        etc... etc.  
