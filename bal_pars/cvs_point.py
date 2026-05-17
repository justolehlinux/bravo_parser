import csv
from typing import Dict, Any
from bal_pars.config import CSV_PROD, CSV_FIELDS

# Внутренние переменные модуля (скрыты от других файлов)
_file_prod = None
_writer_prod = None

_file_barcode = None
_writer_barcode = None


def init_csv(prod_path: str = "product.csv", barcode_path: str = "barcode_parser.csv"):
    """Вызывается ОДИН раз в главном файле (main.py) при старте."""
    global _file_prod, _writer_prod, _file_barcode, _writer_barcode
    
    # Инициализация продуктов
    _file_prod = open(prod_path, "w", newline="", encoding="utf-8")
    _writer_prod = csv.DictWriter(_file_prod, fieldnames=CSV_PROD)
    _writer_prod.writeheader()
    _file_prod.flush()
    
    # Инициализация штрихкодов
    _file_barcode = open(barcode_path, "w", newline="", encoding="utf-8")
    _writer_barcode = csv.DictWriter(_file_barcode, fieldnames=CSV_FIELDS)
    _writer_barcode.writeheader()
    _file_barcode.flush()


# --- ЭЛЕГАНТНЫЕ ФУНКЦИИ ЗАПИСИ (Их импортируют другие файлы) ---

def write_prod_row(row: Dict[str, Any]):
    """Записывает продукт. Не требует передачи объекта."""
    if _writer_prod is None:
        raise RuntimeError("CSV система не инициализирована! Сначала вызовите init_csv()")
    
    _writer_prod.writerow(row)
    _file_prod.flush()  # Теперь работает корректно, так как есть ссылка на файл


def write_barcode_row(row: Dict[str, Any]):
    """Записывает штрихкод. Не требует передачи объекта."""
    if _writer_barcode is None:
        raise RuntimeError("CSV система не инициализирована! Сначала вызовите init_csv()")
    
    _writer_barcode.writerow(row)
    _file_barcode.flush()  # Теперь работает корректно


def close_csv():
    """Вызывается в самом конце работы программы, чтобы корректно закрыть файлы."""
    global _file_prod, _file_barcode
    if _file_prod:
        _file_prod.close()
    if _file_barcode:
        _file_barcode.close()