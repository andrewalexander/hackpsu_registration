# Hackathon Registration application

This application is built from [angular-seed](https://github.com/angular/angular-seed) for the front-end and [Flask](http://flask.pocoo.org/) for the REST backend.

# Prerequisites
- Be in a Mac/Linux environment (we use bash scripts; not tested on Cygwin/minGW)
- Install [homebrew](http://brew.sh/)
- Make sure you installed [Xcode](https://itunes.apple.com/us/app/xcode/id497799835?mt=12) and launched it at least once to install the Command Line tools you need (OSX Only obviously)

# Install fresh:
```
git clone https://github.com/andrewalexander/hackpsu_registration.git
cd hackpsu_registration
./install.sh
```
Once you have done the install once, any time you want to launch the server later, just run `./run_local.sh`

## Note on closing processes

The shell scripts start processes that are not in the current session. Just like the `install.sh` and `run_local.sh` scripts print out, to close the two running python processes that are running your web server and API backend, you must first find out the Process ID (PID) of each running process:

```
ps aux | grep python 
# Output:
ec2-user  2847  0.0  2.4 239508 25208 ?        S    00:52   0:01 python server.py
ec2-user  3310  0.2  1.3 199052 13372 pts/1    S    02:20   0:00 python -m SimpleHTTPServer
ec2-user  3312  0.0  0.2 110456  2220 pts/1    S+   02:20   0:00 grep --color=auto python
           ^ This is the PID column
```

Your output will look slightly different on a mac, but the number is still in the same place. Now that you have the PID, kill them both. Following our example above:

```
kill 2847
kill 3310
```

Now we verify that it is closed by running `ps aux | grep python` again. Since our grep process is the only one, we know the processes have been killed successfully. You can now re-run `./run_local.sh` without worrying about already open sockets.

```
ps aux | grep python
ec2-user  3314  0.0  0.2 110456  2112 pts/1    S+   02:22   0:00 grep --color=auto python
```

# Deeper details/what is going on inside the scripts
- Navigate to a working directory of your choice. I tend to use `~/Projects/` but this is personal preference: `cd ~/Projects`
- Clone the repo in your working directory: `git clone https://github.com/andrewalexander/hackpsu_registration.git`
- Navigate to the directory you just cloned: `cd hackpsu_registration`
- Build everything the front end needs: `npm install`
    * Might need sudo depending on how/where node was installed: `sudo npm install`
- Start a front-end server and push it to the background (so you can run other things in the same Terminal window):
    * `python -m SimpleHTTPServer &` 
    * If you want to stop the server, type `fg` and then do `Ctrl+C` to move process to foreground and then kill it
    * This doesn't apply to the scripts since when we run them with `./install.sh` or `./run_local.sh`, we invoke a new bash session. What this means is that the started processes are not in the scope of the current session, and so a typical `Ctrl+C` to quit doesn't work anymore. 
- Build a virtualenv for the python/Flask backend: `virtualenv ~/envs/hackpsu_registration`
    * We do this so that any packages we install in the virtual environment do not overwrite any system packages that may be in use. 
- Activate virtualenv: `source ~/envs/hackpsu_registration/bin/activate`
    * You will see (hackpsu_registration) in front of your prompt: `(hackpsu_registration) $ `
    * This is how you know your virtual environment has been activated successfully.
- Build everything the backend needs: `pip install -r requirements.txt`
	* Because of the virtualenv, you don't need sudo for pip to install (unlike when we installed virtualenv earlier) and it won't mess with any of your system python packages (especially useful if you are on a *nix system that relies on Python for system functions)
- Run the backend server in a background process: `python server.py &`
- When you want to shut down the python server/backend, deactivate the virtualenv: `deactivate`

Now you can go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) and see the registration app in action

## Technical details
Web server listens at localhost:8000 by default and page is accessible at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

Backend listens at localhost:5000 by default and is accessible by one of its endpoints. See `server.py` for most recent endpoints accepted. 
* `localhost:5000/api/submit`
