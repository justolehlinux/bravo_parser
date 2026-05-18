import logging
from bal_pars.cvs_point import CSV_FIELDS, write_barcode_row

logger = logging.getLogger(__name__)

def barcode_parser(code, barcode_section):
    if barcode_section:
        logger.debug(f"Parsing barcodes for product {code}")
        codes = {field: "" for field in CSV_FIELDS}

        for i, dd in enumerate(barcode_section.find_all("dd")[:4]):
            codes["product_code"] = code
            text = dd.get_text(strip=True)
            codes[f"num_{i}"], codes[f"product_barcode_{i}"] = text.split(" ")
            codes[f"num_{i}"] = codes[f"num_{i}"].strip("()")
        
        write_barcode_row(codes)
        
        return codes["product_barcode_0"]
