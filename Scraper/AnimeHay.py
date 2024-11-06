from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Cấu hình ChromeDriver
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
options = Options()
options.add_argument('--headless')  # Chạy không hiển thị giao diện
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument(f'user-agent={USER_AGENT}')


service = Service()
driver = webdriver.Chrome(service=service, options=options)

url = 'https://animehay.de/'

def get_anime_data_with_selenium(url):
    driver.get(url)
    time.sleep(3)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    anime_items = soup.find_all('div', class_='movie-item')
    animes = {
        'Name': [],
        'Rating': []
    }
    for item in anime_items:
        title_tag = item.find('a', title=True)
        if title_tag:
            animes['Name'].append(title_tag['title'])
        score_tag = item.find('div', class_='score')
        if score_tag:
            rating = score_tag.text.strip()
            animes['Rating'].append(rating)
        else:
            animes['Rating'].append("N/A")  # Đánh giá trống nếu không tìm thấy

    return animes

if __name__ == "__main__":
    try:
        anime_data = get_anime_data_with_selenium(url)
        for i in range(len(anime_data['Name'])):
            name = anime_data['Name'][i]
            rating = anime_data['Rating'][i]
            print(f"Anime #{i + 1}: Name: {name} - Rating: {rating}")
            print("###########################")
    
    except Exception as e:
        print(f"Lỗi: {e}")
    
    finally:
        driver.quit()  
