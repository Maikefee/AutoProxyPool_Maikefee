import requests
import concurrent.futures
from tqdm import tqdm

def check_socks5(proxy):
    url = 'http://httpbin.org/ip'
    proxies = {
        'http': f'socks5h://{proxy}',
        'https': f'socks5h://{proxy}'
    }

    try:
        response = requests.get(url, proxies=proxies, timeout=5)
        response.raise_for_status()
        print(response.text)
        return proxy
    except requests.exceptions.RequestException as e:
        print(f"Proxy {proxy} failed with error: {e}")
    return None

def main():
    input_file = 'socks.txt'
    output_file = 'alive.txt'

    with open(input_file, 'r') as f:
        proxies = [line.strip() for line in f.readlines() if line.strip()]

    alive_proxies = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(check_socks5, proxy) for proxy in proxies]

        with tqdm(total=len(proxies), desc="检测进度") as pbar:
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    alive_proxies.append(result)
                pbar.update(1)

    print(f'存活的代理数量: {len(alive_proxies)}')

    with open(output_file, 'w') as f:
        for proxy in alive_proxies:
            f.write(proxy + '\n')

if __name__ == '__main__':
    main()
