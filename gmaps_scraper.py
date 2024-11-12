from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import re

class GMapsScraper:
    def __init__(self):
        # Initialize Chrome driver
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        
    def search_business(self, query):
        """Search for a business on Google Maps"""
        self.driver.get("https://www.google.com/maps")
        
        # Wait for search box and enter query
        search_box = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "searchboxinput"))
        )
        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys(Keys.ENTER)
        
        # Wait for results to load
        time.sleep(3)
        
    def get_business_details(self):
        """Extract business details from the current listing"""
        try:
            # Wait for business information panel to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.rogA2c"))
            )
            
            # Get phone number
            phone = None
            try:
                phone_elements = self.driver.find_elements(By.CSS_SELECTOR, 'button[data-tooltip="Copy phone number"]')
                if phone_elements:
                    phone = phone_elements[0].get_attribute('aria-label').replace('Phone:', '').strip()
            except NoSuchElementException:
                pass

            # Get email
            email = None
            try:
                # Click "More" button if it exists
                more_button = self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Expand more"]')
                more_button.click()
                time.sleep(1)
                
                # Look for email in the expanded information
                elements = self.driver.find_elements(By.CSS_SELECTOR, 'a[data-item-id="email"]')
                if elements:
                    email = elements[0].get_attribute('href').replace('mailto:', '')
            except NoSuchElementException:
                pass

            return {
                'phone': phone,
                'email': email
            }
            
        except TimeoutException:
            print("Timeout waiting for business details to load")
            return None
        
    def close(self):
        """Close the browser"""
        self.driver.quit()

def main():
    # Example usage
    scraper = GMapsScraper()
    
    try:
        # Search for a business
        business_name = input("Enter business name to search: ")
        scraper.search_business(business_name)
        
        # Get and print business details
        details = scraper.get_business_details()
        if details:
            print("\nBusiness Details:")
            print(f"Phone: {details['phone']}")
            print(f"Email: {details['email']}")
        else:
            print("Could not find business details")
            
    finally:
        scraper.close()

if __name__ == "__main__":
    main() 