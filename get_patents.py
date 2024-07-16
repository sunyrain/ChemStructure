import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# 专利号列表
# 打开patent_collection.xlsx文件，读取专利号
patents_numbers = []
with open('patents.csv', 'r', encoding='utf-8') as file:
    for line in file:
        patents_numbers.append(line.strip())
print(patents_numbers)

# 设置Chrome选项
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-software-rasterizer")
chrome_options.add_argument("blink-settings=imagesEnabled=false")
chrome_options.page_load_strategy = 'eager'
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

driver = webdriver.Chrome(options=chrome_options)

def download_pdf(url, patent_number):
    response = requests.get(url)
    if response.status_code == 200:
        with open(f"{patent_number}.pdf", 'wb') as file:
            file.write(response.content)
    else:
        print(f"Failed to download PDF for patent {patent_number}")

for patent_number in patents_numbers:
    # 打开Google Patents
    url = "https://patents.google.com/patent/" + patent_number
    driver.get(url)
    html = driver.page_source
    # 等待页面加载完毕
    time.sleep(2)
    soup = BeautifulSoup(html, 'html.parser')
    try:
        pdf_link = soup.find('a', string='Download PDF').get('href')
        download_pdf(pdf_link, patent_number)
    except:
        print(f"PDF not found for patent {patent_number}")

driver.quit()
