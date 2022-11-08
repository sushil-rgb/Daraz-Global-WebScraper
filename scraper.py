from daraz_tools_oop import DarazScraper, CreatePathDirectory
import time
import winsound
import pandas as pd
import os


start_time = time.time()


main_url = """https://www.daraz.com.np/early-development-toys/?spm=a2a0e.11779170.cate_9_8.5.287d2d2b4n984L"""
Daraz = DarazScraper(main_url)

product_category = Daraz.category_name()

# Setting up the directory for downloaded databases:
folder_name = f"Daraz {product_category}" 
CreatePathDirectory(folder_name).createFolder()

df = pd.DataFrame(data=Daraz.scrapeMe())
df.to_json(f"{os.getcwd()}//{folder_name}//Daraz {product_category} database.json", indent=4)
df.to_excel(f"{os.getcwd()}//{folder_name}//{product_category} database.xlsx", index=False)

total_time = round(time.time()-start_time, 2)
time_in_secs = round(total_time)
time_in_mins = round(total_time/60)

print(f"{time_in_secs} seconds")
print(f"{time_in_mins} minutes.")
# print(f"Saved | {folder_name}")


# Play the sound after the completion of Scraping process:
winsound.PlaySound('notification.mp3', winsound.SND_FILENAME)

