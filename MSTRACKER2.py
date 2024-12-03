from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import quickstart as qs

# # Replace with your WhatsApp Web URL
# whatsapp_web_url = "https://web.whatsapp.com/"

# # Replace with your browser driver path
# driver_path = "path/to/your/chromedriver"

# # Initialize WebDriver
# driver = webdriver.Chrome(driver_path)
# driver.get(whatsapp_web_url)

options = webdriver.ChromeOptions()
options.add_argument(r"user-data-dir=vipulkedia/Documents/Github/python-whatsapp-messages\whatsapp-web\data")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get('https://web.whatsapp.com')

# Wait for QR code scan
time.sleep(10)  # Adjust the wait time as needed

# Function to send a message
def send_message(phone_number, message):
    # Search for the contact
    search_box = driver.find_element(By.XPATH, "//div[@class='x1hx0egp x6ikm8r x1odjw0f x6prxxf x1k6rcq7 x1whj5v']//p[@class='selectable-text copyable-text x15bjb6t x1n2onr6']")
    search_box.click()
    search_box.send_keys(phone_number)
    time.sleep(5)

    driver.find_element(By.XPATH, "//*[@title='"+phone_number+"']").click()
    wait = WebDriverWait(driver, 10)
    message_field = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='x1hx0egp x6ikm8r x1odjw0f x1k6rcq7 x6prxxf']//p[@class='selectable-text copyable-text x15bjb6t x1n2onr6']")))
    # message_field = driver.find_element(By.XPATH, "//div[@class='x1hx0egp x6ikm8r x1odjw0f x1k6rcq7 x6prxxf']//p[@class='selectable-text copyable-text x15bjb6t x1n2onr6']")
    message_field.send_keys(message)
    time.sleep(5)
    message_field = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='x1hx0egp x6ikm8r x1odjw0f x1k6rcq7 x6prxxf']//p[@class='selectable-text copyable-text x15bjb6t x1n2onr6']")))
    message_field.send_keys(Keys.ENTER)
    time.sleep(5)

    # # Click on the contact
    # contact = driver.find_element(By.XPATH, '//span[@title="' + phone_number + '"]')
    # contact.click()
    # time.sleep(2)

    # # Find the text box and send the message
    # text_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="1"]')
    # text_box.send_keys(message)
    # time.sleep(2)

    # # Send the message
    # send_button = driver.find_element(By.XPATH, '//button[@data-icon="send"]')
    # send_button.click()
    # time.sleep(2)


array = qs.main()
# Example usage

for key, value in array.items():

    name = key
    # phone_number = "Twilio Isha"
    message = "Namaskaram "+name+"\nThis is a reminder of the tasks assigned to you that are due soon\n" + '\n'.join([f"{i+1}. {line}" for i, line in enumerate(value)]) + "\nPranam\nMSR Execution Team\n\n"
    # print(message)
    send_message(name, message)

# Close the browser
driver.quit()