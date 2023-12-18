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

# Mở trang web Facebook
driver.get('http://www.facebook.com')

# Giả sử bạn đã có biến username và password
username = 'subthinh6@gmail.com'
password = 'Lovelybaby93'

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

while True:
    try:
        # Đợi 5 giây sau khi đăng nhập
        time.sleep(15)

        driver.get('https://www.facebook.com/friends')

        time.sleep(3)

        # Liên tục tìm kiếm nút "Xác nhận" mỗi 5 giây cho đến khi tìm thấy
        confirm_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="Xác nhận"]')))
        confirm_button.click()
    except Exception:
        pass
        time.sleep(5)

    # Làm mới trang sau mỗi phút
    time.sleep(55)
    driver.refresh()
