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
        all_users = scripts.get_attendees()
        if all_users:
            tmp = jsonify({'response': all_users})
            resp = flask.make_response(tmp, 200)
        else:
            tmp = jsonify({'error': 'Error communicating with database'})
            resp = flask.make_response(tmp, 500)
    return resp

@app.route('/api/submit', methods = ['POST'])
def submit(): 
    if request.method == 'POST':
        # validate the form before we do anything else
        form = scripts.validate_registration_field(request.data)
    if form:
        # now that it's good, add it to the database
        response = scripts.add_new_attendee(form)
    else:
        tmp = jsonify({'HTTPStatusCode': 400, 'message': 'ERROR: Invalid form'})
        resp = flask.make_response(tmp, 400)
    
    # build response to database update
    if response.get('ResponseMetadata', {}).get('HTTPStatusCode', 404) == 200:
        tmp = jsonify({'HTTPStatusCode': 200, 'message': 'Added user ' + form.email.data})
        resp = flask.make_response(tmp, 200)
    else:
        tmp = jsonify({'HTTPStatusCode': 500, 'message': 'Failed to update database'})
        resp = flask.make_response(tmp, 500)
    
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
