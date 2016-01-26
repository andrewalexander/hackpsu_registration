# Hackathon Registration application

This application is built from [angular-seed](https://github.com/angular/angular-seed) for the front-end and [Flask](http://flask.pocoo.org/) for the REST backend.

To run webserver and backend

    ```
    npm install
    npm start
    python server.py
    ```

`npm install` is configured to do a bower install as well.

Web server listens at localhost:8000 by default and page is accessible at [127.0.0.1:8000/app](127.0.0.1:8000/app).

Backend listens at localhost:5000 by default and is accessibly by one of its endpoints. See `server.py` for most recent endpoints accepted. 