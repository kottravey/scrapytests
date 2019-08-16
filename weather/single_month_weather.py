"""
打印天气后报网某城市单个月份的天气
"""
import io
import sys
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030') #改变标准输出的默认编码, 防止控制台打印乱码

selectedCity = " " #选择的城市或县市名的拼音，部分重名的县市需要在天气后报官网查看
selectedMonth = " " #选择的日期是什么,格式为 "年份" + "月份"（纯数字，例如2015年12月，为 "201512"）

url = "http://www.tianqihoubao.com/lishi/" + selectedCity + "/month/" + selectedMonth + ".html" 

def get_soup(url):
    try:
        r = requests.get(url, timeout=300)
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
    data = get_data()
    saveTocsv(data, "000000.csv")#csv名称可自定义，可改成与selectedMonth对应时间
