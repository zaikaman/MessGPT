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

# Khởi tạo đối tượng ChromeOptions
options = Options()

# Thêm tùy chọn để tắt thông báo
options.add_argument("--disable-notifications")

# Thêm tùy chọn để loại bỏ thông báo lỗi
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Khởi tạo trình duyệt Chrome với các tùy chọn đã thiết lập
driver = webdriver.Chrome(options=options)

try:
    # Mở trang web Facebook
    driver.get('http://www.facebook.com')

    # Giả sử bạn đã có biến username và password
    username = 'codedi4756@jalunaki.com'
    password = 'lovelybaby'

    # Đợi cho đến khi phần tử 'email' xuất hiện
    wait = WebDriverWait(driver, 10)
    email_box = wait.until(EC.presence_of_element_located((By.NAME, 'email')))

    # Điền thông tin đăng nhập
    email_box.send_keys(username)

    # Đợi cho đến khi phần tử 'pass' xuất hiện
    password_box = wait.until(EC.presence_of_element_located((By.NAME, 'pass')))
    password_box.send_keys(password)

    # Nhấn nút đăng nhập
    login_button = wait.until(EC.element_to_be_clickable((By.NAME, 'login')))
    login_button.click()
    
    # Đường dẫn đến file
    file_path = "ReceivedMessages.txt"

    # Kiểm tra xem file đã tồn tại chưa, nếu chưa thì tạo mới
    if not os.path.exists(file_path):
        open(file_path, 'w').close()

    last_sent_message = None

    # Tìm kiếm tin nhắn mới trong hộp thoại trò chuyện
    while True:
        try:
            messages = driver.find_elements(By.CSS_SELECTOR, '.x1gslohp.x11i5rnm.x12nagc.x1mh8g0r.x1yc453h.x126k92a')
            for message in messages:
                if '/ask' in message.text:
                    # Đọc file để kiểm tra xem tin nhắn đã được in ra trước đó hay chưa
                    with open(file_path, 'r', encoding='utf-8') as file:
                        if message.text not in file.read():
                            print(message.text)
                            # Nếu tin nhắn chưa được in ra trước đó, thêm nó vào file
                            with open(file_path, 'a', encoding='utf-8') as file:
                                file.write(message.text + '\n')
            # Đọc nội dung từ file GPTMessages.txt
            with open('GPTMessages.txt', 'r', encoding='utf-8') as file:
                content2 = file.read()
                file.seek(0)

            # Kiểm tra xem nội dung mới có khác với tin nhắn cuối cùng đã gửi hay không
            if content2 != last_sent_message:
                # Đợi cho đến khi hộp thoại xuất hiện
                message_box = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Tin nhắn'][@role='textbox']"))
                )

                # Gửi nội dung đã sao chép vào hộp thoại
                message_box.send_keys(content2)

                # Nhấn phím Enter để gửi tin nhắn
                ActionChains(driver).send_keys(Keys.RETURN).perform()

                # Cập nhật tin nhắn cuối cùng đã gửi
                last_sent_message = content2

        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(5)  # Chờ 5 giây trước khi thử lại

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Đóng trình duyệt
    driver.quit()
