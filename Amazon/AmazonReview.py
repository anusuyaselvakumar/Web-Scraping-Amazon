import requests, re
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
import os

def review_scraping(url,page):
    url = f"{url}&pageNumber={page}"
    
    user_agent = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }
   
    response = requests.get(url,headers = user_agent)
    #print(response.status_code)
   
    soup = BeautifulSoup(response.content,'lxml')
    # print(soup.find_all('div',{'class' : 'a-section review aok-relative'}))
    
    reviews = []
       
    for review in soup.find_all('div',{'class' : 'a-section review aok-relative'}):
        name = review.find('span',{'class' : 'a-profile-name'}).text
        ratings = review.find('i',{'data-hook' : 'review-star-rating'}).text
        comments = re.sub("\s+"," ",review.find('span',{'data-hook' : 'review-body'}).text)
        
        data = {
            'Name' : name,
            'Ratings' : ratings,
            'Comments' : comments
        }
        
        reviews.append(data)
        
    df = pd.DataFrame(reviews)
    df.to_excel('Amazon_reviews.xlsx', index=False)        
    return reviews
   

url = "https://www.amazon.in/Airdopes-141-Bluetooth-Wireless-Playtime/product-reviews/B09N3XMZ5F/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
page = 1

for review in review_scraping(url,page):
    print(review)
    print()