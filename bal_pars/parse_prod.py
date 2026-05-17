from bs4 import BeautifulSoup
from bal_pars.cvs_point import write_prod_row
from bal_pars.config import BASE_URL, CSV_PROD
from bal_pars.barcodeparser import barcode_parser


def visible_text(element):
    if not element:
        return ""
    style = element.get("style", "")
    style_clean = style.replace(" ", "").lower()
    if "display:none" in style_clean or "visibility:hidden" in style_clean:
        return ""
    return element.get_text(strip=True)

def parse_product(html, code):
    soup = BeautifulSoup(html, "html.parser")
    title_tag = soup.select_one("h3.page-title")
    
    # If there is no title, the product does not exist or the page is invalid.
    # This also catches cases where the page is an error page (like the "Object reference..." page)
    # but returns a 200 OK status.
    if not title_tag or not title_tag.get_text(strip=True):
        return None, None # Return None for data and None for soup

    data = {field: "" for field in CSV_PROD}
    data["product_code"] = code
    data["product_url"] = f"{BASE_URL}?Codigo={code}&IdOportunidad=0"
    data["title"] = title_tag.get_text(strip=True)
    price_tag = soup.select_one("span.price")
    price = price_tag.get_text(strip=True).split(" ")[0] if price_tag else ""
    data["price"] = float(price.replace(",", ".")) if price else "" # type: ignore
    KEY_MAPPING = {
        "код": "product_code",
        "подкатегория": "subcategory",
        "категория": "category",
        "бренд": "brand",
        "марка": "brand",
        "продажная единица": "sales_unit",
        "единица": "sales_unit",
        "вес брутто": "gross_weight",
        "страна": "country"
    }

    # 2. Сама логика парсинга становится очень компактной:
    details_section = soup.select_one("div#h2tab2")
    if details_section:
        for dt in details_section.find_all("dt"):
            dd = dt.find_next_sibling("dd")
            if not dd: 
                continue
                
            key = dt.get_text(strip=True).lower()
            val = dd.get_text(strip=True)
            
            # Ищем, какая подстрока из маппинга содержится в нашем ключе
            for match_word, target_field in KEY_MAPPING.items():
                if match_word in key:
                    data[target_field] = val
                    break

        for p in details_section.find_all("p"):
            text = visible_text(p)
            if not text or ":" not in text: continue
            key, _, val = text.partition(":")
            key = key.strip().lower()
            val = val.strip()
            if "упаковка" in key: data["package"] = val
            elif "содержит" in key: data["contains"] = val
            elif "минимальная покупка" in key: data["minimum_purchase"] = val
            
    # Main image selector
    img = soup.select_one("#product-images .overlay-container img")
    if img:
        src = img.get("src", "")
        if src and not src.startswith("http"):
            src = "https://b2b.balkanicadistral.com/" + src.lstrip("/")
        data["image_url"] = src


    barcode_section = soup.select_one("#h2tab4")
    data["barcode"] = barcode_parser(code, barcode_section)
    write_prod_row(data)  # Assuming prod_writer is defined globally or passed as an argument
