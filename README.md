# Hackathon Registration application

This application is built from [angular-seed](https://github.com/angular/angular-seed) for the front-end and [Flask](http://flask.pocoo.org/) for the REST backend.

# TL;DR (if you have pre-reqs):
```
git clone https://github.com/andrewalexander/hackpsu_registration.git
cd hackpsu_registration
sudo -HE npm install
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
    * Don't worry too much about the warnings. If you are that paranoid, you can research how to install different versions of python to put your mind at ease (you can do it with pip...)
- Install virtualenv: `sudo -HE pip install virtualenv`
    * I run the -HE options for two reasons:
        * Any scripts that install to `~` go to my actual user and not `/home/root/` (-H)
        * It pulls in my environment variables. Very handy if you have to set proxy or other env vars for applications (node...) (-E)

# Get the app working
- Navigate to a working directory of your choice. I tend to use `~/Projects/` but this is personal preference: `cd ~/Projects`
- Clone the repo in your working directory: `git clone https://github.com/andrewalexander/hackpsu_registration.git`
- Navigate to the directory you just cloned: `cd hackpsu_registration`
- Build everything the front end needs: `npm install`
    * Might need sudo depending on how/where node was installed: `sudo npm install`
- Start a front-end server and push it to the background (so you can run other things in the same Terminal window):
    * `python -m SimpleHTTPServer &` 
    * If you want to stop the server, type `fg` and then do `Ctrl+C` to move process to foreground and then kill it
- Build a virtualenv for the python/Flask backend: `virtualenv ~/envs/hackpsu_registration`
    * We do this so that any packages we install in the virtual environment do not overwrite any system packages that may be in use. 
- Activate virtualenv: `source ~/envs/hackpsu_registration/bin/activate`
    * You will see (hackpsu_registration) in front of your prompt: `(hackpsu_registration) $ `
    * This is how you know your virtual environment has been activated successfully.
- Build everything the backend needs: `pip install -r requirements.txt`
	* Because of the virtualenv, you don't need sudo for pip to install (unlike when we installed virtualenv earlier) and it won't mess with any of your system python packages (especially useful if you are on a *nix system that relies on Python for system functions)
- Run the backend server in a background process: `python server.py &`
- When you want to shut down the python server/backend, deactivate the virtualenv: `deactivate`

Now you can go to [http://127.0.0.1:8000/app/#/home](http://127.0.0.1:8000/app/#/home) and see the registration app in action

## Technical details
Web server listens at localhost:8000 by default and page is accessible at [http://127.0.0.1:8000/app/#/home](http://127.0.0.1:8000/app/#/home)

Backend listens at localhost:5000 by default and is accessible by one of its endpoints. See `server.py` for most recent endpoints accepted. 
* `localhost:5000/api/submit`
