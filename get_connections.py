from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, unicodedata

with open('./credentials') as file:
    username, password, chrome_driver = (file.read()).split()

driver = webdriver.Chrome(chrome_driver)

driver.get("https://www.linkedin.com/")

driver.implicitly_wait(6)

driver.find_element_by_xpath("""//*[@id="login-email"]""").send_keys(username)
driver.find_element_by_xpath("""//*[@id="login-password"]""").send_keys(password)
driver.find_element_by_xpath("""//*[@id="login-submit"]""").click()


# code to dropdown
# dropdown = driver.find_element_by_id("nav-settings__dropdown-trigger")
# driver.implicitly_wait(3)
# dropdown.click()

# profile = driver.find_element_by_class_name("nav-settings__member-info-container")
# driver.implicitly_wait(3)
# profile.click()

driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections/")

SCROLL_PAUSE_TIME = 0.5
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

connections = driver.find_element_by_class_name("core-rail")
html = connections.get_attribute('innerHTML')
links = []
for tags in html.split(' '):
	if "/in/" in tags:
		links.append(tags[6:-2])
#removing duplicate user profile links
user_connections = []
for i in xrange(len(links)):
	if i%2 == 0: user_connections.append(links[i])
for i in user_connections:
	print i
print len(user_connections)

print 'Work done!'
driver.close()
