from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
import time 
from datetime import date
import os
import json
from selenium.webdriver.common.action_chains import ActionChains


service = Service()
options = webdriver.ChromeOptions()

options.add_argument('--disable-gpu')  # Vô hiệu hóa GPU
options.add_argument('--no-sandbox')  # Tắt sandbox
options.add_argument('--disable-dev-shm-usage')  # Giảm sử dụng bộ nhớ chia sẻ
options.add_argument('--disable-software-rasterizer') 
driver = webdriver.Chrome(service=service, options=options)
action=ActionChains(driver)

url_2='https://www.udemy.com/?utm_medium=udemyads&utm_source=vn-adwords&utm_campaign=_._c_allcategory_v.NONP_la.VN_cc.VietNam&utm_term=_._ag_branded-keywords&utm_campaign_objective=mx&gad_source=1&gclid=Cj0KCQiArby5BhCDARIsAIJvjITTj4MYgpxZktGNjoh7jIfO8L1Bgtq8eR2cBVxR9TyFF6F2B3Sr8UMaAlAMEALw_wcB'
username='test@gmail.com'
password='123456'
def udemy():
    driver.get(url_2)
    login=driver.find_element(By.XPATH,'//*[@id="__next"]/div/div/header/div[5]/a').click()


# def getcount():
#     driver.execute_script("window.open('about:blank','secondtab');")
#     driver.switch_to.window("secondtab")
#     driver.get(url)
#     time.sleep(10)
#     more=driver.find_element(By.LINK_TEXT,'More courses').click()
#     time.sleep(3)
#     item=driver.find_element(By.CLASS_NAME,'uk-link-reset')
#     item.click()
#     time.sleep(3)
#     take=driver.find_element(By.LINK_TEXT,'Take this course').click()
#     time.sleep(3)

def login_google():
    driver.get('https://www.google.com/')
    driver.find_element(By.XPATH,'//*[@id="gb"]/div/div[2]/a').click()#login
    time.sleep(4)
    username_gg=driver.find_element(By.NAME,'identifier')
    username_gg.send_keys(username)
    username_gg.send_keys(Keys.ENTER)
    time.sleep(5)
    password_gg=driver.find_element(By.TAG_NAME,'input')
    password_gg.send_keys(password)
    password_gg.send_keys(Keys.ENTER)
    time.sleep(5)
    



def main():
    try:
        
        login_google()
        input('Bot Operation Completed. Press any key...')
        driver.close()
    except Exception as e:
        print(e)
    finally:
        driver.close()
if __name__=="__main__":
    main()