from email.mime import base
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
import asyncio
import itertools
import random


def get_ua():
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
        self.headers = get_ua()
        
    
    def category_name(self):
        with sync_playwright() as p:
            self.browser = p.chromium.launch(headless=True, slow_mo=3*1000)
            self.page = self.browser.new_page(user_agent=self.headers)
            self.page.goto(self.base_url)

            categ_name = self.page.query_selector("//h1[@class='title--Xj2oo']").inner_text().strip()
            self.browser.close()

            return categ_name   
    

    def number_of_pages(self):
        with sync_playwright() as p:
            self.browser = p.chromium.launch(headless=True, slow_mo=1*3000)
            self.page = self.browser.new_page(user_agent=self.headers)
            self.page.goto(self.base_url)

            last_page_number = self.page.query_selector_all("//li[@tabindex='0']")

            return int(last_page_number[len(last_page_number)-2].get_attribute('title'))
    

    def all_product_links(self):
        # Setting up the Playwright driver:
        with sync_playwright() as p:
            self.browser = p.chromium.launch(headless=True, slow_mo=1*1000)
            self.page = self.browser.new_page(user_agent=self.headers)
            self.page.goto(self.base_url)

            hyper_links = [f"https:{link.get_attribute('href')}" for link in self.page.query_selector_all("//div[@class='title--wFj93']/a")]
            
            # Using for loop to print sraped data in output console:
            for link in self.page.query_selector_all("//div[@class='title--wFj93']/a"):
                print(f"https:{link.get_attribute('href')}")
            self.browser.close()


            return hyper_links
    
        
    def all_product_names(self):
        with sync_playwright() as p:
            self.browser = p.chromium.launch(headless=True, slow_mo=1*1000)
            self.page = self.browser.new_page(user_agent=self.headers)
            self.page.goto(self.base_url)

            prod_names = [name.inner_text() for name in self.page.query_selector_all('//div[@class="title--wFj93"]')]

            # Using for loop to print sraped data in output console:
            for name in self.page.query_selector_all('//div[@class="title--wFj93"]'):
                print(name.inner_text().strip())
            
            self.browser.close()
            return prod_names
    

    def all_product_prices(self):
        with sync_playwright() as p:
            self.browser = p.chromium.launch(headless=True, slow_mo=1*1000)
            self.page = self.browser.new_page(user_agent=self.headers)
            self.page.goto(self.base_url)

            prod_prices = [price.inner_text() for price in self.page.query_selector_all("//span[@class='currency--GVKjl']")]

            # Using for loop to print sraped data in output console:
            for price in self.page.query_selector_all("//span[@class='currency--GVKjl']"):
                print(price.inner_text().strip())
            self.browser.close()

            return prod_prices
    

# Below class scrapes data from an individual product link available in Daraz Nepal:
class DarazIndivLinkScraper:    
    def __init__(self, website_url):
        self.website_url = website_url

    
    def product_name(self):
        pass
        with sync_playwright() as p:
            self.browser = p.chromium.launch(headless=True, slow_mo=3*1000)
            self.page = self.browser.new_page(user_agent=self.headers)
            self.page.goto(self.website_url)

            name = self.page.query_selector("//span[@class='pdp-mod-product-badge-title']").inner_text().strip()
            self.browser.close()

            return name
    

    def product_discount_price(self):
        with sync_playwright() as p:
            self.browser = p.chromium.launch(headless=True, slow_mo=3*1000)
            self.page = self.browser.new_page(user_agent=self.headers)
            self.page.goto(self.website_url)

            price = self.page.query_selector("//span[@class=' pdp-price pdp-price_type_normal pdp-price_color_orange pdp-price_size_xl']").inner_text().strip()
            self.browser.close()

            return price
        
    
    def product_og_price(self):
        with sync_playwright() as p:
            self.browser = p.chromium.launch(headless=True, slow_mo=3*2000)
            self.page = self.browser.new_page(user_agent=self.headers)
            self.page.goto(self.website_url)

            ogPrice = self.page.query_selector("//span[@class=' pdp-price pdp-price_type_deleted pdp-price_color_lightgray pdp-price_size_xs']").inner_text().strip()
            self.browser.close()

            return ogPrice


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
