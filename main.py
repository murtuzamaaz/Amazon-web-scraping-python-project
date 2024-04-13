from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
#function to get product title
def get_title(soup):
    try:
        title=soup.find('span',attrs={'id':'productTitle'})
        title_value=title.text
        title_string=title_value.strip()
    except AttributeError:
        title_string=""
    return title_string
#function to get price
def get_price(soup):
    try:
        price=soup.find('span',attrs={'class':'a-offscreen'}).string.strip()
    except AttributeError:
        price=''
    return price   
#function to get rating 
def get_rating(soup):
    try:
        rate=soup.find('span',attrs={'class':'a-icon-alt'}).text
       
    except AttributeError:
        rate=""
    return rate



#Your user agent 
HEADERS=({'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36','Accept-Language':'en-US, en;q=0.5'})

#URL of website you want to scrape 
URL='https://www.amazon.com/s?k=playstation+4&crid=2HZV7TV1VVZSH&sprefix=pla%2Caps%2C600&ref=nb_sb_ss_ts-doa-p_1_3'

#requests to get website data 
webpage=requests.get(URL,headers=HEADERS)
#converting to html
soup=BeautifulSoup(webpage.content,'html.parser')

#loop which finds all product links
links=soup.find_all("a",attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
link_list=[]
for link in links:
    link_list.append(link.get('href'))

d={'title':[],'price':[],'rating':[]}
#loop to extract data
for link in link_list:
    new_webpage=requests.get('https://amazon.com'+link,headers=HEADERS)

    new_soup=BeautifulSoup(new_webpage.content,'html.parser')
    d['title'].append(get_title(new_soup))
    d['price'].append(get_price(new_soup))
    d['rating'].append(get_rating(new_soup))

#converting to csv
df=pd.DataFrame(d)
amazon_data=df.to_csv()
print(amazon_data)






