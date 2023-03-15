import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0'
}


def get_addr_info(ip):
    url = f'https://www.ip138.com/iplookup.php?ip={ip}&action=2'
    res = requests.get(url=url, headers=headers).text
    print(res)


if __name__ == '__main__':
    get_addr_info('120.229.133.112')