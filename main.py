from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

def get_title(soup):
    try:
        title=soup.find('span',attrs={'id':'productTitle'})
        title_value=title.text
        title_string=title_value.strip()
    except AttributeError:
        title_string=""
    return title_string
def get_price(soup):
    try:
        price=soup.find('span',attrs={'class':'a-offscreen'}).string.strip()
    except AttributeError:
        price=''
    return price   
def get_rating(soup):
    try:
        rate=soup.find('span',attrs={'class':'a-icon-alt'}).text
       
    except AttributeError:
        rate=""
    return rate




HEADERS=({'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36','Accept-Language':'en-US, en;q=0.5'})

URL='https://www.amazon.com/s?k=playstation+4&crid=2HZV7TV1VVZSH&sprefix=pla%2Caps%2C600&ref=nb_sb_ss_ts-doa-p_1_3'

webpage=requests.get(URL,headers=HEADERS)

soup=BeautifulSoup(webpage.content,'html.parser')

links=soup.find_all("a",attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
link_list=[]
for link in links:
    link_list.append(link.get('href'))

d={'title':[],'price':[],'rating':[]}

for link in link_list:
    new_webpage=requests.get('https://amazon.com'+link,headers=HEADERS)

    new_soup=BeautifulSoup(new_webpage.content,'html.parser')
    d['title'].append(get_title(new_soup))
    d['price'].append(get_price(new_soup))
    d['rating'].append(get_rating(new_soup))
    
df=pd.DataFrame(d)
amazon_data=df.to_csv()
print(amazon_data)






