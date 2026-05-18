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


def main():
    logger.info("Starting parser script...")
    try_login()
    init_csv()
    
    with open("products_codes.txt", "r", encoding="utf-8") as f:
        product_codes = f.read().splitlines()

    logger.info(f"Loaded {len(product_codes)} product codes to process.")

    for i, code in enumerate(product_codes, 1):
        logger.info(f"Processing {i}/{len(product_codes)}: {code}")
        start_pars(code)
    
    close_csv()
    logger.info("Finished processing all codes.")

if __name__ == "__main__":
    main()