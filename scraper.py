from daraz_tools_oop import DarazIndivLinkScraper, DarazScraper, FlattenedLists, SplitDarazURL, CreatePathDirectory, AlertEmail
import time
import winsound
import pandas as pd
import traceback
import os


start_time = time.time()


product_url = "https://www.daraz.com.np/laundry-cleaning/?spm=a2a0e.searchlistcategory.breadcrumb.3.62cb20f9Qh8p4F"

total_pages = DarazScraper(product_url).number_of_pages()
list_of_urls = SplitDarazURL(product_url).split(total_pages)
product_category = DarazScraper(product_url).category_name()

print(f"Total pages | {total_pages}")

# Setting up the directory for downloaded databases:
folder_name = f"Daraz {product_category}" 
CreatePathDirectory(folder_name).createFolder()


store_all_datas_in_lists = FlattenedLists().flat([DarazScraper(url).scrapeLinksNamesPrices() for url in list_of_urls])
try:
    all_daraz_product_links = store_all_datas_in_lists[0]
    all_daraz_product_names = store_all_datas_in_lists[1]
    all_daraz_product_prices = store_all_datas_in_lists[2]
except Exception as e:
    traceback.print_exc()


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
SUBJECT = "ALERT EMAIL!!!!!!"
CONTENT = f"Hello Sushil bro! {folder_name} database is saved."


AlertEmail(EMAIL_ADDRESS, EMAIL_PASSWORD).sendAlert(RECEIVERS, SUBJECT, CONTENT)


total_time = round(time.time()-start_time, 2)
time_in_secs = round(total_time)
time_in_mins = round(total_time/60)

print(f"{time_in_secs} seconds")
print(f"{time_in_mins} minutes.")
print(f"Saved | {folder_name}")


# Play the sound after the completion of Scraping process:
winsound.PlaySound('notification.mp3', winsound.SND_FILENAME)

