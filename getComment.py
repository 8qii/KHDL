from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

import re
import time
import pandas as pd
import csv


websites = []

with open('websites.csv', mode='r') as file:
    csv_websites = csv.reader(file)
    for website in csv_websites:
        websites.append(website[0])

chromeOptions = Options()
chromeOptions.add_argument("--incognito")
chromeOptions.add_argument('--start-maximized')

driver = webdriver.Chrome(chromeOptions)

# Login
driver.get("https://vi-vn.facebook.com/login.php/")

txtUser = driver.find_element("id", "email")
txtUser.send_keys("zds34054@dcobe.com")

txtPass = driver.find_element("id", "pass")
txtPass.send_keys("khdl123@")

txtPass.send_keys(Keys.ENTER)

time.sleep(2)

commentsData = []

for website in websites:
    driver.get(website)

    # time.sleep(10)

    # clearLogin = driver.find_element(By.XPATH, '//div[@class ="x92rtbv x10l6tqk x1tk7jg1 x1vjfegm"]')
    # clearLogin.click()

    time.sleep(5)

    replyPattern = r'phản hồi'
    lastHeight = driver.execute_script("return document.body.scrollHeight")

    time.sleep(5)

    loopCount = 0
    while True:
        try:
            sortingButton = driver.find_element(
                By.XPATH, '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[4]/div/div/div[2]/div[2]/div/div/span/div')
            sortingButton.click()
            time.sleep(10)

            allComments = driver.find_element(
                By.XPATH, "//span[contains(text(), 'Tất cả bình luận')]")
            allComments.click()
            time.sleep(10)
        except:
            print('All Comments Error')

        time.sleep(5)

        try:
            replies = driver.find_elements(
                By.XPATH, '//span[@class="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen x1s688f xi81zsa" and @dir="auto"]')
            # print("Element found:", expandComments)
        except NoSuchElementException:
            print("Elements not found")

        if len(replies) > 0:
            count = 0
            for reply in replies:
                action = ActionChains(driver)
                text = reply.text
                if re.search(replyPattern, text):
                    print(1)
                else:
                    count += 1
                    continue

                try:
                    action.move_to_element(reply).click().perform()
                    count += 1
                except:
                    try:
                        driver.execute_script("arguments[0].click();", reply)
                        count += 1
                    except:
                        continue
            if len(replies) - count > 0:
                print('replies issue:', len(replies) - count)
            time.sleep(1)
        else:
            pass

        while True:
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(10)
            newHeight = driver.execute_script(
                "return document.body.scrollHeight")
            if newHeight == lastHeight:
                print('End')
                loopCount += 1
                break
            lastHeight = newHeight
            loopCount = 0

        if loopCount > 1:
            break

    comments = driver.find_elements(
        By.XPATH, '//div[@class="xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs"]')

    for comment in comments:
        commentsData.append(comment.text)

    df = pd.DataFrame({'comments': commentsData})
    df.to_csv('demo.csv')

driver.quit()

df = pd.DataFrame({'comments': commentsData})
df.to_csv('demo.csv')
