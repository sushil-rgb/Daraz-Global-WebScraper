import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from functionalities.tools import userAgents, TryExcept, yamlMe, check_domain
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError


class Daraz:    
    def __init__(self):        
        self.headers = {"User-Agent": userAgents()} 
        self.catchClause = TryExcept()
        self.yaml_me = yamlMe('selectors') 
        

    async def category_name(self, category_url):
        req = requests.get(category_url, headers=self.headers)
        soup = BeautifulSoup(req.content, 'lxml')
        # category = f"{soup.find('span', class_='breadcrumb_item_anchor breadcrumb_item_anchor_last').text.strip()}"
        category = [cate.text.strip() for cate in soup.find('ul', class_='breadcrumb').find_all('li', class_='breadcrumb_item')][-1]
        return category
        # name = re.sub(r"[/_\-]", "", ' '.join(category[1:]))
        # return name
     
    async def product_details(self, product_url):
        async with async_playwright() as p:
            browser = await p.firefox.launch(headless = True)
            context = await browser.new_context(user_agent = userAgents())
            page = await context.new_page()

            await page.goto(product_url)

            datas = {
                "Name": await self.catchClause.text(page.query_selector(self.yaml_me['product_name'])),
                "Discount price": await self.catchClause.text(page.query_selector(self.yaml_me['product_dc_price'])),
                "Original price": await self.catchClause.text(page.query_selector(self.yaml_me['product_og_price'])),
                "Sold by": await self.catchClause.text(page.query_selector(self.yaml_me['store'])),
                "Store link": f"""https:{await self.catchClause.attributes(page.query_selector(self.yaml_me['store']), 'href')}""",
                "Hyperlink": product_url,
                "Image": await self.catchClause.attributes(page.query_selector(self.yaml_me['image_link']), 'src'),
            }

            await browser.close()

            return datas

    # The below method scrapes product's names, prices, links and images according to the category:
    async def scrapeMe(self, category_url):        
        async with async_playwright() as p:      
            daraz_dicts = []      
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(user_agent = userAgents())
            page = await context.new_page()
            
            await page.goto(category_url)            

            country = check_domain(category_url)

            print(f"""Initiating the automation | Powered by Playwright.\n
                      Daraz {country}
                  """)
            self.category = await self.category_name(category_url)
            # Scraping the total number of pages
            last_page_number = await page.query_selector_all(self.yaml_me['last_page_number'])
            
            self.last_one = int(await (last_page_number[len(last_page_number)-2]).get_attribute('title'))            
            
            print(f"Category: {self.category} | Number of pages: {self.last_one}")
            next_page = await page.query_selector(self.yaml_me['next_page_button'])            

            # Loop is for pagination: Added a 2 second interval between each click.
            for count in range(1, self.last_one+1):                
                main_contents = await page.query_selector_all(self.yaml_me['category_main_contents'])
                print(f"Scraping page | {count}")
                for content in main_contents:
                    datas = {
                        "Name": await self.catchClause.text(content.query_selector(self.yaml_me['category_product_names'])),
                        "Original price": await self.catchClause.text(content.query_selector(self.yaml_me['category_discount_price'])),
                        "Discount price": await self.catchClause.text(content.query_selector(self.yaml_me['category_og_price'])),
                        "Discount rate": (await self.catchClause.text(content.query_selector(self.yaml_me['category_discount_rate']))).replace("-", ""),
                        "Hyperlink": f"""https:{await self.catchClause.attributes(content.query_selector(self.yaml_me['category_product_links']), 'href')}""",
                        "Image": await self.catchClause.attributes(content.query_selector(self.yaml_me['category_product_image']), 'src') ,
                    }                    
                    daraz_dicts.append(datas)
                try:
                    await page.wait_for_selector(self.yaml_me['next_page_button'], timeout = 10000)
                    await next_page.click()
                except PlaywrightTimeoutError:                    
                    print(f"Content loading error at page number {count}. There are no result found beyond this page. Scraper is exiting......")
                    break

                await page.wait_for_timeout(timeout=2*1000)                                    
                    
            await browser.close() 

        # Now exporting to excel database:
        df = pd.DataFrame(data = daraz_dicts)
        df.to_excel(f"""Daraz database//{self.category} database-{country}.xlsx""", index = False)      
        print(f"{self.category} saved.")       
            
 