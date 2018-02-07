import random
import socket
import traceback
import urllib
import urllib.request
import bs4
import os

import sys
from baidu_search.settings import USER_AGENTS
import time
import datetime

class IPAgentHelper:
    __headers = {
        'User-Agent': random.choice(USER_AGENTS),
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        # 'Accept-Language': 'en-US,en;q=0.5',
        # 'Connection': 'keep-alive',
        # 'Accept-Encoding': 'gzip, deflate',
    }

    def __init__(self):
        super(IPAgentHelper, self).__init__()

    def get_usable_ip_list(self):
        file_path = '../ip/ip_list.dat'
        valid_ip_list = []
        if not os.path.exists('../ip'):
            os.makedirs('../ip')
        if os.path.exists(file_path):
            create_time = os.path.getctime(file_path)
            create_time = time.localtime(create_time)
            create_time = time.strftime('%Y-%m-%d %H:%M:%S', create_time)
            create_time = datetime.datetime.strptime(create_time, '%Y-%m-%d %H:%M:%S')
            if (datetime.datetime.now() - create_time).total_seconds() > (24 * 60 * 60):
                os.unlink(file_path)
            else:
                f = open(file_path)
                lines = f.readlines()
                for line in lines:
                    ip = line.strip('\n').split('\t')[0]
                    valid_ip_list.append(ip)

        if not os.path.exists(file_path):
            ip_list = self.__get_ip_agent()
            for ip in ip_list:
                if self.__verify_ip_address(ip):
                    valid_ip_list.append(ip)
            f = open(file_path, 'w')
            for ip in valid_ip_list:
                f.write(ip + '\n')
        return valid_ip_list

    def __get_ip_agent(self):
        ip_list = []
        base_url = 'http://www.xicidaili.com/nn/'
        for x in range(1, 5):
            url = base_url + str(x)
            req = urllib.request.Request(url, headers=self.__headers)
            with urllib.request.urlopen(req) as f:
                print(type(f))
                print('status: %s' % f.status)
                # html_text = f.read().decode('unicode')
                html_text = f.read().decode('utf-8')
                parent_soup = bs4.BeautifulSoup(html_text, 'html.parser')
                elems = parent_soup.select('table#ip_list tr')
                if len(elems) == 0:
                    elems = parent_soup.select('table#ip_list tbody tr')
                for elem in elems:
                    tds = elem.select('td')
                    if len(tds):
                        try:
                            speed_text = tds[6].select('div')[0].get('title')
                            speed = float(speed_text[0:len(speed_text) - 2])
                            if speed < 2:
                                ip = tds[5].text.strip().lower() + '&' + tds[1].text.strip() + ':' + tds[2].text.strip()
                                # ip = tds[1].text.strip() + ':' + tds[2].text.strip()
                                ip_list.append(ip)
                        except:
                            pass
                time.sleep(1)
        return ip_list

    def __verify_ip_address(self, ip):
        ip = ip.split('&')
        proxy_handler = urllib.request.ProxyHandler({ip[0]: '%s://%s' % ('http', ip[1])})
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [('User-Agent', random.choice(USER_AGENTS))]
        urllib.request.install_opener(opener)
        second_url = "http://www.whatismyip.com.tw/"
        try:
            with urllib.request.urlopen(second_url) as f:
                if f.status == 200:
                    html_text = f.read().decode('utf-8')
                    print('-----------ip:' + html_text)
                    return True
        except:
            print(traceback.format_exc())
        return False
        # url = 'http://www.baidu.com'
        # with urllib.request.urlopen(url) as f:
        #     print(type(f))
        #     if f.status == 200:
        # second_url = "http://ip.chinaz.com/getip.aspx"
        #                 return True
        # return False
