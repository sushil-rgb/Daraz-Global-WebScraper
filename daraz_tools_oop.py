from email.message import EmailMessage
import traceback
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import itertools
import random
import os
import shutil
import smtplib
import pandas as pd
from bs4 import BeautifulSoup
import requests


def userAgents():
   with open(f"{os.getcwd()}\\user-agents.txt") as f:
    agents = f.read().split("\n")
    return random.choice(agents)
    

# For flattening the multi-dimensional lists:
def flat(d_lists):
    d_lists = d_lists
    return list(itertools.chain(*d_lists))


class DarazScraper:    
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {"User-Agent": userAgents()}       
    

    def category_name(self):
        req = requests.get(self.base_url, headers=self.headers)
        soup = BeautifulSoup(req.content, 'lxml')
        # category = f"{soup.find('span', class_='breadcrumb_item_anchor breadcrumb_item_anchor_last').text.strip()}"
        category = [cate.text.strip() for cate in soup.find('ul', class_='breadcrumb').find_all('li', class_='breadcrumb_item')]
        return ' '.join(category[1:])

     
    # The below method scrapes product's names, prices, links and images according to the category:
    def scrapeMe(self):        
        with sync_playwright() as p: 
            product_links = []           
            product_names = []
            product_prices = []
            product_images = []
            browser = p.chromium.launch(headless=True, slow_mo=1*5000)
            page = browser.new_page(user_agent=userAgents())
            page.goto(self.base_url)

            print(f"Initiating the automation | Powered by Playwright.")

            self.category = page.query_selector("//div[@class='info-panel--qjUGt']/h1[@class='title--Xj2oo']").inner_text().strip()

            # Scraping the total number of pages
            last_page_number = page.query_selector_all("//li[@tabindex='0']")
            last_one = int(last_page_number[len(last_page_number)-2].get_attribute('title'))
            
            print(f"Category: {self.category} | Number of pages: {last_one}")
            next_page = page.locator("xpath=//li[@title='Next Page']")

            # Loop is for pagination: Added a 2 second interval between each click.
            for count in range(1, last_one+1):
                page.wait_for_timeout(timeout=2*1000)
                print(f"Scraping page | {count}")
                links = [f"""https:{link.query_selector("//a").get_attribute('href')}""" for link in page.query_selector_all("//div[@class='title--wFj93']")]
                names = [name.query_selector("//a").get_attribute('title') for name in page.query_selector_all("//div[@class='title--wFj93']")]
                prices = [price.inner_text().strip() for price in page.query_selector_all("//span[@class='currency--GVKjl']")]
                images = [img.get_attribute('src') for img in page.query_selector_all("//img[@class='image--WOyuZ ']")]
                product_links.append(links), product_names.append(names), product_prices.append(prices), product_images.append(images)
                
                next_page.click()
                
            
            browser.close()
        
        # Storing in dicts for pandas dataframes:
        data_in_dicts = {
            "Name": flat(product_names),
            "Price": flat(product_prices),
            "Link": flat(product_links),
            "Image": flat(product_images)
        }
        
        return data_in_dicts
    
    
# Below class scrapes data from an individual product link available in Daraz Nepal:
class DarazIndivLinkScraper:        
    def __init__(self, website_url):       
        self.website_url = website_url
        self.headers = userAgents()
    
    def product_name(self):       
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, slow_mo=1*1000)
            page = browser.new_page(user_agent=self.headers)
            page.goto(self.website_url)

            try:
                page.wait_for_url(self.website_url)
                try:
                    name_selector = "//span[@class='pdp-mod-product-badge-title']"
                    page.wait_for_selector(name_selector, timeout=1*10000)
                    name = self.page.query_selector(name_selector).inner_text().strip()

                    browser.close()
                    return self.name   
                except TypeError:
                    name = "N/A"
                    return self.name             
            except Exception as e:
                print(f"Error in plawright script {page}")   
                traceback.print_exc()     

                browser.close()
    

    def product_discount_price(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, slow_mo=1*1000)
            page = browser.new_page(user_agent=self.headers)
            page.goto(self.website_url)

            try:
                page.wait_for_url(self.website_url)
                try:
                    price_selector = "//span[@class=' pdp-price pdp-price_type_normal pdp-price_color_orange pdp-price_size_xl']"
                    page.wait_for_selector(price_selector, timeout=1*10000)
                    price = self.page.query_selector(price_selector).inner_text().strip()

                    browser.close()
                    return price
                except TypeError:
                    price = "N/A"
            except Exception as e:
                print(f"Error in plawright script {page}") 
                traceback.print_exc()               
                browser.close()                
        
    
    def product_og_price(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, slow_mo=1*1000)
            page = browser.new_page(user_agent=self.headers)
            page.goto(self.website_url)

            try:
                page.wait_for_url(self.website_url)
                try:
                    og_selector = "//span[@class=' pdp-price pdp-price_type_deleted pdp-price_color_lightgray pdp-price_size_xs']"
                    page.wait_for_selector(og_selector)
                    ogPrice = self.page.query_selector(og_selector).inner_text().strip()

                    browser.close()
                    return ogPrice
                except TypeError:
                    ogPrice = "N/A"
            except Exception as e:
                print(f"Error in plawright script {self.page}")
                traceback.print_exc()
                browser.close()


class SplitDarazURL:
    def __init__(self, split_this_url):
        self.split_this_url = split_this_url
    

    def split(self, lastpages):
        url_lists = []
        lastpages = lastpages
        first_split = self.split_this_url.split("?")

        for index in range(1, self.lastpages+1):
            new_url = f"?page={str(index)}&".join(first_split)
            url_lists.append(new_url)
        
        return url_lists


class CreatePathDirectory:
    def __init__(self, folderName):
        self.folderName = folderName


    def createFolder(self):
        parent_dir = os.getcwd()
        path_dir = os.path.join(parent_dir, self.folderName)

        # Overwriting the  directory if already existed:
        if os.path.exists(path_dir):
            shutil.rmtree(path_dir)
        
        os.mkdir(path_dir)
        

class AlertEmail:
    def __init__(self, emailUserSender, emailSenderPassword):        
        self.emailUserSender = emailUserSender        
        self.emailPassword = emailSenderPassword        

    
    def sendAlert(self, emailUserReceiver, msgSubject, msgContent):
        self.emailUserReceiver = emailUserReceiver
        self.msgSubject = msgSubject
        self.msgContent = msgContent        

        msg = EmailMessage()
        msg['Subject'] = self.msgSubject
        msg["From"] = self.emailUserSender
        msg['To'] = self.emailUserReceiver
        msg.set_content(self.msgContent)        

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(self.emailUserSender, self.emailPassword)
            smtp.send_message(msg)
            smtp.quit()

