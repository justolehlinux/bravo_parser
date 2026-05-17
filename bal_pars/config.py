import os
# bal_pars/config.py

BASE_URL = "https://b2b.balkanicadistral.com/Producto.aspx"
LOGIN_URL = "https://b2b.balkanicadistral.com/ru"

CSV_PROD = [
    "product_code",
    "title",
    "price",
    "category",
    "subcategory",
    "brand", 
    "sales_unit", 
    "gross_weight", 
    "country", 
    "barcode", 
    "package",
    "image_url", 
    "contains", 
    "minimum_purchase", 
    "product_url"
]

CSV_FIELDS = [
    "product_code", 
    "num_0", 
    "product_barcode_0", 
    "num_1", 
    "product_barcode_1", 
    "num_2", 
    "product_barcode_2", 
    "num_3", 
    "product_barcode_3"]


HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "Connection": "keep-alive",
}

USERNAME = os.environ.get("BALKANICA_USERNAME")
PASSWORD = os.environ.get("BALKANICA_PASSWORD")


BASE_URL = "https://b2b.balkanicadistral.com/Producto.aspx"
LOGIN_URL = "https://b2b.balkanicadistral.com/ru"
# You can also put USERNAME, PASSWORD, and HEADERS in here!