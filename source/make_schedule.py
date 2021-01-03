import threading
import datetime
import time

from read_schedule import read_schedule

def Threading(sec):
    while True:
        OCN_PATH = "http://ocn.tving.com/ocn/schedule?startDate="
        airTime_ocn_list, program_ocn_list = read_schedule(OCN_PATH)
        print(airTime_ocn_list)
        print(program_ocn_list)
        print(datetime.datetime.now())
        time.sleep(sec)
    
t1 = threading.Thread(target=Threading, args=(5,))
t1.start()

# 근데 이러면 5초마다 수행되지 않는다. 플라스크로 구현해보자

