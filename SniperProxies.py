import time
import re
import requests
from bs4 import BeautifulSoup
from random import choice
import datetime


day = datetime.date.today()
print(day)


class GetProxy:
    def UsProxy(self, user_agent):
        url = requests.get("https://www.us-proxy.org/", headers=user_agent, timeout=30)
        if url.status_code == 200:
            soup = BeautifulSoup(url.text, 'html.parser')

            for row in soup.findAll('table')[0].tbody.findAll('tr'):
                ip = row.findAll('td')[0].contents
                port = row.findAll('td')[1].contents
                proxy = str(ip[0] + ":" + port[0] + "\n")
                print("[*] Proxy:{}".format(proxy))
                time.sleep(1)
                a = open("ListProxy{}.txt".format(day), "a+")
                a.write(proxy)
                a.close()

    def ProxyList(self, user_agent):
        global pages
        url = requests.get("http://proxydb.net/", headers=user_agent, timeout=30)
        if url.status_code == 200:
            soup = BeautifulSoup(url.text, 'html.parser')
            number_of_pages = soup.find_all('small', {"class": "text-muted"})
            get_number = re.findall(r'\d+', str(number_of_pages))
            pages = int(get_number[0])
            url.close()

        start = 0
        while (pages > start):
            url = requests.get("http://proxydb.net/?offset={}".format(start), headers=user_agent, timeout=30)
            if url.status_code == 200:
                soup = BeautifulSoup(url.text, 'html.parser')
                for row in soup.findAll('table')[0].tbody.findAll('tr'):
                    ip = row.findAll('td')[0].text
                    proxy = str(ip).replace("\n", "")
                    print("[*] Proxy:{}".format(proxy))
                    time.sleep(1)
                    with open("ListProxy{}.txt".format(day), "a+") as a:
                        a.write(proxy + "\n")
                        a.close()
            print(start)
            start += 15

    def sslproxies(self, user_agent):
        url = requests.get("https://www.sslproxies.org/", headers=user_agent, timeout=30)
        if url.status_code == 200:
            soup = BeautifulSoup(url.text, 'html.parser')
            for row in soup.findAll('table')[0].tbody.findAll('tr'):
                ip = row.findAll('td')[0].contents
                port = row.findAll('td')[1].contents
                proxy = str(ip[0] + ":" + port[0] + "\n")
                print("[*] Proxy:{}".format(proxy))
                time.sleep(1)
                with open("ListProxy{}.txt".format(day), "a+") as a:
                    a.write(proxy)
                    a.close()


if __name__ == '__main__':
    file_user_agents = open('UserAgent.txt', 'r+')
    read = file_user_agents.read().splitlines()
    choose_user_agent = choice(read)
    user_agent = {"User-Agent": "{}".format(choose_user_agent)}
    file_user_agents.close()
    GetProxy().UsProxy(user_agent)
    GetProxy().sslproxies(user_agent)
    GetProxy().ProxyList(user_agent)
