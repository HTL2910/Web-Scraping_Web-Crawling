from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
import time 
from datetime import date
import os
import json

service = Service()
options = webdriver.ChromeOptions()
url='https://www.instagram.com/'
USERNAME='arhaskjkdkah'
PASSWORD='aaassdad'
class InstagramBot:
    def __init__(self):
        self.driver=webdriver.Chrome(service=service, options=options)
    
    def login(self):
        self.driver.get(url)
        time.sleep(5)

        username=self.driver.find_element(By.NAME,'username')
        password=self.driver.find_element(By.NAME,'password')
        login_button=self.driver.find_element(By.XPATH,'//*[@id="loginForm"]/div/div[3]/button')
        username.send_keys(USERNAME)
        password.send_keys(PASSWORD)
        time.sleep(5)
        login_button.click()

        time.sleep(5)
        self.driver.quit()

if __name__=="__main__":
    bot=InstagramBot()
    bot.login()