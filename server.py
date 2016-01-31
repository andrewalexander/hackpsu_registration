import flask
import json
import scripts
from flask import Flask, render_template, jsonify, request
from flask.ext.cors import CORS
app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    val = flask.request.args
    # return val
    return render_template('index.html')


@app.route('/login/<val>', methods=['GET'])
def login(val):
    # val = flask.request.args.get('test')
    tmp = jsonify({'value': val})
    resp =  flask.make_response((tmp, 200))
    return resp

@app.route('/api/users/')
@app.route('/api/users/<id>/')
def profile(id = None): 
    if id:
        # get specified user
        tmp = jsonify({'response': id})
        
    else:
        # get all users from database
        tmp = jsonify({'response': 'This will eventually get the users that are registered'})

    resp = flask.make_response(tmp, 200)
    return resp

@app.route('/api/submit/', methods = ['POST'])
def submit(): 
    if request.method == 'POST':
        # create new user in database
        form = scripts.validate_registration_field(request.data)
    if form:
        scripts.add_new_attendee(form)

    tmp = jsonify({'response': 200})
    resp = flask.make_response(tmp, 200)
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
