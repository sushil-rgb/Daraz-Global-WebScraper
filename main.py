from tools.functionalities import verifyDarazURL
from scrapers.daraz_scraper import Daraz
import asyncio
import time


if __name__ == "__main__":


    async def main():
        """
        Asynchronous function to execute the web scraping and data export process.
        """
        start_time = time.time()
        url = "https://www.daraz.com.np/air-conditioners/"
        if verifyDarazURL(url):
            print("Invalid link. Please enter a valid Daraz product category link.")
        else:
            daraz = Daraz(url)
            mongo_db = True  # Set this to False if you want to export to an Excel sheet
            if mongo_db:
                await daraz.export_to_mongo()
            else:
                await daraz.export_to_sheet()
            total_time = round((time.time() - start_time), 2)
            time_in_secs = round(total_time, 2)
            time_in_mins = round((total_time / 60), 2)
            print(f"Took {time_in_secs} seconds. | {time_in_mins} minutes.")


    asyncio.run(main())


