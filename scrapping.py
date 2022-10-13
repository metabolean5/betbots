#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "mpdev"
__copyright__ = "Copyright 2022, Turfutoday's Betbots"
__license__ = "CC BY-SA 2.0 FR"
__email__ = "turfutoday@turfutoday.com"

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
import pandas as pd
import pprint as pp
import operator
import datetime




def scrap_fixtures_01(fixtures):

	fixtures_features = {}
	chrome_options = Options()  
	chrome_options.add_argument("--headless")
	driver = webdriver.Chrome(options=chrome_options)
	driver.get(fixtures)
	time.sleep(1)

	soup = bs(driver.page_source, features="lxml")

	table = soup.findAll('table', {'class': "table"})

	trs = table[0].findAll("tr")
	roundnum = trs[1].text

	fixtures_features[roundnum] = [] 

	i = 0
	for tr in trs[3:]:

		tds = tr.findAll('td')

		fixture = {}
		fixture["cotes"] = {'3': tds[3].text, '1': tds[4].text,  '0':tds[5].text }

		info = tds[2].findAll('div', {'class': "col-xs-5 "})

		fixture["info"] = {"teams" :tds[2].text.split(".")[0][:-1]}

		#fixture["info"] = {"Home Team" : }

		xpath = "/html/body/div[1]/div/div/div/div[4]/div/div/div/div/div[2]/div/div/div/table/tbody/tr["+str(i+3)+"]"

		driver.find_element('xpath',xpath).click() #accessing head to head feature
		time.sleep(2)
		print(driver.current_url)
		soup = bs(driver.page_source, features="lxml")
		perfs = soup.findAll('div', {'class': "row margin-top-medium"})
		try:
			svg = perfs[0].findAll('svg', {'class': "margin-center"})
			scores_vector = []
		except:
			print("continue")
			driver.get(fixtures)
			time.sleep(1)
			i+=1

			continue

		date = soup.findAll('div', {'class': "col-xs-12"}) 

		fixture["info"]["date"] = date[3].text

		j = 0
		while j<2: ##getting last 5 matches (latest to the starting from the left)
			k=0
			for score in svg:
				if score.text == "W":
					scores_vector.append(3)
				if score.text == "L":
					scores_vector.append(0)
				if score.text == "D":
					scores_vector.append(1)

				k+=1
				if k >= 5: break

			svg = perfs[1].findAll('svg', {'class': "margin-center"})
			j+=1

		fixture["last5vec"] = scores_vector
		print(fixture)
		
		if len(scores_vector) <= 0: #in case match already took place, bet365 does not provide teams history => fucks up the betting strategies later n
			print("Match already took place")
			driver.get(fixtures)
			time.sleep(1)
			i+=1
			continue

		fixtures_features[roundnum].append(fixture)

		driver.get(fixtures)
		time.sleep(1)
		
		i+=1 #incremt for xpath h2h method (accessing each feature page for all fixtures)


	print(fixtures_features)
	return fixtures_features


	driver.quit()


def betSuccess(bet,betkey ,urlround):

	fixtures_features = {}
	chrome_options = Options()  
	chrome_options.add_argument("--headless")
	driver = webdriver.Chrome(options=chrome_options)
	url = str("https://s5.sir.sportradar.com/bet365/en/1/season/94211/fixtures/")+ urlround
	driver.get(url)
	print(url)

	time.sleep(1)

	soup = bs(driver.page_source, features="lxml")
	table = soup.findAll('table', {'class': "table"})
	trs = table[0].findAll("tr")
	roundnum = trs[1].text

	betindex =  0
	for t in trs[3:]:#iterate through table to find correct betkey

		tds = t.findAll('td')
		score = tds[7].text.split(":")

		if betindex == int(betkey) and score[0] != "FT":
			tr = t
			break

		if score[0] == "FT":
			continue
		else:
			betindex+=1


	tds = tr.findAll('td')

	score = tds[7].text.split(":")	

	print(score)

	if len(score) <= 1:
		return False

	truth = ""
	if int(score[0]) > int(score[2]):
		truth = '3'
	elif int(score[0]) == int(score[2]):
		truth = '1'
	else:
		truth = '0'

	print(tds[7].text)
	print(truth)
	print(bet['bet_data']["prediction"])

	if int(bet['bet_data']["prediction"]) == int(truth):
		return True
	else:
		return False


def printClassification(botlist):

	botdic = {}
	for bot in botlist:
		botdic[bot.getName()] = {"money":bot.getMemory()["money"],"successful bets" : bot.getMemory()["successful_bets"], "failed bets": bot.getMemory()["unsuccessful_bets"]}


	#sorted_x = sorted(botdic.items(), key=operator.itemgetter(1), reverse=True)

	df = pd.DataFrame(botdic).T
	df = df.sort_values(by=['money'])
	df = df[::-1]


	htmlfile = open("betbot.html", 'a')

	htmltable = df.to_html(classes='redTable')
	htmlfile.write("<p></p>")
	htmlfile.write(htmltable)
	htmlfile.close()



	'''
	print("BOT\t\tMONEY\t\tSUCCESSFUL BETS\t\tFAILED BETS\t\tTOTAL BETS")
	for ele1,ele2 in sorted_x:
		print(ele1+"\t"+str(ele2[0])+"\t"+str(ele2[1])+"\t"+str(ele2[2])+"\t"+str(ele2[3]))
	'''

