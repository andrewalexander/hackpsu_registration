from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login(): pass


@app.route('/user/<username>')
def profile(username): pass


@app.route('/foo', methods=['GET', 'POST'])
def foo(x=None, y=None):
    # do something to send email
    pass
# template

# <form action="/foo" method="post">
#     <button type="submit" value="Send Email" />
# </form>


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
    # to make externally visible:
    # app.run(host='0.0.0.0')
