from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
from pathlib import Path

ROOT_DIR = str(Path(__file__).resolve().parents[2])
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from src.db.connection import upsert_product
def scrap_tanishq(url: str):
    # Setup headless Chrome
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)

        # Wait for price element (mobile view div)
        price_elem = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='d-lg-none mx-auto']//p[contains(@class, 'pdp-product-main-sale-price')]"))
        )
        price_text = price_elem.text.strip()
        price = price_text.replace("₹", "").replace(",", "").replace(" ", "")

        # Try product name (Tanishq product title class)
        try:
            name_elem = driver.find_element(By.XPATH, "//h1[contains(@class, 'pdp-product-title')]")
            product_name = name_elem.text.strip()
        except:
            # Fallback to meta tag
            name_elem = driver.find_element(By.XPATH, "//meta[@property='og:title']")
            product_name = name_elem.get_attribute("content")#.strip()

        print(f"Product: {product_name}")
        print(f"Price: ₹{price}")

        # Create ASIN-like identifier
        asin = url.split("/")[-1] or url.split("/")[-2]

        # Prepare data dict
        data = {
            "ASIN": [asin],
            "Product Name": [product_name],
            "Price": [price],
            "URL": [url],
        }

        # Save to database
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
            print("Failed to parse asin, title, or price; skipping DB upsert")

        return data

    except Exception as e:
        print(f"Error during scraping: {str(e)}")
        raise e

    finally:
        driver.quit()


# Example usage:
# url = "https://www.tanishq.co.in/product/bloom-blaze-diamond-ring-50e5b1fck2a02.html?lang=en_IN"
# scrap_tanishq(url)
