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

def get_link_to_file(url):
    urls=[]
    html=get_page_html(url)
    soup=bs4.BeautifulSoup(html,'lxml')
    link_text=soup.findAll('a',attrs={
        'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'
    })
    for link in link_text:
        href= link.get('href')
        if not href.startswith("http"):
            href = "https://www.amazon.com" + href
            urls.append(href)
        else:
            return None
    return urls
    

if __name__=="__main__":
    links=get_link_to_file('https://www.amazon.com/s?k=gaming&_encoding=UTF8&content-id=amzn1.sym.5b60f7cf-8cdf-42b5-80ee-74f9ab340b5d&pd_rd_r=c9bafa08-d645-4a6c-b184-698f7af4aedc&pd_rd_w=o1viv&pd_rd_wg=Zr42N&pf_rd_p=5b60f7cf-8cdf-42b5-80ee-74f9ab340b5d&pf_rd_r=665N4RS8SPQNT1D7188Y&ref=pd_hp_d_atf_unk')
    with open("amazon_web.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for link in links:
            writer.writerow([link])
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