from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import csv
import re
import pandas as pd
import pyperclip
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
options = Options()
options.add_argument('--headless')  # Chạy không hiển thị giao diện
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument(f'user-agent={USER_AGENT}')
options.add_argument('--enable-unsafe-swiftshader')

service = Service() 
driver = webdriver.Chrome(service=service, options=options)
def get_link_to_file(id):
    url = f"https://koyo.jtekt.co.jp/en/products/detail/?pno={id}"
    driver.get(url)
    time.sleep(1) 
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    div_items = soup.find_all('div', class_="rt-item")
    # div=soup.find_all('div',attrs={'class':"results_table accepted_list"})
    
    # div_item=soup.find_all('div',attrs={'class':'rt-item'})
    # return div_item
    print(div_items)

if __name__ == "__main__":
    print(get_link_to_file('60072RS'))