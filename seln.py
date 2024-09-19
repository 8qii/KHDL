from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import sqlite3
import time

# Cấu hình Selenium
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
options.add_argument('--start-maximized')

# Khởi động Chrome WebDriver
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)
driver.get('https://www.facebook.com/BatHuPTIT/posts/pfbid0TtcxQ4FAML6XtHLgMoVsbmr6RPAK4cGhxzPFUB3NhJpHc79H7eDMgKivy5uBEitQl?rdid=7rzhfVRhny9QDGHC')

# Đợi một chút để trang load
time.sleep(5)

# Cuộn trang để tải thêm bình luận
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Đợi một chút để các comment mới load
    new_height = driver.execute_script("return document.body.scrollHeight")

    # Nếu không còn cuộn thêm được nữa thì dừng lại
    if new_height == last_height:
        break
    last_height = new_height

# Kết nối tới cơ sở dữ liệu SQLite3
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Lấy tất cả các comment (dựa trên cấu trúc HTML bạn cung cấp)
comments = driver.find_elements(
    By.XPATH, '//div[@class="xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs"]//div[@dir="auto"]')
for comment in comments:
    text = comment.text
    print(text)  # In ra để kiểm tra

    # Lưu comment vào cơ sở dữ liệu
    cursor.execute('INSERT INTO comments (comment) VALUES (?)', (text,))

# Lưu thay đổi và đóng kết nối
conn.commit()
conn.close()

# Đóng trình duyệt sau khi hoàn thành
driver.quit()
