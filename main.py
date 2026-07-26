import logging
import sys

from bal_pars.init_login import start_pars, try_login
from bal_pars.cvs_point import init_csv, close_csv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

NEW_CODES_PATH = "products_codes_new.txt"
PROCESSED_CODES_PATH = "products_codes.txt"


def load_codes(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            return {line.strip() for line in file if line.strip()}
    except FileNotFoundError:
        return set()


def append_processed_code(path, code):
    needs_separator = False
    try:
        with open(path, "rb") as file:
            file.seek(0, 2)
            if file.tell():
                file.seek(-1, 2)
                needs_separator = file.read(1) not in (b"\n", b"\r")
    except FileNotFoundError:
        pass

    with open(path, "a", encoding="utf-8") as file:
        if needs_separator:
            file.write("\n")
        file.write(f"{code}\n")


def main():
    logger.info("Starting parser script...")
    processed_codes = load_codes(PROCESSED_CODES_PATH)
    queued_codes = load_codes(NEW_CODES_PATH)
    product_codes = sorted(queued_codes - processed_codes)
    skipped_count = len(queued_codes) - len(product_codes)

    logger.info(
        "Loaded %s new product codes to process; skipped %s already processed codes.",
        len(product_codes),
        skipped_count,
    )

    try_login()
    init_csv()
    
    try:
        for i, code in enumerate(product_codes, 1):
            logger.info(f"Processing {i}/{len(product_codes)}: {code}")
            if start_pars(code):
                append_processed_code(PROCESSED_CODES_PATH, code)
                processed_codes.add(code)
                logger.info(f"Added processed product code to {PROCESSED_CODES_PATH}: {code}")
    finally:
        close_csv()
        logger.info("Finished processing all codes.")

if __name__ == "__main__":
    main()
