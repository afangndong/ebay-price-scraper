from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=chrome_options)

def scrape_ebay(product_name):
    driver = setup_driver()
    try:
        search_url = f"https://www.ebay.de/sch/i.html?_nkw={product_name.replace(' ', '+')}"
        driver.get(search_url)
        time.sleep(3)
        
        products = []
        items = driver.find_elements(By.CSS_SELECTOR, ".s-item")
        
        for item in items[:10]:
            try:
                title = item.find_element(By.CSS_SELECTOR, ".s-item__title").text
                price = item.find_element(By.CSS_SELECTOR, ".s-item__price").text
                link = item.find_element(By.CSS_SELECTOR, ".s-item__link").get_attribute("href")
                
                products.append({
                    'title': title,
                    'price': price,
                    'link': link,
                    'platform': 'eBay'
                })
            except:
                continue
                
        return products
    finally:
        driver.quit()
