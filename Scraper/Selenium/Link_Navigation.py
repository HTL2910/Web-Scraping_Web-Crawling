from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from datetime import datetime
import time
import concurrent.futures
from tqdm import tqdm

NO_THREADS=5
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
     with concurrent.futures.ThreadPoolExecutor(max_workers=NO_THREADS) as executor:
        for wkn in tqdm(range(10)):
            executor.submit(test_navigation_link,'https://hathanhlong2910.itch.io/roll-ball-3d')
