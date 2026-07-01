import logging
import csv

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def save_to_csv(data, filename):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Business Name", "Phone", "Website"])
        writer.writeheader()
        writer.writerows(data)
    logging.info(f"Successfully saved {len(data)} leads to {filename}")