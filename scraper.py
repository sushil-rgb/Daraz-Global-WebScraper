from playwright.sync_api import sync_playwright
from daraz_tools_oop import AlertEmail, DarazIndivLinkScraper, DarazScraper, FlattenedLists, SplitDarazURL, CreatePathDirectory, alertEmail
import time
import winsound
import pandas as pd
import os
import shutil
import sys
import smtplib
import asynchat
import os
import smtplib
from email.message import EmailMessage


start_time = time.time()

product_url = "https://www.daraz.com.np/sp-nutrition/?spm=a2a0e.searchlistcategory.cate_11.10.12f23969UiCQpj"

total_pages = DarazScraper(product_url).number_of_pages()
list_of_urls = SplitDarazURL(product_url).split(total_pages)
product_category = DarazScraper(product_url).category_name()

print(f"Total pages | {total_pages}")

# Setting up the directory for downloaded databases:
folder_name = f"Daraz {product_category}" 
CreatePathDirectory(folder_name).createFolder()


all_daraz_product_links = FlattenedLists().flat([DarazScraper(url).all_product_links() for url in list_of_urls])
all_daraz_product_names = FlattenedLists().flat([DarazScraper(url).all_product_names() for url in list_of_urls])
all_daraz_product_prices = FlattenedLists().flat([DarazScraper(url).all_product_prices() for url in list_of_urls])



d = {
    "Names": all_daraz_product_names,
    "Prices": all_daraz_product_prices,
    "Links": all_daraz_product_links
}

df = pd.DataFrame(d)

df.to_json(f"{os.getcwd()}//{folder_name}//Daraz {product_category} database.json", indent=4)
df.to_excel(f"{os.getcwd()}//{folder_name}//{product_category} database.xlsx", index=False)


# Sender address:
EMAIL_ADDRESS = os.environ.get("USER_EMAIL")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
RECEIVERS = ['rockin_sushil@hotmail.com', 'gunz19able@gmail.com']
content = f"Hello Sushil! {folder_name} database."
subject = "ALERT EMAIL!!!!!!"

AlertEmail(EMAIL_ADDRESS, EMAIL_PASSWORD, RECEIVERS, content, subject)



total_time = round(time.time()-start_time, 2)
time_in_secs = round(total_time)
time_in_mins = round(total_time/60)

print(f"{time_in_secs} seconds")
print(f"{time_in_mins} minutes.")
print(f"Saved | {folder_name}")



# Play the sound after the completion of Scraping process:
winsound.PlaySound('notification.mp3', winsound.SND_FILENAME)



