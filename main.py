from tools_in_classes import Scraper
import pandas as pd
import winsound
import time
import itertools
import concurrent.futures


# track the timer:
start_time = time.time()
time_interval = 0.5

# Split URL update:
main_daraz_url = ""
split_main_url = main_daraz_url.split("?")

category_name = Scraper(main_daraz_url).product_category_name()

last_page = Scraper(main_daraz_url).last_page()


url_lists = []
for index in range(1, last_page+1):
    daraz_url = f"?page={str(index)}&".join(split_main_url)
    url_lists.append(daraz_url)

print(f'Total pages to scrape | {len(url_lists)} pages.')


all_daraz_product_links = []
all_product_names = []
for count in range(len(url_lists)+1):
    try:
        print(f"Scraping page number | {count+1}.....")
        daraz = Scraper(url_lists[count])
        all_daraz_product_links.extend(daraz.selenium_scraper())
        all_product_names.extend(daraz.product_names())
    except IndexError:
        break


d = {f"Product Names": all_product_names, f"Product Links": all_daraz_product_links}
df = pd.DataFrame(data=d)
df.to_excel(f"{category_name}.xlsx", index=False)
df.to_json(f"{category_name}.json", indent=4)

winsound.PlaySound('notification.mp3', winsound.SND_FILENAME)

time_took = time.time() - start_time
time_in_seconds = round(time_took, 2)
time_in_minutes = round(time_in_seconds/60, 2)
print(f'Took {time_in_seconds} seconds.....')
print(f"Took {time_in_minutes} minutes.....")
