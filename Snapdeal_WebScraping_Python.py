# Importing required libraries/modules

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
# Taking input from the user :

print("Enter the url of the snapdeal webpage !")
URL = input()
HEADERS = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15','Accept-Language':'en-US,en;q=0.5'}

webpage = requests.get(URL,headers=HEADERS)
if (webpage.status_code == 200):
    print("Data Fetched Successfully !")
else:
    print(f" Error {webpage.status_code} !")
    
soup = BeautifulSoup(webpage.content,'html.parser')
# Extracting the product links from webpage

products_list = soup.find("div", attrs={'class':'product-row js-product-list centerCardAfterLoadWidgets dp-click-widgets'})
products_list_soup = BeautifulSoup(str(products_list),'html.parser')

header_tags = products_list_soup.find_all("section", attrs={'class':'js-section clearfix dp-widget'})

links_list = []

for header_tag in header_tags:
    
    header_soup = BeautifulSoup(str(header_tag),'html.parser')
    sub_header_tags =  header_soup.find_all("div", attrs={'class':'col-xs-6 favDp product-tuple-listing js-tuple'})
    
    for sub_header_tag in sub_header_tags:
        
        product_link_tag = sub_header_tag.find("a", attrs={'class':'dp-widget-link'})
        product_link = product_link_tag.get('href')
        
        links_list.append(product_link)
snapdeal_scrapData = {'Product_Name':[],'Price':[],'Rating':[],'Availability':[],'Product_Link':[]}
# Functions to extract product details

# Function to scrap product name 

def fetch_productName(product_link_soup):
    
    try:
        # Extracting the upper tag of product name
        product_name_uppertag = product_link_soup.find("div", attrs={'class':'col-xs-22'})
        product_name_tag = product_name_uppertag.find("h1", attrs={'class':'pdp-e-i-head'})
        
        # Extracting the product name
        product_name = (product_name_tag).text.strip()
    
    except AttributeError:
        product_name = "Not Available"
        
    return product_name

# Function to extract product price

def fetch_productPrice(product_link_soup):
    
    try:
        # Extracting upper tag of product price
        product_price_uppertag = product_link_soup.find("span", attrs={'class':'pdp-final-price'})
        
        # Extracting tag of product tag
        product_price_tag = product_price_uppertag.find("span", attrs={'class':'payBlkBig'})
        
        # Extracting the product price
        product_price = "Rs. " + (product_price_tag).text.strip()
    
    except AttributeError:
        product_price = "Not Available"
        
    return product_price

# Function to extract product rating

def fetch_productRating(product_link_soup):
    
    try:
        product_rating_tag = product_link_soup.find("span", attrs={'class':'avrg-rating'})
        product_rating_string = (product_rating_tag).text.strip()
        
        # Extracting the product rating
        product_rating = ( product_rating_string[1:4] + "⭐️" )
    
    except AttributeError:
        product_rating = "NA"
        
    return product_rating

# Function to extract availability of product

def fetch_productAvailability(product_link_soup):
    
    try:
        product_availability_tag = product_link_soup.find("div", attrs={'class':'clearfix inventory txt-center fnt-12'})
        product_availability = product_availability_tag.text.strip()
        
    except AttributeError:
        try:
            # Extracting tag of product availability
            product_availability_tag = product_link_soup.find("div", attrs={'class':'sold-out-err'})
            product_availability = product_availability_tag.text.strip()
            
        except AttributeError:
            product_availability = "Available"
            
    return product_availability
# Scrapping Product Details & Storing in a dictionary

for link in links_list:
    new_webpage = requests.get(link,headers=HEADERS)
    
    if ( new_webpage.status_code != 200 ):
        
        error_message = ("Error " + str(new_webpage.status_code) + " Access Denied")
        
    
        snapdeal_scrapData['Product_Name'].append(error_message)
        snapdeal_scrapData['Price'].append(error_message)
        snapdeal_scrapData['Rating'].append(error_message)
        snapdeal_scrapData['Availability'].append(error_message)
        snapdeal_scrapData['Product_Link'].append(link)
        
        continue
        
    product_link_soup = BeautifulSoup(new_webpage.content,'html.parser')
    
    snapdeal_scrapData['Product_Name'].append(fetch_productName(product_link_soup))
    snapdeal_scrapData['Price'].append(fetch_productPrice(product_link_soup))
    snapdeal_scrapData['Rating'].append(fetch_productRating(product_link_soup))
    snapdeal_scrapData['Availability'].append(fetch_productAvailability(product_link_soup))
    snapdeal_scrapData['Product_Link'].append(link)
    
# Generating a dataframe using pandas library

snapdeal_df = pd.DataFrame.from_dict(snapdeal_scrapData)

# Converting the scrap data to a CSV File

snapdeal_df.to_csv("snapdeal_scrapData.csv",index=False)
print(snapdeal_df)
 