import os
import time
import dotenv
import requests
import traceback
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

# Load environment variables
dotenv.load_dotenv()

chrome_options = Options()
chrome_options.add_argument("--headless")  # headless
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

# Set geolocation permissions
prefs = {
    "profile.default_content_setting_values.geolocation": 1,  # 1: allowed, 2: blocked, 0: default
}
chrome_options.add_experimental_option("prefs", prefs)

def query_newest_slot(cities=['Parramatta', 'Sydney', 'Bankstown '], postcode='2000', state='NSW'):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # URL
    url = "https://bmvs.onlineappointmentscheduling.net.au/oasis/"
    driver.get(url)
    result = []
    try:
        # load page and click "New Individual"
        wait = WebDriverWait(driver, 20)
        new_individual_button = wait.until(EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_btnInd")))
        new_individual_button.click()
        print("Clicked 'New Individual booking' button successfully.")

        # Waiting for the final page to load
        wait.until(EC.url_changes(url))
        print("Waiting for the final page to load...")

        # select postcode
        suburb_input = driver.find_element(By.ID, "ContentPlaceHolder1_SelectLocation1_txtSuburb")
        suburb_input.send_keys(postcode)

        # select state
        state_select = Select(driver.find_element(By.ID, "ContentPlaceHolder1_SelectLocation1_ddlState"))
        state_select.select_by_value(state)

        # click search
        search_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Search']")
        search_button.click()

        # waiting for the final page to load
        time.sleep(3)

        # get the html 
        html = driver.page_source

        # quit WebDriver
        driver.quit()

        # parse HTML
        soup = BeautifulSoup(html, 'html.parser')
        for c in cities:
            label = soup.find('label', string=c)
            if label:
                row = label.find_parent('td').find_parent('tr')
                date = row.find('td', class_='tdloc_availability').text.strip()
                if date == "No available slot":
                    print(f"{c}: No available slot.")
                    continue
                date = parse_date_to_yyyymmdd(date)
                print(f"{c}: {date}")
                if compare_dates(date, "2024-08-20 11:30AM"):
                    result.append(f"{c}: {date}")
            else:
                print(f"{c} not found.")

    except Exception as e:
        print(f"An error occurred: {e}")
    return result

def parse_date_to_yyyymmdd(date_str):
    date_str = date_str.replace(',', '')
    date_format = "%A %d/%m/%Y%I:%M %p"
    date_obj = datetime.strptime(date_str, date_format)
    formatted_date = date_obj.strftime("%Y-%m-%d %I:%M%p")
    return formatted_date

def compare_dates(date_str1, date_str2):
    date_str1 = date_str1.split(' ')[0]
    date_str2 = date_str2.split(' ')[0]
    date1 = datetime.strptime(date_str1, "%Y-%m-%d")
    date2 = datetime.strptime(date_str2, "%Y-%m-%d")
    if date1 < date2:
        return True
    elif date1 >= date2:
        return False   


def send_ios_notification(body_text):
    BARK_API = os.environ.get('BARK_API')
    url = f"{BARK_API}/{body_text}"
    response = requests.get(url)
    if response.status_code == 200:
        print("iOS notification sent successfully.")
    else:
        print("Failed to send iOS notification.")


if __name__ == '__main__':
    while True:
        try:
            result = query_newest_slot()
            print(result)
            for i in result:
                send_ios_notification(f'New slot available/{i.replace("/", "-")}')
            time.sleep(120)
        except:
            traceback.print_exc()
            time.sleep(300)