from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from datetime import datetime
import time
def test_navigation_link(url):
    
    service = Service()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    driver.quit()
    # driver=webdriver.Chrome()
    time.sleep(12)
    # driver.get(url)

if __name__=="__main__":
   test_navigation_link('https://hathanhlong2910.itch.io/roll-ball-3d')