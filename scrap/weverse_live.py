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


async def get_lives():
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

    lives = []

    try:
        driver.get('https://weverse.io/fromis9/live')

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

        live_list = soup.select('.LiveListView_live_list__MzGxX .LiveListView_live_item__aX1Ph')

        current_year = datetime.now().year

        for live in live_list:
            title = live.select_one('.RelatedProductItemView_package_name__-Xmh0').text
            date = live.select_one('.LiveArtistProfileView_info__dICbs').text

            if len(date.split('. ')) == 3:
                date = f"{current_year}. {date}"

            datetime_obj = datetime.strptime(date, "%Y. %m. %d. %H:%M")

            date = datetime_obj.isoformat()

            name_mapping = {
                '가로새롬': '이새롬',
                '하영': '송하영',
                '지원': '박지원',
                '지선': '노지선',
                '더여니': '이서연',
                '지헌': '백지헌'
            }

            member_elements = live.select('.LiveArtistProfileView_name_item__8W66y')

            members = ', '.join([element.text for element in member_elements])

            for old_name, new_name in name_mapping.items():
                members = members.replace(old_name, new_name)

            members = members.rstrip(', ')

            url = "https://weverse.io" + live['href']
            live_id = url.split('/')[-1]

            lives.append({
                "liveId": live_id,
                "title": title,
                "date": date,
                "members": members,
                "url": url
            })

    except Exception as e:
        print(f"Error occurred while getting notices: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        driver.quit()

    return lives
