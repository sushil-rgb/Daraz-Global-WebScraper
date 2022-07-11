from tools_in_classes import Scraper
import pandas as pd
import winsound
import time
import itertools


# track the timer:
start_time = time.time()
time_interval = 1

# Paste the Daraz url below:
main_daraz_url = "https://www.daraz.com.np/clothing-men-underwear/?spm=a2a0e.11779170.cate_3.6.287d2d2bqqSBhD"
split_main_url = main_daraz_url.split("?")

print(f"Scraping category name....")
category_name = Scraper(main_daraz_url).product_category_name()
print(f"Category | {category_name}")

print("Scraping last page.....")
# Paste the url below and run the scraper:
last_page = Scraper(main_daraz_url).last_page()
print(f"Last page | {last_page}")


url_lists = []
for index in range(1, last_page+1):
    daraz_url = f"?page={str(index)}&".join(split_main_url)
    url_lists.append(daraz_url)

print(f'Total pages to scrape | {len(url_lists)} pages.')


all_daraz_product_links = []
all_product_names = []
all_product_prices = []
for count in range(len(url_lists)+1):
    try:
        print(f"Scraping page number | {count+1}.....")
        time.sleep(time_interval)
        daraz = Scraper(url_lists[count])
        all_daraz_product_links.extend(daraz.selenium_scraper())
        all_product_names.extend(daraz.product_names())
        all_product_prices.extend(daraz.product_price())
    except IndexError:
        break


d = {f"Product Names": all_product_names, f"Product Prices": all_product_prices, f"Product Links": all_daraz_product_links}
df = pd.DataFrame(data=d)
df.to_json(f"{category_name}.json", indent=4)
df.to_excel(f"{category_name}.xlsx", index=False)

winsound.PlaySound('notification.mp3', winsound.SND_FILENAME)

time_took = time.time() - start_time
time_in_seconds = round(time_took, 2)
time_in_minutes = round(time_in_seconds/60, 2)
print(f'Took {time_in_seconds} seconds.....')
print(f"Took {time_in_minutes} minutes.....")
