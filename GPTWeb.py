from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time
import os
import pyperclip

# Initialize ChromeOptions object
options = Options()

first_time = True

# Add option to disable notifications
options.add_argument("--disable-notifications")

# Add option to exclude logging
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Initialize Chrome browser with the set options
driver = webdriver.Chrome(options=options)

try:
    # Open the website
    driver.get('https://flowgpt.com/p/gpt4-freenofluxcost')

    # Paths to the files
    received_file_path = "ReceivedMessages.txt"
    done_file_path = "DoneMessages.txt"
    gpt_file_path = "GPTMessages.txt"

    # Check if the files exist, if not, create new ones
    if not os.path.exists(received_file_path):
        open(received_file_path, 'w').close()
    if not os.path.exists(done_file_path):
        open(done_file_path, 'w').close()
    if not os.path.exists(gpt_file_path):
        open(gpt_file_path, 'w').close()

    while True:
        # Read the content from the last occurrence of "/ask" until the end of the file
        with open(received_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            last_ask_index = max([i for i, line in enumerate(lines) if '/ask' in line])
            last_ask_content = ''.join(lines[last_ask_index:]).strip()

        # Write the last ask content to the DoneMessages.txt file
        with open(done_file_path, 'a', encoding='utf-8') as file:
            file.write(last_ask_content + '\n')

        try:
            # Find the chat box on the website
            message_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[data-testid='chat-input-textarea']"))
            )
            print("Chat box found")
        except TimeoutException:
            print("Chat box not found. Waiting for 60 seconds.")
            time.sleep(60)

        # Copy the last ask content to the clipboard
        pyperclip.copy(last_ask_content)

        message_box.send_keys(Keys.CONTROL, 'v')
        message_box.send_keys(Keys.ENTER)
        first_time = False

        # Wait for the element to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'group relative w-fit rounded-bl-xl rounded-br-xl border border-white border-opacity-10 p-3 sm:max-w-[60%] sm:p-4 lg:max-w-[80%] mr-[46px] rounded-tr-xl bg-fgMain-800')]"))
        )

        while True:
            # Get the latest element
            response_element = driver.find_elements(By.XPATH, "//div[contains(@class, 'group relative w-fit rounded-bl-xl rounded-br-xl border border-white border-opacity-10 p-3 sm:max-w-[60%] sm:p-4 lg:max-w-[80%] mr-[46px] rounded-tr-xl bg-fgMain-800')]")[-1]

            # Get the text from the element
            test1_text = response_element.get_attribute("innerHTML")

            # Wait for 5 seconds
            time.sleep(5)

            # Get the text from the same element after 5 seconds
            test2_text = response_element.get_attribute("innerHTML")

            # Check if the text has changed after 5 seconds
            if test1_text == test2_text:
                # If it hasn't changed, start getting the child elements
                break

        child_elements = response_element.find_elements(By.XPATH, ".//p | .//code | .//ol[not(.//p)]")

        # Create a list to store the text from the child elements
        response_texts = []

        for child in child_elements:
            # Get the text from the child element
            response_text = child.get_attribute("textContent")

            # Check if this text is "Loading..."
            if response_text != "Loading...":
                # If not, check if this text already exists in the list
                if response_text not in response_texts:
                    # If not, add the text to the list
                    response_texts.append(response_text)

        # Remove duplicate text paragraphs from the list
        response_texts = list(dict.fromkeys(response_texts))

        # Concatenate the response_texts list into a single string
        response_text = ' '.join(response_texts)

        # Clear the content of the GPTMessages.txt file
        open(gpt_file_path, 'w').close()

        # Write the response_text to the GPTMessages.txt file
        with open(gpt_file_path, 'a', encoding='utf-8') as file:
            file.write(response_text + '\n')

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    driver.quit()
