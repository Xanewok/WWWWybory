from wybory import app

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/gowno')
def index2():
    return 'Hello World!'
