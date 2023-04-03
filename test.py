import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')

# 크롬 드라이버 경로 설정
chromedriver_path = './chromedriver'

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

# URL 파일을 열어서 URL 리스트에 저장
with open('urls.txt', 'r') as f:
    urls = f.readlines()
urls = [url.strip() for url in urls]

# Selenium을 사용해 각 URL에 접속하고 캡쳐 및 HTTP 응답 코드 확인
for url in urls:
    try:
        # Selenium을 이용해 URL에 접속하여 캡쳐
        driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
        driver.get(url)

        # HTTP 응답 코드 확인
        response = requests.get(url)
        status_code = response.status_code

        # HTTP 응답 코드에 따라 정상/리다이렉션/에러에 저장
        if status_code < 300:
            normal_urls.append(url)
            driver.save_screenshot(f'captures/normal/{url}.png')
        else:
            redirection_urls.append(url)
            driver.save_screenshot(f'captures/redirection/{url}.png')
            if status_code >= 400 or status_cord is None:
                error_urls.append(url)
                driver.save_screenshot(f'captures/error/{url}.png')
    except Exception:
        exception_urls.append(url)
    finally:
        driver.quit()

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