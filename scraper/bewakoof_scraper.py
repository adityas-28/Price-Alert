from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
from pathlib import Path

ROOT_DIR = str(Path(__file__).resolve().parents[1])
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from backend.app.db.connection import upsert_product

# Setup headless Chrome
options = Options()
options.add_argument("--headless=new")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

driver = webdriver.Chrome(options=options)

try:
    url = "https://www.bewakoof.com/p/mens-green-navy-blue-oversized-hoodies"
    driver.get(url)

    # Wait for price element to load
    price_elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/main/main/div[1]/div[1]/section[2]/div[1]/div[2]/div[1]/div/div[1]/h3'))
    )
    price = price_elem.text.replace("₹", "").replace(",", "").strip()

    # Example: Product name XPath
    name_elem = driver.find_element(By.XPATH, '//*[@id="__next"]/main/main/div[1]/div[1]/section[2]/div[1]/div[1]/span')
    product_name = name_elem.text.strip()
    print(product_name)
    
    # asin like identifier 
    asin = url.split("/")[-1]
	
    # MRP XPath
    # mrp_elem = driver.find_element(By.XPATH, '//*[@id="__next"]/main/main/div[1]/div[1]/section[2]/div[1]/div[2]/div[1]/div/div[1]/span[1]')
    # mrp = mrp_elem.text.replace("₹", "").replace(",", "").strip()

    # Discount XPath
    # discount_elem = driver.find_element(By.XPATH, '//*[@id="__next"]/main/main/div[1]/div[1]/section[2]/div[1]/div[2]/div[1]/div/div[1]/span[2]')
    # discount = discount_elem.text.strip()

    data = {
        "ASIN": [asin],
        "Product Name": [product_name],
        "Price": [price],
        # "MRP": [mrp],
        # "Discount": [discount],
        "URL": [url]
    }
    
    if asin and product_name and price and url is not None:
        upserted = upsert_product({
            "asin": asin,
            "name": product_name,
            "url": url,
            "price": price,
        })
        if upserted:
            print("Upserted:", upserted.get("asin"), upserted.get("last_updated"))
        else:
            print("Upsert failed; no document returned")
    else:
        print("Failed to parse asin, title or price; skipping DB upsert")

finally:
    driver.quit()