from flask import Flask, url_for, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

# def index(): pass

@app.route('/login')
def login(): pass

@app.route('/user/<username>')
def profile(username): pass

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
	
if __name__ == '__main__':
    app.run(debug=True)
    # to make externally visible:
    # app.run(host='0.0.0.0')
