from daraz_tools_oop import DarazScraper

url = "https://www.daraz.com.np/auto-parts-spares/?spm=a2a0e.searchlistcategory.cate_12_5.4.d1654f4f5xaidm"

test_daraz = DarazScraper(url)
print(test_daraz.number_of_pages())