import flask
import json
import scripts
import multiprocessing
from flask import Flask, render_template, jsonify, request
from flask.ext.cors import CORS
app = Flask(__name__)
CORS(app, resources=r'/api/*', allow_headers=['Content-Type', 'Access-Control-Allow-Origin', 'Access-Control-Allow-Headers'])


@app.route('/')
def index():
    val = flask.request.args
    # return val
    # return 
    resp = flask.make_response(render_template('index.html'), 200)


@app.route('/login/<val>', methods=['GET'])
def login(val):
    # val = flask.request.args.get('test')
    tmp = jsonify({'value': val})
    resp =  flask.make_response((tmp, 200))
    return resp

@app.route('/api/users/', methods=['GET'])
@app.route('/api/users/<id>/', methods=['GET'])
def profile(id = None): 
    if id:
        # get specified user
        tmp = jsonify({'response': id})
        resp = flask.make_response(tmp, 200)
        
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
    if form and not form.errors:
        # now that it's good, add it to the database
        response = scripts.add_new_attendee(form)
        
        # catch our custom errors first
        if response.get('error_response'):
            if response.get('error_response') == 'user_exists':
                tmp = jsonify({'HTTPStatusCode': 200, 'message': 'user_exists'})
                resp = flask.make_response(tmp, 200)

                # get out of there, she's gonna blow!
                return resp

        # build response to database update
        if response and response.get('aws_response', {}).get('ResponseMetadata', {}).get('HTTPStatusCode', 0) == 200:
            tmp = jsonify({'HTTPStatusCode': 200, 'message': 'Added user'})
            resp = flask.make_response(tmp, 200)

            # now start a background process to send the email out, passing in hash
            jobs = []
            data = response.get('new_attendee')
            p = multiprocessing.Process(target=send_email, args=tuple(data.items()))
            jobs.append(p)
            p.start()

        else:
            tmp = jsonify({'HTTPStatusCode': 500, 'message': 'Failed to update database'})
            resp = flask.make_response(tmp, 500)
    elif form and form.errors:
        tmp = jsonify({'HTTPStatusCode': 400, 'message': form.errors})
        resp = flask.make_response(tmp, 400)
    else:
        tmp = jsonify({'HTTPStatusCode': 400, 'message': 'Failed to validate form'})
        resp = flask.make_response(tmp, 400)
    
    return resp

@app.route('/api/rsvp', methods = ['POST'])
def rsvp():
    if request.method == 'POST':
        print request.data
        form = scripts.validate_rsvp_field(request.data)
    if form:
        response = scripts.add_rsvp(form.data)
        # catch our custom errors first
        if response.get('error_response'):
            if response.get('error_response') == 'user_exists':
                tmp = jsonify({'HTTPStatusCode': 200, 'message': 'user_exists'})
                resp = flask.make_response(tmp, 200)

                # no sense checking the rest
                return resp

        if response and response.get('aws_response', {}).get('ResponseMetadata', {}).get('HTTPStatusCode', 0) == 200:
            tmp = jsonify({'HTTPStatusCode': 200, 'message': response.get('error_response')})
            resp = flask.make_response(tmp, 200)

        else:
            tmp = jsonify({'HTTPStatusCode': 500, 'message': response})
            resp = flask.make_response(tmp, 500)
    else:
        tmp = jsonify({'HTTPStatusCode': 400, 'message': {'error_response': request.data}})
        resp = flask.make_response(tmp, 400)

    return resp



def send_email(*args, **kwargs):
    form = dict(args)
    scripts.send_registration_email(form)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
