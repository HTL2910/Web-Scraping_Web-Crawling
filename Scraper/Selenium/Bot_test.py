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
driver = webdriver.Chrome(service=service, options=options)
def main():
    try:
        driver.get('https://trello.com')
        input('Bot Operation Completed.Press any key...')
        driver.close()
    except Exception as e:
        print(e)
if __name__=="__main__":
    main()
    