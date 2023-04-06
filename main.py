import time 
import asyncio
from functionalities.tools import verifyDarazURL
from scrapersFunctionalities.scraper import Daraz


async def main():
    url = input("Enter a Daraz product URL:> ")
    if await verifyDarazURL(url):
        print("Invalid link. Please enter a valid Daraz product category link.")
    else:
        results = await Daraz().scrapeMe(url)
        # results = await Daraz().product_details(url)
        return results


if __name__ == "__main__":
    start_time = time.time()    

    print(asyncio.run(main()))

    total_time = round((time.time() - start_time), 2)
    time_in_secs = round(total_time, 2)
    time_in_mins = round((total_time / 60), 2)

    print(f"Took {time_in_secs} seconds. | {time_in_mins} minutes.")

