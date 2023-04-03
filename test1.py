import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def save_capture(url, file_path):
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
    driver.get(url)
    driver.save_screenshot(file_path)
    driver.quit()


chrome_options = Options()
chrome_options.add_argument('--headless')

# 크롬 드라이버 경로 설정
chromedriver_path = './chromedriver'

# 결과를 저장할 디렉토리 생성
capture_dir = 'captures'
if not os.path.exists(capture_dir):
    os.makedirs(capture_dir)

normal_dir = os.path.join(capture_dir, 'normal')
if not os.path.exists(normal_dir):
    os.makedirs(normal_dir)

redirection_dir = os.path.join(capture_dir, 'redirection')
if not os.path.exists(redirection_dir):
    os.makedirs(redirection_dir)

error_dir = os.path.join(capture_dir, 'error')
if not os.path.exists(error_dir):
    os.makedirs(error_dir)

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
        file_name = url.replace('/', '_') + '.png'
        file_path = os.path.join(normal_dir, file_name)
        save_capture(url, file_path)

        # HTTP 응답 코드 확인
        response = requests.get(url)
        status_code = response.status_code

        # HTTP 응답 코드에 따라 정상/리다이렉션/에러에 저장
        if status_code < 300:
            normal_urls.append(url)
            normal_file_path = os.path.join(normal_dir, file_name)
            save_capture(url, normal_file_path)
        else:
            redirection_urls.append(url)
            redirection_file_path = os.path.join(redirection_dir, file_name)
            save_capture(url, redirection_file_path)
            if status_code >= 400 or status_code is None:
                error_urls.append(url)
                error_file_path = os.path.join(error_dir, file_name)
                save_capture(url, error_file_path)
    except Exception:
        exception_urls.append(url)

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

# 예외 처리된 URL 리스트
with open('exception_urls.txt', 'w') as f:
    for url in exception_urls:
        f.write(url + '\n')