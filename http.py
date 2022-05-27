import requests
import re
from bs4 import BeautifulSoup

# THSRshare/ NBA/ forsale/ mobilesales
Board = 'mobilesales'
key_article = "iphone" # split with "," comma 
# key_content = "螢幕"
num_pages = 5
ppt_url = 'https://www.ptt.cc'
url = 'https://www.ptt.cc/bbs/'+Board+'/index.html'
selected_url = []

for i in range(1, num_pages+1):
    print(f"Page {i} : ")
    web = requests.get(url)                                 #get the website request
    soup = BeautifulSoup(web.text,'html.parser')            #parse the website text
    articles = soup.select('div.title a')                   #get articles
    
    paging = soup.select('div.btn-group-paging a')          #get the pre-page group
    next_url = 'https://www.ptt.cc'+paging[1]['href']       #get the pre-page url
    url = next_url

    for article in articles:
        for key in key_article.split(","):
            if article.text.find(key) != -1:
                print(article.text, ppt_url + article['href'])
                selected_url.append(ppt_url + article['href'])