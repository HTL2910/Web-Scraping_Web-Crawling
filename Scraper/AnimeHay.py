from datetime import datetime
import requests
import csv
import bs4
import concurrent.futures
from tqdm import tqdm
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
REQUEST_HEADER = {
    'User-Agent': USER_AGENT,
    'Accept-Language': 'en-US,en;q=0.5'
}

url='https://animehay.de/'


def get_page_html(url):
    try:
        res = requests.get(url=url, headers=REQUEST_HEADER)
        res.raise_for_status()  # Kiểm tra lỗi HTTP
        return res.content
    except requests.exceptions.RequestException as e:
        print(f"Lỗi không thấy nội dung trang: {e}")
        return None
def get_link_to_file(url):
    html=get_page_html(url)
    soup=bs4.BeautifulSoup(html,'lxml')
    return soup

def get_name_anime(soup):
    titles=[]
    
    title_div = soup.findAll('div', attrs={'class': 'movie-item'})
    for div in title_div:
        title=div.find('a',title=True)
        titles.append(title['title'] )
    return titles

def get_rating_anime(soup):
    ratings=[]
    
    anime_div = soup.findAll('div', attrs={'class': 'movie-item'})
    for div in anime_div:
        score_div = div.find('div', class_='score')
        if score_div:  # Kiểm tra nếu tìm thấy
            rating = score_div.text.strip()  # Lấy điểm số và loại bỏ khoảng trắng
            ratings.append(rating)
    return ratings
if __name__=="__main__":
    animes={}
    soup=get_link_to_file(url)
    animes['Name']=get_name_anime(soup)
    animes['Rating']=get_rating_anime(soup)
  
    for i in range(len(animes['Name'])):
        name = animes['Name'][i]
        rating = animes['Rating'][i]
        print(f"Anime #{i + 1}: Name: {name} : Rating: {rating}")
        print("###########################")
