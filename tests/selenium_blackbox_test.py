from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.firefox import GeckoDriverManager
import time
import random

# Use a FIXED username for duplicate test
fixed_username = "blackbox_test_user"

# Generate a unique username for first registration
unique_username = f"blackbox_user_{int(time.time())}_{random.randint(1000,9999)}"

# Firefox WebDriver
service = Service(executable_path=GeckoDriverManager().install())
driver = webdriver.Firefox(service=service)
wait = WebDriverWait(driver, 15)

try:
    # Test 1: Try to register
    print("=== TEST 1: Registration Attempt ===")
    try:
        driver.get("http://localhost:8008/register")
        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(unique_username)
        driver.find_element(By.NAME, "password").send_keys("Password123")
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        time.sleep(2)
        
        print(f"Test 1 Passed: Registered new user '{unique_username}' successfully!")
        
    except Exception as e:
        print(f"Test 1 Failed: {e}")

    # Test 2: Try duplicate registration
    print("\n=== TEST 2: Duplicate Registration Attempt ===")
    try:
        driver.get("http://localhost:8008/register")
        time.sleep(1)
        
        driver.find_element(By.NAME, "username").send_keys(fixed_username)  # Same username
        driver.find_element(By.NAME, "password").send_keys("DifferentPass456")
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        time.sleep(2)
        
        current_url = driver.current_url
        flash_danger = driver.find_elements(By.CSS_SELECTOR, ".flash-danger")
        
        if flash_danger or "/register" in current_url:
            print(f"Test 2 Passed: Duplicate registration correctly rejected for '{fixed_username}'.")
        else:
            print("Test 2 Failed: Duplicate may have been accepted!")

    except Exception as e:
        print(f"Test 2 Failed: {e}")

    print("\n=== BLACK BOX TEST SUMMARY ===")
    print(f"Test Username: {unique_username}")
    print(f"Fixed Test Username for Duplicate: {fixed_username}")
    print("To reset: Delete these users from your database and run again")

finally:
    # Cleanup
    driver.quit()
    print("\nBrowser closed.")
