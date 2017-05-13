from flask import Flask, render_template
app = Flask(__name__)

from prometheus_metrics import setup_metrics
setup_metrics(app)

@app.route('/')
def home():
    return render_template('index.html')
    #return "Flask Server Website"

@app.route('/firstPage')
def firstPage():
    return render_template('firstPage.html')

@app.route('/myCoolTopic')
def coolPage():
    return render_template('coolTopic.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
