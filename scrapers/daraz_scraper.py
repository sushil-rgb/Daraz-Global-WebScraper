import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from tools.functionalities import userAgents, TryExcept, yamlMe, check_domain
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError


class Daraz:    
    """
    A class for scraping products from Daraz website.

    Attributes:
    -----------
    headers : dict
        A dictionary containing the user agent for the requests.
    catchClause : TryExcept
        A TryExcept object.
    yaml_me : dict
        A dictionary containing the selectors to be used for scraping.
    category : str
        A string representing the category name.
    last_one : int
        An integer representing the number of pages for the category.

    Methods:
    --------
    category_name(category_url: str) -> str:
        Returns the category name for the given category url.

    product_details(product_url: str) -> dict:
        Returns the details of the given product url.

    scrapeMe(category_url: str) -> None:
        Scrapes the products according to the category and saves them to an excel file.
    """

    def __init__(self):       
        """
        Initializes the headers, catchClause and yaml_me attributes of the class.
        """ 

        self.headers = {"User-Agent": userAgents()} 
        self.catchClause = TryExcept()
        self.yaml_me = yamlMe('selectors') 
        

    async def category_name(self, category_url):
        """
        Returns the category name for the given category url.

        Parameters:
        -----------
        category_url : str
            A string representing the url of the category.

        Returns:
        --------
        category : str
            A string representing the name of the category.
        """

        req = requests.get(category_url, headers=self.headers)
        soup = BeautifulSoup(req.content, 'lxml')
        category = [cate.text.strip() for cate in soup.find('ul', class_='breadcrumb').find_all('li', class_='breadcrumb_item')][-1]
        return category        
     
    async def product_details(self, product_url):
        """
        Returns the details of the given product url.

        Parameters:
        -----------
        product_url : str
            A string representing the url of the product.

        Returns:
        --------
        datas : dict
            A dictionary containing the details of the product.
        """
         
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
    
    async def scrapeMe(self, category_url):        
        """
    This function scrapes product data from a category page on Daraz website, using Playwright library for web automation.
    The scraped data is stored in a Pandas DataFrame and exported as an Excel file.

    Args:
        category_url (str): The URL of the category page to scrape.

    Returns:
        None.

    Raises:
        None.
    """
        
        # Initialize a list to store the scraped data.
        daraz_dicts = []        

        # Launch the Playwright browser.
        async with async_playwright() as p:                    
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(user_agent = userAgents())
            page = await context.new_page()
            
            # Navigate to the category URL.
            await page.goto(category_url)            

            # Determine the country from the URL.
            country = await check_domain(category_url)

            # Print a message indicating that the automation has started.
            print(f"""Initiating the automation | Powered by Playwright.\n
                      Daraz {country}
                  """)
            
            # Get the name of the category being scraped.
            self.category = await self.category_name(category_url)

            # Get the total number of pages in the category.
            page_number_elements = await page.query_selector_all(self.yaml_me['last_page_number'])            
            self.last_page_number = int(await (page_number_elements[len(page_number_elements)-2]).get_attribute('title'))            
            
            # Print a message indicating the category and the number pages to be scraped.
            print(f"Category: {self.category} | Number of pages: {self.last_page_number}")

            # Get the "next page" button.
            next_page = await page.query_selector(self.yaml_me['next_page_button'])            

            # Loop through the page using the "next page button".
            for count in range(1, self.last_page_number+1):         
                # Get the main content section of the page.       
                main_contents = await page.query_selector_all(self.yaml_me['category_main_contents'])                

                # Print a message indicating the current page being scraped.
                print(f"Scraping page | {count}")
                await page.wait_for_timeout(timeout=2*1000)

                # Loop through the products on the current page and extract their data.
                for content in main_contents:
                    product = await self.catchClause.text(content.query_selector(self.yaml_me['category_product_names']))
                    print(f"Scraping product | {product}.")
                    await page.wait_for_timeout(timeout=0.2*1000)
                    datas = {
                        "Name": product,
                        "Original price": await self.catchClause.text(content.query_selector(self.yaml_me['category_discount_price'])),
                        "Discount price": await self.catchClause.text(content.query_selector(self.yaml_me['category_og_price'])),
                        "Discount rate": (await self.catchClause.text(content.query_selector(self.yaml_me['category_discount_rate']))).replace("-", ""),
                        "Hyperlink": f"""https:{await self.catchClause.attributes(content.query_selector(self.yaml_me['category_product_links']), 'href')}""",
                        "Image": await self.catchClause.attributes(content.query_selector(self.yaml_me['category_product_image']), 'src') ,
                    }                    
                    daraz_dicts.append(datas)
                
                # Click the "next page" button to go to the next page.
                try:
                    await page.wait_for_selector(self.yaml_me['next_page_button'], timeout = 10000)
                    await next_page.click()
                except PlaywrightTimeoutError: 
                    # If the "next page" button cannot be found, there are no more pages to scrape.
                    # Print a message indicating the error and break out of the loop.               
                    print(f"Content loading error at page number {count}. There are no result found beyond this page. Scraper is exiting......")
                    break
                
                # Wait for a short time before scraping the next page.
                await page.wait_for_timeout(timeout=2*1000)                                    
            
            # Close the browser.
            await browser.close() 

        # Now exporting to excel database:
        df = pd.DataFrame(data = daraz_dicts)
        df.to_excel(f"""Daraz database//{self.category} database-{country}.xlsx""", index = False)      
        print(f"{self.category} saved.")       
            
 