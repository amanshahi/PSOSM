from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, unicodedata, sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

with open('./credentials') as file:
    username, password, chrome_driver = (file.read()).split()

driver = webdriver.Chrome(chrome_driver)

driver.get("https://www.linkedin.com/")

driver.implicitly_wait(6)

driver.find_element_by_xpath("""//*[@id="login-email"]""").send_keys(username)
driver.find_element_by_xpath("""//*[@id="login-password"]""").send_keys(password)
driver.find_element_by_xpath("""//*[@id="login-submit"]""").click()

actions = ActionChains(driver)

with open('./users') as users:
	all_users = users.read().split('\n')

for i in all_users:
	driver.get("https://www.linkedin.com" + i)
	driver.implicitly_wait(5)
	while 1:
		driver.execute_script("window.scrollBy(0,250);")
		try:
			experience = driver.find_element_by_id("experience-section")
			exp_html = experience.get_attribute('innerHTML')
			break
		except:
			pass
	while 1:
		driver.execute_script("window.scrollBy(0,150);")
		try:
			education = driver.find_element_by_id("education-section")
			edu_html = education.get_attribute('innerHTML')
			break
		except:
			pass

	from bs4 import BeautifulSoup

	exp_soup  = BeautifulSoup(exp_html, 'html.parser')
	edu_soup =  BeautifulSoup(edu_html, 'html.parser')
	exp = []
	for i in exp_soup.findAll('div', {'class': 'pv-entity__summary-info'}):
		temp = []
		temp.append(i.findAll('h3', {'class': 'Sans-17px-black-85%-semibold'})[0].encode_contents())
		temp.append(i.findAll('span', {'class': 'pv-entity__secondary-title'})[0].encode_contents())
		exp.append(temp)
	print exp

	edu = []
	for i in edu_soup.findAll('div', {'class': 'pv-entity__degree-info'}):
		temp, info = [], []
		temp.append(i.findAll('h3', {'class': 'pv-entity__school-name'})[0].encode_contents())
		for j in i.findAll('span', {'class':'pv-entity__comma-item'}):
			info.append(j.encode_contents())
		temp.append(''.join(info))
		edu.append(temp)
	print edu
