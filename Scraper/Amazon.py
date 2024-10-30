from datetime import datetime
import requests
import csv
import bs4
import concurrent.futures
from tqdm import tqdm
USER_AGENT='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
REQUEST_HEADER={
    'User-Agent':USER_AGENT,
    'Accept-Language':'en-US,en;q=0.5',

}
NO_THREADS=5
def get_page_html(url):
    res=requests.get(url=url,headers=REQUEST_HEADER)
    return res.content
def get_product_price(soup):
    main_price_span=soup.find('span',attrs={
        'class':'a-price-whole'
    })
    
    return main_price_span.get_text(strip=True).strip().replace('.','')
def get_product_title(soup):
    product_title=soup.find('span',id='productTitle')
    return product_title.text.strip()

def get_product_rating(soup):
    product_rating_div=soup.find('div',attrs={
        'id':'averageCustomerReviews'
    })
    product_rating_section=product_rating_div.find('span', id='acrPopover',attrs={
        'class':"reviewCountTextLinkedHistogram noUnderline"
    })

    product_rating=product_rating_section.find('span',attrs={
        'class':'a-icon-alt'
    })
    return float(product_rating.get_text(strip=True).strip().split()[0])


def extract_product_info(url,output):
    product_info={}
    html=get_page_html(url)
    soup=bs4.BeautifulSoup(html,'lxml')

    product_info['title']=get_product_title(soup)
    product_info['price']=get_product_price(soup)
    product_info['rating']=get_product_rating(soup)
    output.append( product_info)


if __name__=="__main__":
    product_data=[]
    urls=[]
    with open("amazon_web.csv",newline='')as csvFile:
        urls=list(csv.reader(csvFile,delimiter=','))
    with concurrent.futures.ThreadPoolExecutor(max_workers=NO_THREADS) as executor:
        for wkn in tqdm(range(0,len(urls))):
            executor.submit(extract_product_info,urls[wkn][0],product_data)
    output_file='amazon_product_data-{}.csv'.format(
        datetime.today().strftime("%d_%m_%Y")
    )
    with open(output_file,'w',newline='')as outputFile:
        write=csv.writer(outputFile)
        write.writerow(product_data[0].keys())
        for product in product_data:
            write.writerow(product.values())