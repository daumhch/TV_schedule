from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)



# html 파일 연결하기
from flask import render_template
@app.route('/')
def index():
    return render_template("index.html")

def schedule_job():
    print('I am working...')

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    job = scheduler.add_job(schedule_job, 'interval', minutes=1/60)
    scheduler.start()
    app.run()
    # app.run(host='0.0.0.0')