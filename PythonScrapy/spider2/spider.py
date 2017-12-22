import requests
from MachineLearning.PythonScrapy.spider2 import get_header
from lxml.html import etree
from MachineLearning.PythonScrapy.spider2 import playload, headers, detail_data_url_pre
import threading as td
import time

count = 0
count_lock = td.Lock()
start_time = time.time()

def begin_with_date(query_date):
    playload['matchdate'] = query_date
    headers['User-Agent'] = get_header()['User-Agent']
    # print(headers)
    response = requests.post('http://op1.win007.com/bet007history.aspx', headers=headers, data=playload)
    # return response
    parse_html(response)

def parse_html(response):
    html = etree.HTML(response.text)

    for index in range(1, 200):
        rex_path = '//*[@id="tr_' + str(index) + '"]/td[13]/a/@href'

        href = html.xpath(rex_path)
        if href:
            import re
            id = re.findall(r"\d+", href[0])[0]
            detail_url = detail_data_url_pre + str(id) + '.js'
            # get_detail_data(detail_url)
            childT = td.Thread(target=get_detail_data, args=(detail_url,))
            childT.start()
            childT.join()


def get_detail_data(url):
    global count
    try:
        response = requests.get(url=url, headers=get_header())
        # print(response.text)
        print("**********")
        print(response.status_code)

        if count_lock.acquire():
            count += 1
            print("Total is %d " % count)
            end_time = time.time()
            tt = end_time - start_time
            print("Time:\nHave been run is %f seconds" % (tt))
            print("Avage %f \n" % (tt / count))
            count_lock.release()
    except Exception:
        return

def start_collect_data():

    for year in range(int(startYMD[0]), int(endYMD[0]) + 1):
        if year == int(startYMD[0]):
            startMonth = int(startYMD[1])
        else:
            startMonth = 1

        if year == int(endYMD[0]):
            endMonth = int(endYMD[1])
        else:
            endMonth = 13

        for month in range(startMonth, endMonth + 1):
            startDay = 1
            endDay = calendar.monthrange(year, month)[1]
            if year == int(startYMD[0]) and month == int(startYMD[1]):
                startDay = int(startYMD[2])

            if year == int(endYMD[0]) and month == int(endYMD[1]):
                endDay = int(endYMD[2])

            for day in range(startDay, endDay + 1):
                strdate_for_query = str(year) + "-" + str(month) + "-" + str(day)
                # print(strdate_for_query)
                # begin_with_date(strdate_for_query)
                t = td.Thread(target=begin_with_date, args=(strdate_for_query,))
                t.setDaemon(True)
                t.start()
                t.join(timeout=1)


# this part for get args from cmd
import argparse
from datetime import datetime
import calendar
now = datetime.now().today()
today = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
parser = argparse.ArgumentParser(description="Usage for this scrpt")
parser.add_argument('-s', type=str, default='2017-12-1')
parser.add_argument('-e', type=str, default=today)
parser.add_argument('-d', type=str, default="/home/alan/tempdata")
args = parser.parse_args()
startYMD = args.s.split('-')
endYMD = args.e.split('-')

if __name__=='__main__':
    main_thread = td.Thread(target=start_collect_data)
    main_thread.setDaemon(True)
    main_thread.start()
    main_thread.join()





