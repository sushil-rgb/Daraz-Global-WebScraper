import time
import asyncio
from scrapers.daraz_scraper import Daraz
from tools.functionalities import verifyDarazURL


if __name__ == "__main__":
    start_time = time.time()
    url = input("Enter a Daraz product URL:> ")
    if verifyDarazURL(url):
        print("Invalid link. Please enter a valid Daraz product category link.")
    else:
        results = Daraz().scrape_datas(url)
        asyncio.run(results)

    total_time = round((time.time() - start_time), 2)
    time_in_secs = round(total_time, 2)
    time_in_mins = round((total_time / 60), 2)

    print(f"Took {time_in_secs} seconds. | {time_in_mins} minutes.")

