import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--log-path=chromedriver.log')  # 로그 파일 경로 설정

# 크롬 드라이버 경로 설정
chromedriver_path = './chromedriver'

def capture_screenshot(url, directory, driver_path):
    """Saves a screenshot of the given URL using the given ChromeDriver"""
    driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, 'loading-spinner')))
        driver.save_screenshot(f"{directory}/{url}.png")
    except Exception:
        capture_exception_urls.append(url)
    finally:
        driver.quit()


def check_status_code(url):
    """Checks the HTTP response code for the given URL"""
    try:
        response = requests.get(url)
        status_code = response.status_code
        return status_code
    except Exception:
        return None

# 결과를 저장할 디렉토리 생성
if not os.path.exists('captures'):
    os.makedirs('captures')
if not os.path.exists('captures/normal'):
    os.makedirs('captures/normal')
if not os.path.exists('captures/redirection'):
    os.makedirs('captures/redirection')
if not os.path.exists('captures/error'):
    os.makedirs('captures/error')

normal_urls = []  # 정상 URL 리스트
redirection_urls = []  # 리다이렉션 URL 리스트
error_urls = []  # 에러 URL 리스트
exception_urls = []  # 예외 처리된 URL 리스트
capture_exception_urls = []  # 캡쳐에서 예외 처리된 URL 리스트

# URL 파일을 열어서 URL 리스트에 저장
with open('urls.txt', 'r') as f:
    urls = f.readlines()
urls = [url.strip() for url in urls]

# Selenium을 사용해 각 URL에 접속하고 캡쳐 및 HTTP 응답 코드 확인
for url in urls:
    try:
        status_code = check_status_code(url)

        # HTTP 응답 코드에 따라 정상/리다이렉션/에러에 저장
        if status_code is None:
            exception_urls.append(url)
        elif status_code < 300:
            normal_urls.append(url)
        elif status_code < 400:
            redirection_urls.append(url)
        else:
            error_urls.append(url)

    except Exception:
        exception_urls.append(url)

# 정상 URL 리스트를 캡쳐
for url in normal_urls:
    capture_screenshot(url, 'captures/normal', chromedriver_path)

# 리다이렉션 URL 리스트를 캡쳐
for url in redirection_urls:
    capture_screenshot(url, 'captures/redirection', chromedriver_path)

# 에러 URL 리스트를 캡쳐
for url in error_urls:
    capture_screenshot(url, 'captures/error', chromedriver_path)

# 정상/리다이렉션/에러 URL 리스트를 파일에 저장
with open('normal_urls.txt', 'w') as f:
    for url in normal_urls:
        f.write(url + '\n')

with open('redirection_urls.txt', 'w') as f:
    for url in redirection_urls:
        f.write(url + '\n')

with open('error_urls.txt', 'w') as f:
    for url in error_urls:
        f.write(url + '\n')

# 예외 처리된 URL 리스트를 파일에 저장
with open('exception_urls.txt', 'w') as f:
    for url in exception_urls:
        f.write(url + '\n')
