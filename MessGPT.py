from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import pyperclip
import os

# Initialize ChromeOptions object
options = Options()

# Add option to disable notifications
options.add_argument("--disable-notifications")

# Add option to exclude logging
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Initialize Chrome browser with the set options
driver = webdriver.Chrome(options=options)

try:
    # Open the Facebook website
    driver.get('http://www.facebook.com')

    # Assume you already have the username and password variables
    username = 'subthinh6@gmail.com'
    password = 'Lovelybaby93'

    # Wait until the 'email' element appears
    wait = WebDriverWait(driver, 10)
    email_box = wait.until(EC.presence_of_element_located((By.NAME, 'email')))

    # Enter the login information
    email_box.send_keys(username)

    # Wait until the 'pass' element appears
    password_box = wait.until(EC.presence_of_element_located((By.NAME, 'pass')))
    password_box.send_keys(password)

    # Click the login button
    login_button = wait.until(EC.element_to_be_clickable((By.NAME, 'login')))
    login_button.click()

    # Path to the file
    file_path = "ReceivedMessages.txt"

    # Check if the file exists, if not, create a new one
    if not os.path.exists(file_path):
        open(file_path, 'w').close()

    last_sent_message = None

    # Search for new messages in the chatbox
    while True:
        try:
            messages = driver.find_elements(By.CSS_SELECTOR, '.x1gslohp.x11i5rnm.x12nagc.x1mh8g0r.x1yc453h.x126k92a')
            for message in messages:
                if '/ask' in message.text:
                    # Read the file to check if the message has been printed before
                    with open(file_path, 'r', encoding='utf-8') as file:
                        if message.text not in file.read():
                            print(message.text)
                            # If the message hasn't been printed before, add it to the file
                            with open(file_path, 'a', encoding='utf-8') as file:
                                file.write(message.text + '\n')
            
            # Read the content from the GPTMessages.txt file
            with open('GPTMessages.txt', 'r', encoding='utf-8') as file:
                content2 = file.read()
                file.seek(0)

            # Check if the new content is different from the last sent message
            if content2 != last_sent_message:
                # Wait until the dialog box appears
                message_box = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Tin nhắn'][@role='textbox']"))
                )

                # Copy the content to the clipboard
                pyperclip.copy(content2)

                # Paste the copied content into the message box
                message_box.send_keys(Keys.CONTROL, 'v')

                # Press Enter to send the message
                ActionChains(driver).send_keys(Keys.RETURN).perform()

                time.sleep(2)

                # Find and click the button
                button = driver.find_element(By.CSS_SELECTOR, 'div.x1i10hfl.x1qjc9v5.xjbqb8w.xjqpnuy.xa49m3k.xqeqjp1.x2hbi6w.x13fuv20.xu3j5b3.x1q0q8m5.x26u7qi.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xdl72j9.x2lah0s.xeuugli.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1n2onr6.x16tdsg8.x1hl2dhg.xggy1nq.x1ja2u2z.x1t137rt.x1o1ewxj.x3x9cwd.x1q0g3np.x87ps6o.x1lku1pv.x1a2a7pz')
                button.click()

                # Update the last sent message
                last_sent_message = content2

        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(5)  # Wait for 5 seconds before retrying

        # Refresh the webpage every 5 minutes
        time.sleep(300)  # Wait for 300 seconds
        driver.refresh()  # Refresh the webpage

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    driver.quit()
