import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
import requests
from tkinter.filedialog import asksaveasfilename
import csv
import bs4
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas
import time
from selenium.webdriver.common.action_chains import ActionChains

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
options.add_argument('--disable-software-rasterizer') 
action=ActionChains(driver)

USER_AGENT='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
REQUEST_HEADER={
    'User-Agent':USER_AGENT,
    'Accept-Language':'en-US,en;q=0.5',
}

urls=f"https://kital-tools.com/search?gf_312953=brand_TONE&q=tone&options%5Bprefix%5D=last"
origin_link="https://kital-tools.com"
name="TONE"
count_page=53

def get_link_to_file(url):
    driver.get(url)
    time.sleep(1.5) 
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    return soup
def get_data_from_web(index):
    url = f"{urls}&page={index}"
    driver.get(url)
    time.sleep(1.5) 
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    data_web = []
    products = soup.findAll('div', attrs={'class': 'spf-col-xl-2 spf-col-lg-3 spf-col-md-3 spf-col-sm-3 spf-col-6'})
    for product in products:
        name_tag = product.find("div", class_="h4 spf-product-card__title").find("a")
        name = name_tag.text.strip() if name_tag else "Không có tên"
        link = "https://kital-tools.com" + name_tag["href"] if name_tag else "Không có link"   
        data_web.append([index, name, link])
    return data_web
def get_data_from_link(url):
    if not url:
        print("Url Error")
        return None

    driver.get(url)
    time.sleep(1.5) 
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Ảnh
    img_tag = soup.find('img', class_='zoomImg')
    img_link = img_tag['src'] if img_tag else "No Image Found"

    # Tiêu đề
    title_tag = soup.find('h1', class_='product-single__title')
    title = title_tag.text.strip() if title_tag else "Không có tiêu đề"

    # Thông tin chi tiết
    product_info = soup.find('div', class_='product-single__meta')
    details = {}
    if product_info:
        for div in product_info.find_all('div'):
            text = div.text.strip()
            if text:
                parts = text.split("】")
                if len(parts) == 2:
                    key = parts[0].replace("【", "").strip()
                    value = parts[1].strip()
                    details[key] = value

    # Mô tả
    description_tag = soup.find('div', class_='product-single__description rte')
    description = description_tag.text.strip() if description_tag else " "

    # Giá
    price_tag = soup.find("span", class_='price-item price-item--regular')
    price = price_tag.text.strip() if price_tag else "None"
    time.sleep(1.5)
    return {
        "Product Name": title,
        "Image Link": img_link,
        **details,
        "Description": description,
        "Price": price
    }
def get_data_to_file():
    full_data = []
    for i in range(41,54):
        full_data.extend(get_data_from_web(i))
        print(f"✅ Đã lấy dữ liệu trang {i}")

    df_web = pd.DataFrame(full_data, columns=["Page Index", "Product Name", "Product Link"])
    print(df_web.count())

    product_details_list = []

    for index, row in df_web.iterrows():
        if pd.notna(row["Product Link"]):  # Kiểm tra không phải None/NaN
            product_details = get_data_from_link(row["Product Link"])
            if not product_details:  # Nếu lỗi thì bỏ qua
                print(f"❌ Bỏ qua dòng {index} do không lấy được dữ liệu")
                continue
            product_details["Product Name"] = row["Product Name"]
            product_details["Product Link"] = row["Product Link"]
            product_details_list.append(product_details)
            print(f"✅ complete row {index}")
        else:
            print(f"⚠️ Link bị thiếu ở dòng {index}")
            continue

    print('✅ Hoàn tất crawl thông tin chi tiết')
    df_details = pd.DataFrame(product_details_list)

    # Kiểm tra xem cột có tồn tại trước khi merge
    missing_cols = {"Product Name", "Product Link"} - set(df_details.columns)
    if missing_cols:
        print(f"❌ Thiếu cột: {missing_cols} trong df_details. Không thể merge.")
        return

    df_final = df_web.merge(df_details, on=["Product Name", "Product Link"], how="left")
    df_final.to_csv(f"{name}.csv", index=False, encoding="utf-8-sig")
    print(f"🚀 Đã lưu {len(df_web)} sản phẩm vào {name}.csv")
get_data_to_file()