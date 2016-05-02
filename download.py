__author__ = 'evan'
import os
import time
import requests
import xlrd
import csv


def download_300_500(fresh = False):
    url500 = 'http://115.29.204.48/webdata/Csi905Perf.xls'
    url300 = 'http://115.29.204.48/webdata/Csi300Perf.xls'
    ret_list = []
    for i in [url300, url500]:
        name = i.split('/')[-1]
        if os.path.isfile(os.getcwd() + '/' + name):
            statinfo = os.stat(name)
            st_mtime = time.strftime('%F', time.localtime(statinfo.st_mtime))
            current_time = time.strftime('%F', time.localtime())
            hours = int(time.strftime('%H', time.localtime()))
            if st_mtime == current_time and hours < 16:
                fresh = False
        if fresh:
            ret = requests.get(i)
            with open(name, 'w') as fb:
                fb.write(ret.content)

        data = xlrd.open_workbook(name)
        table = data.sheets()[0]
        lines = []
        for rnum in range(1, table.nrows):
            rvalue = table.row_values(rnum)[7]
            rvalue = float(rvalue)
            lines.append(rvalue)
            # print(rvalue)
        ret_list.append(lines)
    return ret_list


def get_current_300_500():
    url300 = 'http://hq.sinajs.cn/list=s_sz399300'
    url500 = 'http://hq.sinajs.cn/list=s_sh000905'
    ret_list = []
    for i in [url300, url500]:
        ret = requests.get(i)
        point = ret.content.split(',')[1]
        point = float(point)
        # print(point)
        ret_list.append(point)
    return ret_list


def download_163():
    base_url = 'http://quotes.money.163.com/service/chddata.html?code=0'
    date = '&fields=TCLOSE&start=20160217&end='
    codes = ['000300', '000905']
    current_time = time.strftime('%Y%m%d', time.localtime())
    ret_list = []
    fresh = True
    for i in codes:
        name = i + '.csv'
        if os.path.isfile(os.getcwd() + '/' + name):
            statinfo = os.stat(name)
            st_mtime = time.strftime('%Y%m%d', time.localtime(statinfo.st_mtime))
            # current_time = time.strftime('%F', time.localtime())
            if st_mtime == current_time:
                # pass
                fresh = False
        if fresh:
            print('download')
            url = base_url + i + date + current_time
            ret = requests.get(url)
            # print(url)
            with open(name, 'w') as fb:
                fb.write(ret.content)
        reader = csv.reader(open(name))
        lines = list(reader)[1:]
        ret_list.append(lines)
    return ret_list


if __name__ == '__main__':
    # print(download_300_500())
    print(download_163())