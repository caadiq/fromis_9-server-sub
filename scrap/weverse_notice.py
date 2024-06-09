import time
from datetime import datetime

from bs4 import BeautifulSoup
from fastapi import HTTPException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import config


async def get_notices():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Whale/3.26.244.21 Safari/537.36')

    driver = webdriver.Chrome(options=options)

    notices = []

    try:
        driver.get('https://weverse.io/fromis9/notice')

        wait = WebDriverWait(driver, 10)

        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='confirm modal']")))
        login_button.click()

        email_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='userEmail']")))
        email_field.send_keys(config.weverse_id)

        continue_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        continue_button.send_keys(Keys.RETURN)

        password_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='password']")))
        password_field.send_keys(config.weverse_pw)

        login_submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_submit_button.send_keys(Keys.RETURN)

        time.sleep(5)

        html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')

        notice_list = soup.select('.NoticeListView_notice_item__1-Ud8')

        for notice in notice_list:
            title = notice.select_one('.NoticeListView_notice_title__YIRBv').text
            date = notice.select_one('.NoticeListView_notice_date__eC4V1').text
            link = "https://weverse.io" + notice.select_one('a')['href']

            postid = link.split('/')[-1]

            notice_date = datetime.strptime(date, "%Y.%m.%d")

            current_month = datetime.now().month

            if notice_date.month == current_month:
                notices.append({
                    "postId": postid,
                    "title": title,
                    "date": date,
                    "url": link
                })

    except Exception as e:
        print(f"Error occurred while getting notices: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        driver.quit()

    return notices
