# 다시만들어야 한다 왜냐면 2일치를 붙여도 마지막을 읽기 때문에
import time
import numpy as np

from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup


now_time = datetime.now().strftime("%H:%M")
print('now_time:', now_time)

yest_day = (datetime.now()-timedelta(days=1)).strftime("%Y%m%d")
now_day = datetime.now().strftime("%Y%m%d")
tomo_day = (datetime.now()+timedelta(days=1)).strftime("%Y%m%d")
tomo2_day = (datetime.now()+timedelta(days=2)).strftime("%Y%m%d")
print(yest_day+' / '+now_day+' / '+tomo_day+' / '+tomo2_day)

PATH = "http://ocn.tving.com/ocn/schedule?startDate="
TIME = 'TIME'
PROGRAM = 'PROGRAM'

start1 = time.time()

def read_Soup(path, day):
    return BeautifulSoup(requests.get(path+day).text, 'html5lib')

# yest_ocn_soup = BeautifulSoup(requests.get(PATH+yest_day).text, 'html5lib')
# now_ocn_soup = BeautifulSoup(requests.get(PATH+now_day).text, 'html5lib')
# tomo_ocn_soup = BeautifulSoup(requests.get(PATH+tomo_day).text, 'html5lib')
yest_ocn_soup = read_Soup(PATH, yest_day)
now_ocn_soup = read_Soup(PATH, now_day)
tomo_ocn_soup = read_Soup(PATH, tomo_day)


def cut_HTML(save, soup, now_day, tomo_day, option):
    if option == 'TIME':
        temp = soup.select('td.programInfo em')
    else:
        temp = soup.select('td.programInfo > div .program')
    for i, value in enumerate(temp):
        j = value.text.replace('\t','').replace(' ','').replace('\n','')
        if i>len(temp)/2 and j.startswith('0',0,2): #내일
            save.append(tomo_day+' '+j)
        else: #오늘
            save.append(now_day+' '+j)
    return save

airTime_ocn_list = []
airTime_ocn_list = cut_HTML(airTime_ocn_list, yest_ocn_soup, yest_day, now_day, TIME)
airTime_ocn_list = cut_HTML(airTime_ocn_list, now_ocn_soup, now_day, tomo_day, TIME)
airTime_ocn_list = cut_HTML(airTime_ocn_list, tomo_ocn_soup, tomo_day, tomo2_day, TIME)

program_ocn_list = []
program_ocn_list = cut_HTML(program_ocn_list, yest_ocn_soup, yest_day, now_day, PROGRAM)
program_ocn_list = cut_HTML(program_ocn_list, now_ocn_soup, now_day, tomo_day, PROGRAM)
program_ocn_list = cut_HTML(program_ocn_list, tomo_ocn_soup, tomo_day, tomo2_day, PROGRAM)

# temp = yest_ocn_soup.select('td.programInfo em')
# for i, value in enumerate(temp):
#     j = value.text.replace('\t','').replace(' ','').replace('\n','')
#     if i>len(temp)/2 and j.startswith('0',0,2): #내일
#         airTime_ocn_list.append(now_day+' '+j)
#     else: #오늘
#         airTime_ocn_list.append(yest_day+' '+j)

# temp = now_ocn_soup.select('td.programInfo em')
# for i, value in enumerate(temp):
#     j = value.text.replace('\t','').replace(' ','').replace('\n','')
#     if i>len(temp)/2 and j.startswith('0',0,2): #내일
#         airTime_ocn_list.append(tomo_day+' '+j)
#     else: #오늘
#         airTime_ocn_list.append(now_day+' '+j)

# temp = tomo_ocn_soup.select('td.programInfo em')
# for i, value in enumerate(temp):
#     j = value.text.replace('\t','').replace(' ','').replace('\n','')
#     if i>len(temp)/2 and j.startswith('0',0,2): #내일
#         airTime_ocn_list.append(tomo2_day+' '+j)
#     else: #오늘
#         airTime_ocn_list.append(tomo_day+' '+j)

print(airTime_ocn_list)
print(program_ocn_list)
print(len(airTime_ocn_list))


start_index = [i for i, value in enumerate(airTime_ocn_list) if value >= (now_day+' '+now_time)][0]-1
airTime_ocn_list = airTime_ocn_list[start_index:start_index+4]
program_ocn_list = program_ocn_list[start_index:start_index+4]
print(airTime_ocn_list)
print(program_ocn_list)

print('걸린 시간:', time.time()-start1)
