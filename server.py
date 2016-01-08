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
	
# with app.test_request_context():
# 	print (url_for('hello_world'))
# 	print (url_for('login'))
# 	print (url_for('login', next='/', other_param='hah'))
# 	print (url_for('profile', username='John Doe'))

if __name__ == '__main__':
    app.run(debug=True)
    # to make externally visible:
    # app.run(host='0.0.0.0')
