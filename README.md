# Daraz Scraper
This is a Python application that scrapes product details from <a href = "https://www.daraz.com.np/">Daraz</a> - a popular online marketplace in Nepal. The application uses asyncio for asynchronous programming and makes use of the Requests-HTML library for HTML parsing and beautifulsoup4 for scraping.

# Installation
1. Clone the repository to your local machine:
```python
git clone https://github.com/<usernam>/<repository-name>.git
```
2. Open your terminal and navigate to the project directory:
```python
cd daraz-scraper
```
3. Create a viertual environment for the project using **venv**:
```python
python -m venv environment
```
4. Activate the virtual environment:
```python
environment/scripts/activate
```
5. Install the required dependencies:
```python
pip install -r requirements.txt
```
5. Run the **`main.py`** file:
```python
python main.py
```

# Daraz Class
The **`Daraz` class is the main class of this scraper. It has the following methods:**

### product_details(category_url)
This methord takes a category URL as input and returns the name of the category. It uses the **`product_url`** to scrape the product page and extract product name, discount price, original price, store name, store link, product link, and image link.
### scrapeMe(cateogory_url)
This method is the main method of the **`Daraz`** class. It takes a category URL as input, scrapes all the product URLs in that category, and calls the **`product_details`** method to
extract the product details. It then exports the data to an Excel database with the name of the category.


# Example Usage
## product_details() method:
```python
Enter a Daraz product URL:> https://www.daraz.com.np/products/sony-playstation-5-digital-edition-console-i200366811-s1419520534.html

{'Name': 'Sony PlayStation 5 Digital Edition Console',
 'Discount price': 'Rs. 67,499',
 'Original price': 'Rs. 69,999',
 'Sold by': 'Sony Authorized Store',
 'Store link': 'https://www.daraz.com.np/shop/sony-official-store',
 'Hyperlink': 'https://www.daraz.com.np/products/sony-playstation-5-digital-edition-console-i200366811-s1419520534.html',
 'Image': 'https://static-01.daraz.com.np/p/17df7b25c4fa18e8d35f394cfe04ef06.jpg'}

Took 11.95 seconds. | 0.2 minutes.
```

## scrapeMe() method:
```python
import asyncio
from daraz_scraper import Daraz

async def main():
    url = "https://www.daraz.pk/womens-sandals/?page=1"
    daraz = Daraz()
    await daraz.scrapeMe(url)
    print("Scraping finished!")

if __name__ == "__main__":
    asyncio.run(main())
```
In this example, we create a Daraz object, and call its scrapeMe() method with a URL for a Daraz category page for women's sandals. The scrapeMe() method will scrape all the product information from all pages of the category and save it to an Excel file. Once the scraping is finished, the program will print "Scraping finished!" to the console.

Note that since scrapeMe() is an asynchronous method, we need to use asyncio.run() to run it.

# Contributing
If you find any bugs or issues with the scraper, feel free to open an issue or submit a pull request. Contributions are always welcome!

# License
This project is licensed under the MIT license.