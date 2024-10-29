from datetime import datetime
import requests
import csv
import bs4

USER_AGENT='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
REQUEST_HEADER={
    'User-Agent':USER_AGENT,
    'Accept-Language':'en-US,en;q=0.5',

}
def get_page_html(url):
    res=requests.get(url=url,headers=REQUEST_HEADER)
    return res.content
def get_product_price(soup):
    main_price_span=soup.find('span',attrs={
        'class':'a-price-whole'
    })
    
    return main_price_span.get_text(strip=True).replace('.','')

def extract_product_info(url):
    product_info={}
    html=get_page_html(url)
    soup=bs4.BeautifulSoup(html,'lxml')

    product_info['price']=get_product_price(soup)
    return product_info


if __name__=="__main__":
    with open("amazon_web.csv",newline='')as csvFile:
        reader=csv.reader(csvFile,delimiter=',')
        for row in reader:
            url=row[0]
            print(extract_product_info(url))