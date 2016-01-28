import flask
from flask import Flask, render_template, jsonify
from flask.ext.cors import CORS
app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    val = flask.request.args
    # return val
    # return render_template('index.html')


@app.route('/login/<val>', methods=['GET'])
def login(val):
    # val = flask.request.args.get('test')
    tmp = jsonify({'value': val})
    # resp =  flask.Response(response=tmp,
    #     status=200,
    #     mimetype="application/json")
    return(tmp)

@app.route('/user/<id>')
def profile(id): 
    tmp = jsonify({'value': id})
    return(tmp)

@app.route('/foo', methods=['GET', 'POST'])
def foo():
    # do something to send email
    
    return flask.jsonify(**tmp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    # to make externally visible:
    # app.run(host='0.0.0.0')
