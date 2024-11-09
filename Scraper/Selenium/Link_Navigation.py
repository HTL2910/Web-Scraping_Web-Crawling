from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from datetime import datetime
import time
import concurrent.futures
from tqdm import tqdm
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

NO_THREADS=5

url='https://www.python.org/'

def find_element_driver(driver):
    driver = webdriver.Chrome(service=service, options=options)
    ele=driver.find_element(By.ID,'mainnav')#by ID 
    ele_1=driver.find_element(By.CLASS_NAME,'donate-button')#By class name
    ele_2=driver.find_element(By.XPATH,'//*[@id="touchnav-wrapper"]/header/div/div[1]/a')#By xpath
    ele_3=driver.find_element(By.LINK_TEXT,'Donate')#By link text
    ele_4=driver.find_element(By.TAG_NAME,'p')#By tag name
    ele_5=driver.find_elements(By.TAG_NAME,'div')#By tag name many element
    ele_6=driver.find_elements(By.NAME,'q')#By names
 
    print(ele_6)

def action_link(driver):
    # button=driver.find_element(By.CLASS_NAME,'donate-button')
    # btn=driver.find_element(By.LINK_TEXT,'Downloads')
    search=driver.find_element(By.ID,'id-search-field')
    action=ActionChains(driver)
    # action.click(on_element=button)
    # action.double_click(on_element=button)
    # action.click_and_hold(on_element=button)
    # action.release(button)
    # action.move_by_offset(100,10)
    # action.move_to_element(to_element=button)
    # action.move_to_element_with_offset(btn,150,0).click()

    # action.key_down('p',search)
    
    # action.key_up('a',search)
    # action.click(search).send_keys('python a')
    # action.reset_actions()
    action.perform()

def test_navigation_link(url):
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    # find_element_driver(driver)
    action_link(driver)
    
    time.sleep(12)
    driver.close()
    driver.quit()
   


if __name__=="__main__":
    service = Service()
    options = webdriver.ChromeOptions()
    
    
    
    ###########ThreadPoolExecutor
    #  with concurrent.futures.ThreadPoolExecutor(max_workers=NO_THREADS) as executor:
    #     for wkn in tqdm(range(10)):
    #         executor.submit(test_navigation_link,'https://hathanhlong2910.itch.io/roll-ball-3d')
    ###########ThreadPoolExecutor
    test_navigation_link(url)
