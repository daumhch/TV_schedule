from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
from read_schedule import read_schedule

app = Flask(__name__)

GLOBAL_COUNT = 0

# html 파일 연결하기
from flask import render_template
@app.route('/')
def index():
    return render_template("index.html", data=GLOBAL_COUNT)

def schedule_job():
    global GLOBAL_COUNT
    GLOBAL_COUNT = GLOBAL_COUNT+1
    print('GROVAL_COUNT:',GLOBAL_COUNT)
    print('I am working...')

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    job = scheduler.add_job(schedule_job, 'interval', minutes=1/60)
    scheduler.start()
    app.run()
    # app.run(host='0.0.0.0')