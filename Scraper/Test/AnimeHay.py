from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import csv


# Cấu hình ChromeDriver
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

url = 'https://animehay.de/'

def get_link_to_file(url):
    driver.get(url)
    time.sleep(3) 
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    return soup

def get_name_anime(soup):
    titles = []
    title_div = soup.findAll('div', attrs={'class': 'movie-item'})
    for div in title_div:
        title = div.find('a', title=True)
        titles.append(title['title'])
    return titles

def get_rating_anime(soup):
    ratings = []
    anime_div = soup.findAll('div', attrs={'class': 'movie-item'})
    for div in anime_div:
        score_div = div.find('div', class_='score')
        if score_div:
            rating = score_div.text.strip()
            ratings.append(rating)
        else:
            ratings.append("N/A")  
    return ratings
def get_list_url():
    count_page=100
    urls=[]
    for i in range(count_page):
        url=f'https://animehay.de/phim-moi-cap-nhap/trang-{i}.html'
        urls.append(url)
    return urls
def get_list_anime(url):
    animes = {'Name': [], 'Rating': []}    
    
    soup = get_link_to_file(url)
    animes['Name'].extend(get_name_anime(soup))
    animes['Rating'].extend( get_rating_anime(soup))
        # for i in range(len(animes['Name'])):
        #     name = animes['Name'][i]
        #     rating = animes['Rating'][i]
        #     print(f"Anime #{i + 1}: Name: {name} - Rating: {rating}")
        #     print("###########################")
    
    return animes
def save_data(index_page):
    urls=get_list_url()
    animes={}
    animes=get_list_anime(urls[index_page])
    name_file_csv='AnimeHay.csv'
    with open(name_file_csv, 'a', newline='', encoding='utf-8') as outputFile:
        writer=csv.writer(outputFile)
        if(index_page==0):
            writer.writerow(['Index','Name', 'Rating']) 
        for i in range(len(animes['Name'])):
            writer.writerow([i+1+len(animes['Name'])*index_page,animes['Name'][i], animes['Rating'][i]])
    driver.quit()  
if __name__ == "__main__":
    index=32
    save_data(index)
   