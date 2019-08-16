"""
打印天气后报网某城市一整年的天气
"""

import io
import sys
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030') #改变标准输出的默认编码, 防止控制台打印乱码

url_list = []

for month in range(601, 613):#由于天气后报数据从11年1月开始，因此此处range内区间第一位替换为年份末位，本年数据不满整年请替换range值以免报错
    url_list.append("http://www.tianqihoubao.com/lishi/city/month/201" + str(month) + ".html")
    #city由城市或县的拼音替换，部分重名县市命名不通需要在天气后报网查找


def get_soup(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()    #若请求不成功,抛出HTTPError 异常
        #r.encoding = 'gbk'  #与该网站编码匹配
        soup = BeautifulSoup(r.text, 'lxml')
        return soup
    except HTTPError:
        return "Request Error"

def get_data():
    soup = get_soup(url)
    all_weather = soup.find('div', class_="wdetail").find('table').find_all("tr")
    data = list()
    for tr in all_weather[1:]:
        td_li = tr.find_all("td")
        for td in td_li:
            s = td.get_text()
            data.append("".join(s.split()))
    res = np.array(data).reshape(-1, 4)
    return res

def saveTocsv(data, fileName):
    '''
    将天气数据保存至csv文件
    '''
    result_weather = pd.DataFrame(data, columns=['date','tq','temp','wind'])
    result_weather.to_csv(fileName, index=False, encoding='gbk')
    print('Save all weather success!')

if __name__ == '__main__':
    for i in range(12):#本年数据不满整年请将12替换掉，否则会报错（但是不影响结果）
        url = url_list[i]
        data = get_data()
        #name重请将所需爬取的年份取消注释，
        #name=['201101.csv','201102.csv','201103.csv','201104.csv','201105.csv','201106.csv','201107.csv','201108.csv','201109.csv','201110.csv','201111.csv','201112.csv']
        #name=['201201.csv','201202.csv','201203.csv','201204.csv','201205.csv','201206.csv','201207.csv','201208.csv','201209.csv','201210.csv','201211.csv','201212.csv']
        #name=['201301.csv','201302.csv','201303.csv','201304.csv','201305.csv','201306.csv','201307.csv','201308.csv','201309.csv','201310.csv','201311.csv','201312.csv']
        #name=['201401.csv','201402.csv','201403.csv','201404.csv','201405.csv','201406.csv','201407.csv','201408.csv','201409.csv','201410.csv','201411.csv','201412.csv']
        #name=['201501.csv','201502.csv','201503.csv','201504.csv','201505.csv','201506.csv','201507.csv','201508.csv','201509.csv','201510.csv','201511.csv','201512.csv']
        #name=['201601.csv','201602.csv','201603.csv','201604.csv','201605.csv','201606.csv','201607.csv','201608.csv','201609.csv','201610.csv','201611.csv','201612.csv']
        #name=['201701.csv','201702.csv','201703.csv','201704.csv','201705.csv','201706.csv','201707.csv','201708.csv','201709.csv','201710.csv','201711.csv','201712.csv']
        #name=['201801.csv','201802.csv','201803.csv','201804.csv','201805.csv','201806.csv','201807.csv','201808.csv','201809.csv','201810.csv','201811.csv','201812.csv']
        #name=['201901.csv','201902.csv','201903.csv','201904.csv','201905.csv','201906.csv','201907.csv']
        saveTocsv(data, name[i]) 
