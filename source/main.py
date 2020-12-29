from flask import Flask
app = Flask(__name__)



# html 파일 연결하기
from flask import render_template
@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(threaded=True)
    # app.run(host='0.0.0.0')