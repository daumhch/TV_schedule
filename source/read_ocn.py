import time

from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

def read_ocn():
    now_time = datetime.now().strftime("%H:%M")
    print('now_time:', now_time)

    now_day = datetime.now().strftime("%Y%m%d")
    print('now_day:', now_day)

    tomo_day = datetime.now()+timedelta(days=1)
    tomo_day = tomo_day.strftime("%Y%m%d")
    print('tomo_day:', tomo_day)

    start1 = time.time()

    now_ocn_html = requests.get("http://ocn.tving.com/ocn/schedule?startDate="+now_day)
    now_ocn_soup = BeautifulSoup(now_ocn_html.text, 'html5lib')

    tomo_ocn_html = requests.get("http://ocn.tving.com/ocn/schedule?startDate="+tomo_day)
    tomo_ocn_soup = BeautifulSoup(tomo_ocn_html.text, 'html5lib')

    airTime_ocn_list = []
    for i in now_ocn_soup.select('td.programInfo em'):
        airTime_ocn_list.append(i.text.replace('\t','').replace(' ','').replace('\n',''))
    for i in tomo_ocn_soup.select('td.programInfo em'):
        airTime_ocn_list.append(i.text.replace('\t','').replace(' ','').replace('\n',''))
    print(airTime_ocn_list)

    program_ocn_list = []
    # td 태크 밑에 programInfo 태크 밑에 종속된 div 밑에 class 이름이 program
    for i in now_ocn_soup.select('td.programInfo > div .program'): 
        program_ocn_list.append(i.text.replace('\t','').replace(' ','').replace('\n',''))
    for i in tomo_ocn_soup.select('td.programInfo > div .program'): 
        program_ocn_list.append(i.text.replace('\t','').replace(' ','').replace('\n',''))
    print(program_ocn_list)


    start_index = [i for i, value in enumerate(airTime_ocn_list) if value >= now_time][0]-1

    airTime_ocn_list = airTime_ocn_list[start_index:start_index+4]
    program_ocn_list = program_ocn_list[start_index:start_index+4]

    # print(airTime_ocn_list)
    # print(program_ocn_list)
    print('걸린 시간:', time.time()-start1)

    return airTime_ocn_list, program_ocn_list

if __name__ == '__main__':
    airTime_ocn_list, program_ocn_list = read_ocn()
    print(airTime_ocn_list)
    print(program_ocn_list)


