from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from time import sleep
import pandas as pd
import winsound
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


class Scraper:
    headers ={'User-Agent': get_ua()}


    def __init__(self, url):
        self.url = url
        self.r = requests.get(url, headers=self.headers)
        self.soup = BeautifulSoup(self.r.content, 'lxml')

        self.opt = Options()
        self.path = Service("c:\\users\\chromedriver.exe")
        self.selenium_arguments = ['--headless',  f"user-agent= {get_ua()}", "window-size=1400,900", '--silent', '--no-sandbox', 'disable-notifications', '--disable-dev-shm-usage', '--disable-gpu']
        
    

    def status_code(self):
        soup = BeautifulSoup(self.r.content, 'lxml')
        try:
            if self.r.status_code == 200:
                return f"Status code | {self.r.status_code}\nLink is accessible."
        except Exception:
            return "Can't access web. DENIED!!!"
    

    def beautifulsoup_scraper(self):
        soup = BeautifulSoup(self.r.content, 'lxml')
        return soup.prettify()


    def selenium_scraper(self):
        all_product_links = []
        
        self.opt.add_experimental_option('detach', True)
        self.opt.add_experimental_option('excludeSwitches', ['enable-logging'])

        # opt.headless = selenium_bool
        for arg in self.selenium_arguments:
            self.opt.add_argument(arg)

        driver = webdriver.Chrome(service=self.path, options=self.opt)

        driver.maximize_window()
        driver.get(self.url)
        
        
        try:
            mobile_links = WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'mainPic--ehOdr')))
        except TimeoutException:          
            mobile_links = WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'title--wFj93')))
                   
        for mobile in mobile_links:
            all_product_links.append(mobile.find_element(By.TAG_NAME, 'a').get_attribute('href'))
        
        
        driver.quit()

        return all_product_links
             

    def last_page(self):
        self.opt.add_experimental_option('detach', True)
        self.opt.add_experimental_option('excludeSwitches', ['enable-logging'])

        # opt.headless = selenium_bool
        for arg in self.selenium_arguments:
            self.opt.add_argument(arg)

        driver = webdriver.Chrome(service=self.path, options=self.opt)

        driver.maximize_window()
        driver.get(self.url)
        
        # WebDriverWait(driver, 10).until((EC.visibility_of_element_located((By.TAG_NAME, 'body')))).send_keys(Keys.END)
        try:
            last_page = WebDriverWait(driver, 10).until((EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div[3]/div[1]/div/div[1]/div[3]/div/ul/li[8]')))).text.strip()
        except TimeoutException:
            last_page = WebDriverWait(driver, 10).until((EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[3]/div/ul/li[8]')))).text.strip()
        
        driver.quit()
        
        return int(last_page)
    

    def product_category_name(self):       
        self.opt.add_experimental_option('detach', True)
        self.opt.add_experimental_option('excludeSwitches', ['enable-logging'])

        # opt.headless = selenium_bool
        for arg in self.selenium_arguments:
            self.opt.add_argument(arg)

        driver = webdriver.Chrome(service=self.path, options=self.opt)

        driver.maximize_window()
        driver.get(self.url)

        category = WebDriverWait(driver, 10).until((EC.visibility_of_element_located((By.ID, 'J_breadcrumb'))))

        list_breadcumbs = category.find_elements(By.TAG_NAME, 'li')

        if len(list_breadcumbs) == 4:
            product_category_name = f"{list_breadcumbs[2].text.strip()}-{list_breadcumbs[-1].text.strip()}"
        else:
            product_category_name = list_breadcumbs[-1].text.strip()
        
        driver.quit()

        return product_category_name


    def product_names(self):
        all_product_names = []

        self.opt.add_experimental_option('detach', True)
        self.opt.add_experimental_option('excludeSwitches', ['enable-logging'])

        # opt.headless = selenium_bool
        for arg in self.selenium_arguments:
            self.opt.add_argument(arg)

        driver = webdriver.Chrome(service=self.path, options=self.opt)

        driver.maximize_window()
        driver.get(self.url)


        names = WebDriverWait(driver, 10).until((EC.visibility_of_all_elements_located((By.CLASS_NAME, 'title--wFj93'))))

        for name in names:
            all_product_names.append(name.text.strip())
        
        driver.quit()
        
        return all_product_names
    

    def product_price(self):
        all_product_price = []

        self.opt.add_experimental_option('detach', True)
        self.opt.add_experimental_option('excludeSwitches', ['enable-logging'])

        # opt.headless = selenium_bool
        for arg in self.selenium_arguments:
            self.opt.add_argument(arg)

        driver = webdriver.Chrome(service=self.path, options=self.opt)

        driver.maximize_window()
        driver.get(self.url)
        
        prices = WebDriverWait(driver, 10).until((EC.visibility_of_all_elements_located((By.CLASS_NAME, 'price--NVB62'))))

        for price in prices:
            all_product_price.append(price.text.strip())
        
        driver.quit()
        return all_product_price
    
    