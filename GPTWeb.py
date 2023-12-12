from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time
import os

# Khởi tạo đối tượng ChromeOptions
options = Options()

# Thêm tùy chọn để tắt thông báo
options.add_argument("--disable-notifications")

# Thêm tùy chọn để loại bỏ thông báo lỗi
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Khởi tạo trình duyệt Chrome với các tùy chọn đã thiết lập
driver = webdriver.Chrome(options=options)

try:
    # Mở trang web
    driver.get('https://flowgpt.com/p/gpt4-freenofluxcost')

    # Đường dẫn đến file
    received_file_path = "ReceivedMessages.txt"
    done_file_path = "DoneMessages.txt"
    gpt_file_path = "GPTMessages.txt"

    # Kiểm tra xem file đã tồn tại chưa, nếu chưa thì tạo mới
    if not os.path.exists(received_file_path):
        open(received_file_path, 'w').close()
    if not os.path.exists(done_file_path):
        open(done_file_path, 'w').close()
    if not os.path.exists(gpt_file_path):
        open(gpt_file_path, 'w').close()

    while True:
        # Đọc dòng cuối cùng từ file ReceivedMessages.txt
        with open(received_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            last_line = lines[-1].strip() if lines else None

        # Kiểm tra xem dòng cuối cùng đã được gửi chưa
        with open(done_file_path, 'r', encoding='utf-8') as file:
            done_messages = file.read()
            if last_line and last_line not in done_messages:
                # Gửi dòng cuối cùng vào file DoneMessages.txt
                with open(done_file_path, 'a', encoding='utf-8') as file:
                    file.write(last_line + '\n')

                try:
                    # Tìm hộp thoại trên trang web
                    message_box = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[data-testid='chat-input-textarea']"))
                    )
                    print("Đã tìm thấy hộp thoại")
                except TimeoutException:
                    print("Không tìm thấy hộp thoại. Đợi 60 giây.")
                    time.sleep(60)

                message_box.send_keys(last_line + " Đừng gửi các ký tự icon, chỉ gửi văn bản thôi")
                message_box.send_keys(Keys.ENTER)

                # Đợi cho đến khi phần tử cần tìm kiếm xuất hiện
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'group relative w-fit rounded-bl-xl rounded-br-xl border border-white border-opacity-10 p-3 sm:max-w-[60%] sm:p-4 lg:max-w-[80%] mr-[46px] rounded-tr-xl bg-fgMain-800')]"))
                )

                while True:
                    # Lấy phần tử mới nhất
                    response_element = driver.find_elements(By.XPATH, "//div[contains(@class, 'group relative w-fit rounded-bl-xl rounded-br-xl border border-white border-opacity-10 p-3 sm:max-w-[60%] sm:p-4 lg:max-w-[80%] mr-[46px] rounded-tr-xl bg-fgMain-800')]")[-1]

                    # Lấy văn bản từ phần tử
                    test1_text = response_element.get_attribute("innerHTML")

                    # Đợi 5 giây
                    time.sleep(5)

                    # Lấy văn bản từ cùng một phần tử sau 5 giây
                    test2_text = response_element.get_attribute("innerHTML")

                    # Kiểm tra xem văn bản có thay đổi sau 5 giây không
                    if test1_text == test2_text:
                        # Nếu không thay đổi, bắt đầu lấy các phần tử con
                        break

                # Lấy tất cả các phần tử con <p> và <li>
                child_elements = response_element.find_elements(By.XPATH, ".//p")

                # Tạo một danh sách để lưu trữ văn bản từ các phần tử con
                response_texts = []

                for child in child_elements:
                    # Lấy văn bản từ phần tử con
                    response_text = child.get_attribute("textContent")

                    # Kiểm tra xem văn bản này có phải là "Loading..." hay không
                    if response_text != "Loading...":
                        # Nếu không phải, kiểm tra xem văn bản này đã tồn tại trong danh sách chưa
                        if response_text not in response_texts:
                            # Nếu không phải, thêm văn bản vào danh sách
                            response_texts.append(response_text)

                # Loại bỏ các đoạn văn bản trùng lặp từ danh sách
                response_texts = list(dict.fromkeys(response_texts))

                # Lấy response_text là danh sách các văn bản đã thu thập được
                response_text = ' '.join(response_texts)

                # Xóa nội dung file GPTMessages.txt
                open(gpt_file_path, 'w').close()

                # Gửi văn bản vào file GPTMessages.txt
                with open(gpt_file_path, 'a', encoding='utf-8') as file:
                    file.write(response_text + '\n')

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Đóng trình duyệt
    driver.quit()
