from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from datetime import datetime
import time
import concurrent.futures
from tqdm import tqdm
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

NO_THREADS=5

url='https://www.python.org/'

def find_element_driver(driver):
    ele=driver.find_element(By.ID,'mainnav')#by ID 
    ele_1=driver.find_element(By.CLASS_NAME,'donate-button')#By class name
    ele_2=driver.find_element(By.XPATH,'//*[@id="touchnav-wrapper"]/header/div/div[1]/a')#By xpath
    ele_3=driver.find_element(By.LINK_TEXT,'Donate')#By link text
    ele_4=driver.find_element(By.TAG_NAME,'p')#By tag name
    ele_5=driver.find_elements(By.TAG_NAME,'div')#By tag name many element
    ele_6=driver.find_elements(By.NAME,'q')#By names
 
    print(ele_6)

def action_link(driver,action):
    button=driver.find_element(By.CLASS_NAME,'donate-button')
    action.click(on_element=button)
    action.double_click(on_element=button)
    action.click_and_hold(on_element=button)
    action.release(button)
    action.perform()

def test_navigation_link(url):
    driver.get(url)
    # find_element_driver(driver)
    action_link(driver,action)
    
    driver.close()
    # driver.quit()
    time.sleep(12)


if __name__=="__main__":
    service = Service()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    action=ActionChains(driver)
    ###########ThreadPoolExecutor
    #  with concurrent.futures.ThreadPoolExecutor(max_workers=NO_THREADS) as executor:
    #     for wkn in tqdm(range(10)):
    #         executor.submit(test_navigation_link,'https://hathanhlong2910.itch.io/roll-ball-3d')
    ###########ThreadPoolExecutor
    test_navigation_link(url)
