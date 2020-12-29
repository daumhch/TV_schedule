import threading
import datetime
import time

def Threading(sec):
    while True:
        print(datetime.datetime.now())
        time.sleep(sec)
    
t1 = threading.Thread(target=Threading, args=(3,))
t1.start()



