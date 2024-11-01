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

options.add_argument('--disable-gpu')  # Vô hiệu hóa GPU
options.add_argument('--no-sandbox')  # Tắt sandbox
options.add_argument('--disable-dev-shm-usage')  # Giảm sử dụng bộ nhớ chia sẻ
options.add_argument('--disable-software-rasterizer') 
driver = webdriver.Chrome(service=service, options=options)

def login():
    with open('D:/Python_Project/Web-Scraping_Web-Crawling/Scraper/Selenium/config.json') as configFile:
        credentials = json.load(configFile)
    time.sleep(2)
    driver.find_element(By.XPATH, value="//a[contains(@href, '/login')]").click()    
    time.sleep(2)
    #nhập user name
    username = driver.find_element(By.CSS_SELECTOR, value="input[name='username']")
    username.clear()
    username.send_keys(credentials["USERNAME"])
    time.sleep(2)

    #login with google
    # driver.find_element(By.ID,value='google-auth-button').click()
    # Click nút submit
    driver.find_element(By.ID, value="login-submit").click()
    time.sleep(2)
    #nhập Passwords
    username = driver.find_element(By.CSS_SELECTOR, value="input[name='password']")
    username.clear()
    username.send_keys(credentials["PASSWORD"])
    time.sleep(2)
    driver.find_element(By.ID, value="login-submit").click()
    time.sleep(2)

def screenshot_Page():
    time.sleep(2)
    date_str = date.today().strftime("%d-%m-%Y")
    fpath = os.path.join(os.getcwd(), f'download\{date_str}.png')
    if not os.path.exists('download'):
        os.makedirs('download')
    driver.get_screenshot_as_file(fpath)
    print(fpath)

def main():
    try:
        # Truy cập trang chủ Trello
        driver.get('https://trello.com')
        login()
        screenshot_Page()
        input('Bot Operation Completed. Press any key...')
        driver.close()
    except Exception as e:
        print(e)
    finally:
        driver.close()
if __name__=="__main__":
    main()
    