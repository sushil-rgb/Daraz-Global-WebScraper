from typing import Type
from daraz_tools_oop import DarazIndivLinkScraper, DarazScraper, FlattenedLists, SplitDarazURL, CreatePathDirectory, AlertEmail
import time
import winsound
import pandas as pd
import traceback
import os


start_time = time.time()


main_url = "https://www.daraz.com.np/fitness-trackers/?spm=a2a0e.searchlistcategory.cate_7_3.3.631638ffhBxRrw"

total_pages = DarazScraper(main_url).number_of_pages()
list_of_urls = SplitDarazURL(main_url).split(total_pages)
product_category = DarazScraper(main_url).category_name()

print(f"Total number of pages | {total_pages}\n-----------------------------")

# Setting up the directory for downloaded databases:
folder_name = f"Daraz {product_category}" 
CreatePathDirectory(folder_name).createFolder()

all_product_names = []
all_product_prices = []
all_product_links = []

for url in list_of_urls:
    all_datas_daraz = DarazScraper(url).scrapeLinksNamesPrices()
    all_product_names.append(all_datas_daraz[0])
    all_product_prices.append(all_datas_daraz[1])
    all_product_links.append(all_datas_daraz[-1])


d = {
    "Names": FlattenedLists().flat(all_product_names),
    "Prices": FlattenedLists().flat(all_product_prices),
    "Links": FlattenedLists().flat(all_product_links)
}

df = pd.DataFrame(d)

df.to_json(f"{os.getcwd()}//{folder_name}//Daraz {product_category} database.json", indent=4)
df.to_excel(f"{os.getcwd()}//{folder_name}//{product_category} database.xlsx", index=False)


# Sender address:
EMAIL_ADDRESS = os.environ.get("USER_EMAIL")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
RECEIVERS = "rockin_sushil@hotmail.com"  # Paste the email address here
SUBJECT = "ALERT EMAIL!!!!!!"
CONTENT = f"Hello Sushil! {folder_name} database is saved."


AlertEmail(EMAIL_ADDRESS, EMAIL_PASSWORD).sendAlert(RECEIVERS, SUBJECT, CONTENT)


total_time = round(time.time()-start_time, 2)
time_in_secs = round(total_time)
time_in_mins = round(total_time/60)

print(f"{time_in_secs} seconds")
print(f"{time_in_mins} minutes.")
print(f"Saved | {folder_name}")


# Play the sound after the completion of Scraping process:
winsound.PlaySound('notification.mp3', winsound.SND_FILENAME)

