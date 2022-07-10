test = "https://www.daraz.com.np/laptops/?spm=a2a0e.searchlistcategory.cate_5.4.1eec5884kIeql2"
sp_lit = test.split("?")
new_url = f"?page=10&".join(sp_lit)
print(new_url)
