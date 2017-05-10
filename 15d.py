'''
Created on 2017年5月10日

@author: Administrator
'''

#conding:UTF-8

import requests
import csv
import random
import time
import socket
import http.client
#import urllib.request
from bs4 import BeautifulSoup


def get_content(url , data = None):
    header={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }
    timeout = random.choice(range(80, 180))
    while True:
        try:
            rep = requests.get(url,headers = header,timeout = timeout)
            rep.encoding = 'utf-8'
            # req = urllib.request.Request(url, data, header)
            # response = urllib.request.urlopen(req, timeout=timeout)
            # html1 = response.read().decode('UTF-8', errors='ignore')
            # response.close()
            break
        # except urllib.request.HTTPError as e:
        #         print( '1:', e)
        #         time.sleep(random.choice(range(5, 10)))
        #
        # except urllib.request.URLError as e:
        #     print( '2:', e)
        #     time.sleep(random.choice(range(5, 10)))
        except socket.timeout as e:
            print( '3:', e)
            time.sleep(random.choice(range(8,15)))

        except socket.error as e:
            print( '4:', e)
            time.sleep(random.choice(range(20, 60)))

        except http.client.BadStatusLine as e:
            print( '5:', e)
            time.sleep(random.choice(range(30, 80)))

        except http.client.IncompleteRead as e:
            print( '6:', e)
            time.sleep(random.choice(range(5, 15)))

    return rep.text
    # return html_text
    
    
def get_data(html_text):
        final = []
        bs = BeautifulSoup(html_text, "html.parser")  # 创建BeautifulSoup对象
        body = bs.body # 获取body部分
        data = body.find('div', {'id': '15d'})  # 找到id为7d的div
        ul = data.find('ul')  # 获取ul部分
        li = ul.find_all('li')  # 获取所有的li

        for day in li: # 对每个li标签中的内容进行遍历
            temp = []
            #print(day)
            span = day.find_all('span') #找到所有的span标签
            #print(span)
            date = span[0].string  # 找到日期
            temp.append(date)  # 添加到temp中
            wea1 = span[1].string#获取天气情况
            temp.append(wea1) #加入到list
            tem =str(span[2])
            tem = tem.replace('<span class="tem"><em>', '')
            tem = tem.replace('</span>','')
            tem = tem.replace('</em>','')
            #tem = tem.find('span').string #获取温度
            temp.append(tem) #温度加入list
            
            
            windy = span[3].string
            temp.append(windy)#加入到list
            windy1 = span[4].string
            temp.append(windy1)#加入到list
            final.append(temp)
           
        return final


def write_data(data, name):
    file_name = name
    with open(file_name, 'a', errors='ignore', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerows(data)
            
            
if __name__ == '__main__':
    url ='http://www.weather.com.cn/weather15d/101180101.shtml'
    html = get_content(url)
    #print(html)
    result = get_data(html)
    #print(result)
    write_data(result, 'weather7.csv')