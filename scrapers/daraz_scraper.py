from tools.functionalities import userAgents, TryExcept, yamlMe, check_domain, random_interval, create_path, verifyDarazURL
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from bs4 import BeautifulSoup
import pymongo as mong
import pandas as pd
import requests
import re


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

    def __init__(self, base_url):
        """
        Initializes the headers, catchClause and yaml_me attributes of the class.
        """
        self.base_url = base_url
        self.headers = {"User-Agent": userAgents()}
        self.catchClause = TryExcept()
        self.yaml_me = yamlMe('selectors')

    async def category_name(self):
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
        req = requests.get(self.base_url, headers=self.headers)
        soup = BeautifulSoup(req.content, 'lxml')
        category = [cate.text.strip() for cate in soup.find('ul', class_='breadcrumb').find_all('li', class_='breadcrumb_item')][-1]
        name = [nam.strip() for nam in re.split(r'[,/]', category)]
        return ' '.join(name)

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

    async def scrape_datas(self):
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
            await page.goto(self.base_url)
            # Determine the country from the URL.
            country = await check_domain(self.base_url)

            print(f"""Initiating the automation | Powered by Playwright.\n
                    Daraz {country}
                """)
            # Get the name of the category being scraped.
            category = await self.category_name()
            # Get the total number of pages in the category.
            page_number_elements = await page.query_selector_all(self.yaml_me['last_page_number'])
            self.last_page_number = int(await (page_number_elements[len(page_number_elements)-2]).get_attribute('title'))

            print(f"Category: {category} | Number of pages: {self.last_page_number}")
            # Get the "next page" button.
            next_page = await page.query_selector(self.yaml_me['next_page_button'])

            # Loop through the page using the "next page button".
            for count in range(1, self.last_page_number+1):
                # Get the main content section of the page.
                main_contents = await page.query_selector_all(self.yaml_me['category_main_contents'])
                # Print a message indicating the current page being scraped.
                print(f"\nScraping page | {count}")
                # Wait for a short time before scraping the next page.
                await page.wait_for_timeout(timeout=random_interval(5)*1000)
                # Loop through the products on the current page and extract their data.
                for content in main_contents:
                    product = await self.catchClause.text(content.query_selector(self.yaml_me['category_product_names']))
                    print(f"Scraping product | {product}.")
                    try:
                        og_price = float(re.sub(r'[Rs.,]', '', await ( await content.query_selector(self.yaml_me['category_og_price'])).inner_text()).strip())
                    except Exception as e:
                        og_price = "N/A"
                    try:
                        dc_price = float(re.sub(r'[Rs.,]', '', await ( await content.query_selector(self.yaml_me['category_discount_price'])).inner_text()).strip())
                    except Exception as e:
                        dc_price = "N/A"
                    try:
                        dc_rate = float(re.sub(r'[-%]', '', await (await content.query_selector(self.yaml_me['category_discount_rate'])).inner_text()).strip())
                    except Exception as e:
                        dc_rate = "N/A"
                    await page.wait_for_timeout(timeout=0.03*1000)
                    datas = {
                        "Name": product,
                        "Original price": og_price,
                        "Discount price": dc_price,
                        "Discount rate": dc_rate,
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
            # Close the browser.
            await browser.close()
        return daraz_dicts

    async def export_to_mongo(self):
        """
            Asynchronously exports scraped data to a MongoDB database.

            Steps:
            1. Obtains the collection name by calling the `category_name()` method asynchronously.
            2. Establishes a connection to the local MongoDB server on port 27017.
            3. Selects the 'daraz' database from the client.
            4. Fetches data by calling the `scrape_datas()` method asynchronously.
            5. Inserts the fetched data into the specified collection in the database using `insert_many()`.
            6. Closes the MongoDB client.

            Returns:
                pymongo.results.InsertManyResult: The result object containing information about the insertion operation.
        """
        collection_name = await self.category_name()
        client = mong.MongoClient('mongodb://localhost:27017/')
        db = client['daraz']
        collection = db[collection_name]
        print(f"Collecting {collection_name} to Mongo database.")
        datas = await self.scrape_datas()
        result = collection.insert_many(datas)
        client.close()
        return result

    async def export_to_sheet(self):
        """
            Asynchronously exports scraped data to an Excel sheet.

            Steps:
            1. Obtains the file name by calling the `category_name()` method asynchronously.
            2. Creates a 'Daraz database' directory if it doesn't exist.
            3. Fetches data by calling the `scrape_datas()` method asynchronously.
            4. Converts the data into a Pandas DataFrame.
            5. Writes the DataFrame to an Excel file located at 'Daraz database/{file_name}.xlsx'.

            Note:
                The function assumes that the `scrape_datas()` method returns a list of dictionaries, each representing a row of data.

            Returns:
                None
        """
        file_name = await self.category_name()
        print(f"Exporting {file_name} to Excel database.")
        create_path('Daraz database')
        datas = await self.scrape_datas()
        df = pd.DataFrame(datas)
        df.to_excel(f"Daraz database//{file_name}.xlsx", index = False)


