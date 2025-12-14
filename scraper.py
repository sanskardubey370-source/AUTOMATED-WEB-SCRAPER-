from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def get_dynamic_data(url):
    """
    Launches a headless browser, waits for content, and returns parsed data.
    """
    # Configure Headless Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run without UI
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize Driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)

        # Wait up to 10 seconds for a specific element to load (Adjust class name as needed)
        # This is crucial for dynamic sites (React/Angular/Vue)
        wait = WebDriverWait(driver, 10)
        # Example: Waiting for the product title to appear
        # wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product-title")))

        # Pass page source to BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # --- EXTRACTION LOGIC (Modify selectors based on target site) ---
        # Example logic for a generic e-commerce site:
        try:
            name = soup.find('h1').text.strip()
        except AttributeError:
            name = "Unknown Product"

        try:
            price_text = soup.find('span', class_='price').text.strip()
            # Clean currency symbols (e.g., "$19.99" -> 19.99)
            price = float(''.join(filter(lambda x: x.isdigit() or x == '.', price_text)))
        except AttributeError:
            price = 0.0

        return {
            "name": name, 
            "price": price, 
            "url": url
        }

    except Exception as e:
        print(f"Scraping Error: {e}")
        return None
    finally:
        driver.quit()  # Always close the browser to prevent memory leaks