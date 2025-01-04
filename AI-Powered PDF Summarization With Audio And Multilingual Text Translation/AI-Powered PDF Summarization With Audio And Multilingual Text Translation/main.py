from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# this opens the browser using the chrome driver
driver = webdriver.Chrome()  
driver.maximize_window()

# I have used the demo capcha google web page for testing
url = "https://www.google.com/recaptcha/api2/demo"
driver.get(url)
time.sleep(5)

#here i have specified the xpath of the cliclt button for verfy as human request 
WebDriverWait(driver, 10).until(
    EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//iframe[contains(@title, "reCAPTCHA")]')))
# Click the checkbox to "Verify"
checkbox = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '.recaptcha-checkbox-border'))
    )
checkbox.click()
print("Clicked the 'Verify as human' checkbox.")
time.sleep(10)
driver.quit()
"""
conclusion : if we click the verfy as human option using this program , it detects the annomally in the 
                movement of the mouse and redirects us to the  specific images selection part for further
                verification.
            if we visit this link "https://www.google.com/recaptcha/api2/demo" in browser and click it 
                ourself it excepts as human
"""