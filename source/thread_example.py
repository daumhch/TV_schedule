import threading
from time import sleep

def Threading(id):
    print(id)

def thProc(id, sec):
    while True:
        Threading(id)
        sleep(sec)
    
t1 = threading.Thread(target=thProc, args=("Test1",1))
t1.start()



