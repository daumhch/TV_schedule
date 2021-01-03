# 다시만들어야 한다 왜냐면 2일치를 붙여도 마지막을 읽기 때문에
import time
import numpy as np

from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

def read_Soup(path, day):
    return BeautifulSoup(requests.get(path+day).text, 'html5lib')

def cut_HTML(save, soup, now_day, tomo_day, option):
    if option == 'TIME':
        temp = soup.select('td.programInfo em')
        for i, value in enumerate(temp):
            j = value.text.replace('\t','').replace(' ','').replace('\n','')
            if i>len(temp)/2 and j.startswith('0',0,2): #내일
                save.append(tomo_day+' '+j)
            else: #오늘
                save.append(now_day+' '+j)
    elif option == 'PROGRAM':
        temp = soup.select('td.programInfo > div .program')
        for i, value in enumerate(temp):
            j = value.text.replace('\t','').replace(' ','').replace('\n','')
            save.append(j)
    return save

def read_schedule(path):
    now_time = datetime.now().strftime("%H:%M")
    yest_day = (datetime.now()-timedelta(days=1)).strftime("%Y%m%d")
    now_day = datetime.now().strftime("%Y%m%d")
    tomo_day = (datetime.now()+timedelta(days=1)).strftime("%Y%m%d")
    tomo2_day = (datetime.now()+timedelta(days=2)).strftime("%Y%m%d")

    yest_ocn_soup = read_Soup(path, yest_day)
    now_ocn_soup = read_Soup(path, now_day)
    tomo_ocn_soup = read_Soup(path, tomo_day)

    airTime_ocn_list = []
    airTime_ocn_list = cut_HTML(airTime_ocn_list, yest_ocn_soup, yest_day, now_day, 'TIME')
    airTime_ocn_list = cut_HTML(airTime_ocn_list, now_ocn_soup, now_day, tomo_day, 'TIME')
    airTime_ocn_list = cut_HTML(airTime_ocn_list, tomo_ocn_soup, tomo_day, tomo2_day, 'TIME')

    program_ocn_list = []
    program_ocn_list = cut_HTML(program_ocn_list, yest_ocn_soup, yest_day, now_day, 'PROGRAM')
    program_ocn_list = cut_HTML(program_ocn_list, now_ocn_soup, now_day, tomo_day, 'PROGRAM')
    program_ocn_list = cut_HTML(program_ocn_list, tomo_ocn_soup, tomo_day, tomo2_day, 'PROGRAM')

    start_index = [i for i, value in enumerate(airTime_ocn_list) if value >= (now_day+' '+now_time)][0]-1
    airTime_ocn_list = airTime_ocn_list[start_index:start_index+4]
    program_ocn_list = program_ocn_list[start_index:start_index+4]
    return airTime_ocn_list, program_ocn_list


if __name__ == '__main__':
    OCN_PATH = "http://ocn.tving.com/ocn/schedule?startDate="
    airTime_ocn_list, program_ocn_list = read_schedule(OCN_PATH)
    print(airTime_ocn_list)
    print(program_ocn_list)

    THRILLS_PATH = "http://ocnthrills.tving.com/ocnthrills/schedule?startDate="
    airTime_ocnT_list, program_ocnT_list = read_schedule(THRILLS_PATH)
    print(airTime_ocnT_list)
    print(program_ocnT_list)

    MOVIES_PATH = "http://ocnmovies.tving.com/ocnmovies/schedule?startDate="
    airTime_ocnM_list, program_ocnM_list = read_schedule(MOVIES_PATH)
    print(airTime_ocnM_list)
    print(program_ocnM_list)