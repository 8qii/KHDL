from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import csv
import pandas as pd

# Đọc danh sách các link từ file websites.csv
websites = []
with open('data/websites.csv', mode='r') as file:
    csv_websites = csv.reader(file)
    for website in csv_websites:
        websites.append(website[0])

# Cấu hình chế độ incognito cho trình duyệt
chromeOptions = Options()
chromeOptions.add_argument("--incognito")
chromeOptions.add_argument('--start-maximized')

driver = webdriver.Chrome(options=chromeOptions)

# Đăng nhập Facebook
driver.get("https://vi-vn.facebook.com/login.php/")
time.sleep(2)

txtUser = driver.find_element(By.ID, "email")
txtUser.send_keys("zds34054@dcobe.com")

txtPass = driver.find_element(By.ID, "pass")
txtPass.send_keys("khdl123@")
txtPass.send_keys(Keys.ENTER)

time.sleep(2)

# Danh sách để lưu dữ liệu số lượng react
reactData = []

# Duyệt qua các website trong danh sách
for website in websites:
    driver.get(website)
    time.sleep(5)  # Chờ trang tải

    try:
        # Tìm phần tử <span> chứa số lượng react dựa trên class đã cung cấp
        reactElement = driver.find_element(
            By.XPATH, '//span[@class="xt0b8zv x1e558r4"]')
        reactCount = reactElement.text  # Lấy số lượng react từ text của span
        print(f'Link: {website}, React: {reactCount}')
    except NoSuchElementException:
        reactCount = "0"
        print(f'Link: {website}, React not found')

    # Lưu dữ liệu vào danh sách
    reactData.append({'link': website, 'react': reactCount})

# Lưu dữ liệu react vào file react.csv
df = pd.DataFrame(reactData)
df.to_csv('data/react.csv', index=False)

# Đóng trình duyệt
driver.quit()
