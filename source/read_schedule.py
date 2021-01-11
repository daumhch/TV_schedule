# 다시만들어야 한다 왜냐면 2일치를 붙여도 마지막을 읽기 때문에
import numpy as np
import pandas as pd

from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup


def read_Soup(path, day):
    return BeautifulSoup(requests.get(path+day).text, 'html.parser')


def cut_HTML(save, soup, now_day, tomo_day, option):
    if option == 'TIME':
        temp = soup.select('td.programInfo em')
        for i, value in enumerate(temp):
            j = value.text.replace('\t', '').replace(' ', '').replace('\n', '')
            if i > len(temp)/2 and j.startswith('0', 0, 2):  # 내일
                save.append(tomo_day+' '+j)
            else:  # 오늘
                save.append(now_day+' '+j)
    elif option == 'PROGRAM':
        temp = soup.select('td.programInfo > div .program')
        for i, value in enumerate(temp):
            j = value.text.replace('\t', '').replace(' ', '').replace('\n', '')
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

    temp1 = []
    temp1 = cut_HTML(temp1, yest_ocn_soup, yest_day, now_day, 'TIME')
    temp1 = cut_HTML(temp1, now_ocn_soup, now_day, tomo_day, 'TIME')
    temp1 = cut_HTML(temp1, tomo_ocn_soup, tomo_day, tomo2_day, 'TIME')

    temp2 = []
    temp2 = cut_HTML(temp2, yest_ocn_soup, yest_day, now_day, 'PROGRAM')
    temp2 = cut_HTML(temp2, now_ocn_soup, now_day, tomo_day, 'PROGRAM')
    temp2 = cut_HTML(temp2, tomo_ocn_soup, tomo_day, tomo2_day, 'PROGRAM')

    start_index = [i for i, value in enumerate(temp1)
                    if value >= (now_day+' '+now_time)][0]-1
    temp1 = temp1[start_index:start_index+4]
    temp2 = temp2[start_index:start_index+4]

    temp = np.array([temp1, temp2]).T
    temp = pd.DataFrame(temp)
    return temp


if __name__ == '__main__':
    OCN_PATH = "http://ocn.tving.com/ocn/schedule?startDate="
    ocn_list = read_schedule(OCN_PATH)
    print(ocn_list.to_html())

    # THRILLS_PATH = "http://ocnthrills.tving.com/ocnthrills/schedule?startDate="
    # ocnT_list = read_schedule(THRILLS_PATH)
    # print(ocnT_list)

    # MOVIES_PATH = "http://ocnmovies.tving.com/ocnmovies/schedule?startDate="
    # ocnM_list = read_schedule(MOVIES_PATH)
    # print(ocnM_list)
