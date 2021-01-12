from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
from read_schedule import read_schedule

app = Flask(__name__)

GLOBAL_COUNT = 0
OCN_PATH = "http://ocn.tving.com/ocn/schedule?startDate="
OCN_DATA = ''

# html 파일 연결하기
from flask import render_template
@app.route('/')
def index():
    return render_template("index.html", data=OCN_DATA, data2=GLOBAL_COUNT)

def schedule_job():
    global GLOBAL_COUNT
    GLOBAL_COUNT = GLOBAL_COUNT+1

    global OCN_PATH, OCN_DATA
    OCN_DATA = read_schedule(OCN_PATH)

    print('GROVAL_COUNT:',GLOBAL_COUNT)
    print('I am working...')

if __name__ == '__main__':
    OCN_DATA = read_schedule(OCN_PATH)

    scheduler = BackgroundScheduler()
    job = scheduler.add_job(schedule_job, 'interval', minutes=1)
    scheduler.start()
    app.run()
    # app.run(host='0.0.0.0')