import os
import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup

# loading variables from .env file
load_dotenv()

# CONSTANT 
TARGET_URL = os.getenv("TARGET_URL")
USERNAME = os.getenv("USERNAME")
PASS = os.getenv("PASS")
grad_link = f"https://{USERNAME}:{PASS}@www2.cpce-polyu.edu.hk/cpce/Graduation_2023/";
# CONSTANT


# init webdriver
options = webdriver.ChromeOptions()
options.add_argument("--headless=new") # No UI pops up
chrome_driver = webdriver.Chrome(options=options)

# get to the website
chrome_driver.get(url=grad_link)

def display_page_content(driver):
    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")
    print(soup)

for i in range(1, 6):
    targer_folder_path = os.path.abspath(os.path.join('.' '/downloads', f'Session {i}'))
    if not os.path.exists(targer_folder_path):
        os.makedirs(targer_folder_path)
    chrome_driver.find_element(By.PARTIAL_LINK_TEXT, f"Session {i}").click() # Enter each session
    chrome_driver.find_element(By.LINK_TEXT, "All").click()  # Switch to display all photo
    galleries = chrome_driver.find_elements(By.CLASS_NAME, 'gallery')
    for gallery in galleries:
        a_tags = chrome_driver.find_elements(By.XPATH, '//ul/li/a')
        for a_tag in a_tags:
            img_link = a_tag.get_attribute('href')
            file_name_with_ext = img_link.split('/')[-1].replace("%20", " ") # extract the file name from src and replace %20 with actual space
            r = requests.get(img_link, auth=HTTPBasicAuth(USERNAME, PASS))
            full_targer_folder_path = f"{targer_folder_path}/{file_name_with_ext}"
            with open(full_targer_folder_path, 'wb') as file:
                print("Downloading", file_name_with_ext)
                file.write(r.content)
    #display_page_content(chrome_driver) #debug only
    chrome_driver.back()
    chrome_driver.back()
