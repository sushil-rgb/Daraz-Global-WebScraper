# Daraz Scraper
This is a Python application that scrapes product details from <a href = "https://www.daraz.com.np/">Daraz</a> - a popular online marketplace in South Asia. The application uses asyncio for asynchronous programming and makes use of the Requests-HTML library for HTML parsing and beautifulsoup4 for scraping.
**This scraper is designed to scrape product details from the online marketplaces of Sri Lanka, Pakistan, Bangladesh, and Nepal**

# New Addition - Exporting to MongoDB Database
-------------------------------------------

The Daraz Scraper now includes the option to export the scraped data to a MongoDB database. To utilize this feature, follow these steps:

1. Make sure you have MongoDB installed and running on your local machine or on a remote server. If you don't have MongoDB installed, you can download it from the official MongoDB website (https://www.mongodb.com/try/download) and follow the installation instructions for your operating system.

2. Ensure that the `pymongo` library is installed in your virtual environment. If it's not already installed, you can install it using pip:
   ```
   pip install pymongo
   ```

3. In the `main.py` file, you'll see the following block of code:

   ```python
   if __name__ == "__main__":
       async def main():
           start_time = time.time()
           url = "https://www.daraz.com.np/air-conditioners/"
           if verifyDarazURL(url):
               print("Invalid link. Please enter a valid Daraz product category link.")
           else:
               daraz = Daraz(url)
               mongo_db = True
               if mongo_db:
                   await daraz.export_to_mongo()
               else:
                   await daraz.export_to_sheet()
               total_time = round((time.time() - start_time), 2)
               time_in_secs = round(total_time, 2)
               time_in_mins = round((total_time / 60), 2)
               print(f"Took {time_in_secs} seconds. | {time_in_mins} minutes.")


       print(asyncio.run(main()))
   ```
   Run the **`main.py`** file:
```python
python main.py
```

4. Set the `url` variable to the desired Daraz product category URL that you want to scrape.<br>

5. The `mongo_db` variable controls whether the data will be exported to a MongoDB database or an Excel database. If `mongo_db` is set to `True`, the data will be exported to a MongoDB database. If `mongo_db` is set to `False`, the data will be exported to an Excel file.<br>

6. When `mongo_db` is `True`, the `export_to_mongo()` method of the Daraz class is called to export the data to the MongoDB database. Ensure that your MongoDB connection details are properly set up within the Daraz class.<br>

7. If `mongo_db` is set to `False`, the `export_to_sheet()` method will be called to export the data to an Excel file, as in the original version of the scraper.<br>

With these steps completed, the scraper will scrape the data from the specified Daraz product category URL and export it to the selected database, either MongoDB or Excel.<br>

Note: Please ensure that you have the necessary permissions and credentials to access the MongoDB database, and adjust the MongoDB connection details in the `export_to_mongo()` method of the Daraz class according to your setup.<br>

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

```
In this example, we create a Daraz object, and call its scrapeMe() method with a URL for a Daraz category page for women's sandals. The scrapeMe() method will scrape all the product information from all pages of the category and save it to an Excel file. Once the scraping is finished, the program will print "Scraping finished!" to the console.

Note that since scrapeMe() is an asynchronous method, we need to use asyncio.run() to run it.

# Contributing
If you find any bugs or issues with the scraper, feel free to open an issue or submit a pull request. Contributions are always welcome!

# License
This project is licensed under the MIT license.