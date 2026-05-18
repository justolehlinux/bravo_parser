import logging
from bs4 import BeautifulSoup
from bal_pars.cvs_point import write_prod_row
from bal_pars.config import BASE_URL, CSV_PROD
from bal_pars.barcodeparser import barcode_parser

logger = logging.getLogger(__name__)

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
        logger.warning(f"Product {code}: Page layout unexpected or product not found (no title).")
        return None, None # Return None for data and None for soup

    data = {field: "" for field in CSV_PROD}
    data["seller_ids/product_code"] = code
    data["name"] = title_tag.get_text(strip=True)
    price_tag = soup.select_one("span.price")
    price = price_tag.get_text(strip=True).split(" ")[0] if price_tag else ""
    data["seller_ids/price"] = float(price.replace(",", ".")) if price else "" # type: ignore
    KEY_MAPPING = {
        "код": "seller_ids/product_code",
        "подкатегория": "categ_id",
        "категория": "category",
        "продажная единица": "sales_unit",
        "единица": "sales_unit",
        "вес брутто": "weight"
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
            
            if key == "вес брутто":
                val = '{0:.2f}'.format(float(val.split(" ")[0].replace(",", ".")))
            if val == "ШТ": val = "Единицы"
            if val == "ШТ": val = "Единицы"
            
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
            elif "минимальная покупка" in key:
                data["seller_ids/min_qty"] = val.split(" ")[0]
            
    
    data["purchase_ok"] = True
    data["active"] = True
    data["is_storable"] = True
    data["available_in_pos"] = True
    data["seller_ids/partner_id"] = "BALKANICA DISTRAL SOCIEDAD LIMITADA"
    data["sale_ok"] = True


    barcode_section = soup.select_one("#h2tab4")
    data["barcode"] = barcode_parser(code, barcode_section)
    write_prod_row(data)  # Assuming prod_writer is defined globally or passed as an argument
    logger.info(f"Successfully parsed and saved product: {code}")
