import requests
import re
import time
from bs4 import BeautifulSoup as bs
import urllib
from urllib.request import urlretrieve
import json
from pprint import pprint
import time as theTime
from lxml import html	
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pprint as pp
import operator
import datetime

link = "https://s5.sir.sportradar.com/bet365/en/1/season/77239/fixtures/round/21-37"
fixtures_features = {}
chrome_options = Options()  
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
print("loading page")
driver.get(link)
print("page loaded")


soup = bs(driver.page_source, features="lxml")

features = soup.findAll('div', {'class': "ff-MarketGroupFixture "})

print(features)

for feature in features:
	cotes = feature.findAll('div', {'class': "ff-MarketFixtureOdds gl-Market_General gl-Market_General-topborder gl-Market_General-pwidth100 gl-Market_General-lastinrow "})
	print(cotes)





"""
fixture = {}
fixture["cotes"] = {'3': tds[3].text, '1': tds[4].text,  '0':tds[5].text }
"""