import threading
import datetime
import time

from read_ocn import read_ocn

def Threading(sec):
    while True:
        print(datetime.datetime.now())
        airTime_ocn_list, program_ocn_list = read_ocn()
        print(airTime_ocn_list)
        print(program_ocn_list)
        time.sleep(sec)
    
t1 = threading.Thread(target=Threading, args=(3,))
t1.start()



