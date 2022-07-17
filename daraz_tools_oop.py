from email.message import EmailMessage
import traceback
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import itertools
import random
import os
import shutil
import smtplib


def get_user_agent():
    uastrings = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 "
        "Safari/600.1.25",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 "
        "Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 "
        "Safari/537.85.10",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36"
    ]
 
    return random.choice(uastrings)


class FlattenedLists:
    def flat(self, d_lists):
        self.d_lists = d_lists
        return list(itertools.chain(*self.d_lists))


class DarazScraper:    
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = get_user_agent()
        
    
    def category_name(self):
        with sync_playwright() as p:
            self.browser = p.chromium.launch(headless=True, slow_mo=1*1000)
            self.page = self.browser.new_page(user_agent=self.headers)
            self.page.goto(self.base_url)           

            
            try:
                self.page.wait_for_url(self.base_url)
                self.query_name_selector = "//h1[@class='title--Xj2oo']"

                self.page.wait_for_selector(self.query_name_selector, timeout=10000)
                self.categ_name = self.page.query_selector(self.query_name_selector).inner_text().strip()
                self.browser.close()

                return self.categ_name
            except Exception as e:
                print(f"Playwright Script error. | {self.page}")
                traceback.print_exc()
                self.browser.close()  
               
    
    def number_of_pages(self):
        with sync_playwright() as p:
            self.browser = p.chromium.launch(headless=True, slow_mo=1*1000)
            self.page = self.browser.new_page(user_agent=self.headers)
            self.page.goto(self.base_url)

            self.last_page_number = self.page.query_selector_all("//li[@tabindex='0']")
            self.last_one = int(self.last_page_number[len(self.last_page_number)-2].get_attribute('title'))

            return self.last_one
            


    def scrapeLinksNamesPrices(self):
        # Setting up the Playwright driver:
        with sync_playwright() as p:
            self.browser = p.chromium.launch(headless=True, slow_mo=1*5000)
            self.page = self.browser.new_page(user_agent=self.headers)
            self.page.goto(self.base_url)

            # Splitting the url to get the page number for tracking purpose:
            # The split could be done cleaner by using regex, this one is ugly:
            self.letsplit = self.base_url.split("?")[-1].split("&")[0].split("=")[-1]
            print(f"Scraping page number | {self.letsplit}\n-----------------------------")

                
            try:                
                self.link_selector = "//div[@class='title--wFj93']/a"
                self.page.wait_for_selector(self.link_selector, timeout=10000)
                self.hyper_links = [f"https:{link.get_attribute('href')}" for link in self.page.query_selector_all(self.link_selector)]
            except PlaywrightTimeoutError:
                print("Timeout error. Reloading the page.")
                self.page.reload()
                self.link_selector = "//div[@class='title--wFj93']/a"
                self.page.wait_for_selector(self.link_selector, timeout=10000)
                self.hyper_links = [f"https:{link.get_attribute('href')}" for link in self.page.query_selector_all(self.link_selector)]  
              
            self.prod_selector = '//div[@class="title--wFj93"]'
            self.page.wait_for_selector(self.prod_selector, timeout=10000)
            
            self.prod_query_selector = self.page.query_selector_all(self.prod_selector)
            
            self.prod_names = [name.inner_text() for name in self.prod_query_selector] 
            
            self.price_selector = "//span[@class='currency--GVKjl']"
            self.page.wait_for_selector(self.price_selector, timeout=10000)

            self.prod_prices = [price.inner_text() for price in self.page.query_selector_all(self.price_selector)]
           
            self.browser.close()
                            
            return self.prod_names, self.prod_prices, self.hyper_links
           
    
# Below class scrapes data from an individual product link available in Daraz Nepal:
class DarazIndivLinkScraper:        
    def __init__(self, website_url):       
        self.website_url = website_url
        self.headers = get_user_agent()
    
    def product_name(self):       
        with sync_playwright() as p:
            self.browser = p.chromium.launch(headless=True, slow_mo=1*1000)
            self.page = self.browser.new_page(user_agent=self.headers)
            self.page.goto(self.website_url)

            try:
                self.page.wait_for_url(self.website_url)
                try:
                    self.name_selector = "//span[@class='pdp-mod-product-badge-title']"
                    self.page.wait_for_selector(self.name_selector, timeout=1*10000)

                    self.name = self.page.query_selector(self.name_selector).inner_text().strip()
                    self.browser.close()

                    return self.name   
                except TypeError:
                    self.name = "N/A"
                    return self.name             
            except Exception as e:
                print(f"Error in plawright script {self.page}")   
                traceback.print_exc()             
                self.browser.close()
    

    def product_discount_price(self):
        with sync_playwright() as p:
            self.browser = p.chromium.launch(headless=True, slow_mo=1*1000)
            self.page = self.browser.new_page(user_agent=self.headers)
            self.page.goto(self.website_url)

            try:
                self.page.wait_for_url(self.website_url)
                try:
                    self.price_selector = "//span[@class=' pdp-price pdp-price_type_normal pdp-price_color_orange pdp-price_size_xl']"
                    self.page.wait_for_selector(self.price_selector, timeout=1*10000)

                    self.price = self.page.query_selector(self.price_selector).inner_text().strip()
                    self.browser.close()

                    return self.price
                except TypeError:
                    self.price = "N/A"
            except Exception as e:
                print(f"Error in plawright script {self.page}") 
                traceback.print_exc()               
                self.browser.close()                
        
    
    def product_og_price(self):
        with sync_playwright() as p:
            self.browser = p.chromium.launch(headless=True, slow_mo=1*1000)
            self.page = self.browser.new_page(user_agent=self.headers)
            self.page.goto(self.website_url)

            try:
                self.page.wait_for_url(self.website_url)
                try:
                    self.og_selector = "//span[@class=' pdp-price pdp-price_type_deleted pdp-price_color_lightgray pdp-price_size_xs']"
                    self.page.wait_for_selector(self.og_selector)

                    self.ogPrice = self.page.query_selector(self.og_selector).inner_text().strip()
                    self.browser.close()

                    return self.ogPrice
                except TypeError:
                    self.ogPrice = "N/A"
            except Exception as e:
                print(f"Error in plawright script {self.page}")
                traceback.print_exc()
                self.browser.close()


class SplitDarazURL:
    def __init__(self, split_this_url):
        self.split_this_url = split_this_url
    

    def split(self, lastpages):
        self.url_lists = []
        self.lastpages = lastpages
        self.first_split = self.split_this_url.split("?")

        for index in range(1, self.lastpages+1):
            self.new_url = f"?page={str(index)}&".join(self.first_split)
            self.url_lists.append(self.new_url)
        
        return self.url_lists


class CreatePathDirectory:
    def __init__(self, folderName):
        self.folderName = folderName


    def createFolder(self):
        self.parent_dir = os.getcwd()
        self.path_dir = os.path.join(self.parent_dir, self.folderName)

        # Overwriting the  directory if already existed:
        if os.path.exists(self.path_dir):
            shutil.rmtree(self.path_dir)
        
        os.mkdir(self.path_dir)
        

class AlertEmail:
    def __init__(self, emailUserSender, emailSenderPassword):        
        self.emailUserSender = emailUserSender        
        self.emailPassword = emailSenderPassword        

    
    def sendAlert(self, emailUserReceiver, msgSubject, msgContent):
        self.emailUserReceiver = emailUserReceiver
        self.msgSubject = msgSubject
        self.msgContent = msgContent        

        self.msg = EmailMessage()
        self.msg['Subject'] = self.msgSubject
        self.msg["From"] = self.emailUserSender
        self.msg['To'] = self.emailUserReceiver
        self.msg.set_content(self.msgContent)        

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(self.emailUserSender, self.emailPassword)
            smtp.send_message(self.msg)
            smtp.quit()

