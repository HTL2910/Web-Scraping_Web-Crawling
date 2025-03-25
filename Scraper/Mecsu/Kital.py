import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Cấu hình Selenium
service = Service()
options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-software-rasterizer')
options.add_argument('--headless=new')  # Chế độ không giao diện

driver = webdriver.Chrome(service=service, options=options)
origin_link = "https://kital-tools.com"

def scroll_and_get_products():
    """Cuộn trang để tải hết dữ liệu lazy loading."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Chờ trang tải thêm sản phẩm
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # Nếu không có sản phẩm mới, dừng lại
        last_height = new_height

def scrape_page(index):
    """Thu thập dữ liệu từ một trang cụ thể."""
    url = f"https://kital-tools.com/collections/hand-tools?gf_312953=brand_ASH&page={index}"
    driver.get(url)
    time.sleep(5)  # Đợi trang tải ban đầu
    scroll_and_get_products()
    
    # Phân tích HTML sau khi cuộn
    soup = BeautifulSoup(driver.page_source, "html.parser")
    products = soup.find_all("div", class_="grid-view-item product-card")
    
    data_web = []
    for product in products:
        name_tag = product.find("span", class_="visually-hidden")
        name = name_tag.text.strip() if name_tag else "Không có tên"
        
        link_tag = product.find("a", class_="grid-view-item__link")
        link = origin_link + link_tag["href"] if link_tag else "Không có link"
        
        data_web.append([index, name, link])
    
    return data_web

def main():
    all_data = []
    total_pages = 16  # Số trang cần crawl (có thể điều chỉnh)
    
    name="Kital_brand_ASH"
    for i in range(1, total_pages + 1):
        print(f"Đang thu thập dữ liệu từ trang {i}...")
        page_data = scrape_page(i)
        all_data.extend(page_data)
    
    driver.quit()
    
    # Lưu dữ liệu vào CSV
    df_web = pd.DataFrame(all_data, columns=["Page Index", "Product Name", "Product Link"])
    df_web.to_csv(f"{name}.csv", index=False, encoding="utf-8-sig")
    print(f"Đã lưu {len(df_web)} sản phẩm vào {name}.csv 🚀")

if __name__ == "__main__":
    main()

