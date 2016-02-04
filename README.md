# Hackathon Registration application

This application is built from [angular-seed](https://github.com/angular/angular-seed) for the front-end and [Flask](http://flask.pocoo.org/) for the REST backend.

# TL;DR (if you have pre-reqs):
```
git clone https://github.com/andrewalexander/hackpsu_registration.git
npm install
python -m SimpleHTTPServer &
virtualenv ~/envs/hackpsu_registration
source ~/envs/hackpsu_registration/bin/activate
pip install -r requirements.txt
python server.py &
# when you are done running backend:
deactivate
```

# Prerequisites
- Install [node.js](https://nodejs.org/en/download/) (do it all.... you want everything)
- Install [pip](https://pip.pypa.io/en/stable/installing/)
    * Download the `get-pip.py` installer and run it with `sudo python get-pip.py`
- Install virtualenv: `pip install virtualenv`

# Get the app working
- Clone the repo: `git clone https://github.com/andrewalexander/hackpsu_registration.git`
- Build everything the front end needs: `npm install`
- Start a front-end server and push it to the background (so you can run other things in the same Terminal window):
    * `python -m SimpleHTTPServer &` 
    * If you want to stop the server, type `fg` and then do `Ctrl+C` to move process to foreground and then kill it
- Build a virtualenv (to keep everything isolated): `virtualenv ~/envs/hackpsu_registration`
- Activate virtualenv: `source ~/envs/hackpsu_registration/bin/activate`
- Build everything the backend needs: `pip install -r requirements.txt`
	* Because of the virtualenv, you don't need sudo and it won't mess with your system python packages.
- Run the backend server in a background process: `python server.py &`
- When you are done, deactivate the virtualenv: `deactivate`

Now you can go to [http://127.0.0.1:8000/app/#/home](http://127.0.0.1:8000/app/#/home) and see the registration app in action

## Technical details
Web server listens at localhost:8000 by default and page is accessible at [127.0.0.1:8000/app](127.0.0.1:8000/app).

Backend listens at localhost:5000 by default and is accessible by one of its endpoints. See `server.py` for most recent endpoints accepted. 
