import calendar, csv
import os
import platform
import sys
import urllib

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
driver = None

download_uploaded_photos = True
download_friends_photos = True

friends_small_size = True
photos_small_size = True

total_scrolls = 5000
current_scrolls = 0
scroll_time = 5

old_height = 0


def check_height():
    new_height = driver.execute_script("return document.body.scrollHeight")
    return new_height != old_height


def scroll():
    global old_height
    current_scrolls = 0

    while (True):
        try:
            if current_scrolls == total_scrolls:
                return

            old_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            WebDriverWait(driver, scroll_time, 0.05).until(lambda driver: check_height())
            current_scrolls += 1
        except TimeoutException:
            break

    return

def extract_and_write_posts(elements, filename):
    try:
        f = open(filename, "a", newline='\r\n')
        print (elements)
        f.writelines(elements)
    except: pass

def save_to_file(name, elements, status, current_section):

    try:
        f = None  # file pointer
        results = []
        img_names = []
        extract_and_write_posts(elements, name)
        return

    except:
        print("Exception (save_to_file)", "Status =", str(status), sys.exc_info()[0])

    return

def scrap_data(id, scan_list, section, elements_path, save_status, file_names):
    page = []

    if save_status == 4:
        page.append(id)

    for i in range(len(section)):
        page.append(id + section[i])

    for i in range(len(file_names)):

        driver.get(page[i])

        if save_status != 3:
            scroll()

        data = driver.find_elements_by_xpath(elements_path[i])
        for d in data:
            x = d.text.split('\n')
            s = ''
            for j in x[:-7]: s+=str(j.encode("utf-8"))
            s+='\n'
            print (file_names[i])
            file = open(file_names[i], "a")
            file.write(s)

def create_original_link(url):
    if url.find(".php") != -1:
        original_link = "https://en-gb.facebook.com/" + ((url.split("="))[1])

        if original_link.find("&") != -1:
            original_link = original_link.split("&")[0]

    elif url.find("fnr_t") != -1:
        original_link = "https://en-gb.facebook.com/" + ((url.split("/"))[-1].split("?")[0])
    elif url.find("_tab") != -1:
        original_link = "https://en-gb.facebook.com/" + (url.split("?")[0]).split("/")[-1]
    else:
        original_link = url

    return original_link

def scrap_profile(ids):
    folder = os.path.join(os.getcwd(), "Data")

    if not os.path.exists(folder):
        os.mkdir(folder)

    os.chdir(folder)

    for id in ids:

        driver.get(id)
        url = driver.current_url
        id = create_original_link(url)

        print("\nScraping:", id)

        try:
            if not os.path.exists(os.path.join(folder, id.split('/')[-1])):
                os.mkdir(os.path.join(folder, id.split('/')[-1]))
            else:
                print("A folder with the same profile name already exists."
                      " Kindly remove that folder first and then run this code.")
                continue
            os.chdir(os.path.join(folder, id.split('/')[-1]))
        except:
            print("Some error occurred in creating the profile directory.")
            continue

        scan_list = ["posts"]
        section = []
        elements_path = ["//div[@class='_4-u2 mbm _4mrt _5jmm _5pat _5v3q _4-u8']"]

        file_names = ["Posts.txt"]
        save_status = 4

        scrap_data(id, scan_list, section, elements_path, save_status, file_names)
        print("Posts(Statuses) Done")

    return

def login(email, password):
    try:
        global driver
        options = Options()

        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--mute-audio")

        try:
            if platform.system() == 'Linux':
                driver = webdriver.Chrome(executable_path="./chromedriver", chrome_options=options)
            else:
                driver = webdriver.Chrome(executable_path="./chromedriver.exe", chrome_options=options)
        except:
            print("Kindly replace the Chrome Web Driver with the latest one from"
                  " http://chromedriver.chromium.org/downloads")
            exit()

        driver.get("https://en-gb.facebook.com")
        driver.maximize_window()

        driver.find_element_by_name('email').send_keys(email)
        driver.find_element_by_name('pass').send_keys(password)

        driver.find_element_by_id('loginbutton').click()

    except Exception as e:
        print("There's some error in log in.")
        print(sys.exc_info()[0])
        exit()

def main():
    ids = ["https://en-gb.facebook.com/" + line.split("/")[-1] for line in open("input.txt", newline='\n')]

    if len(ids) > 0:
        email = "enchantedpudding@gmail.com"
        password = "Walter@1000"

        print("\nStarting Scraping...")

        login(email, password)
        scrap_profile(ids)
        driver.close()
    else:
        print("Input file is empty..")

main()
