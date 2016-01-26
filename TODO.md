# TODO
- use `url_for` to generate unique urls for attendees
	- have this feed into database
- set up database
	- ~build schema~
    - build create database method 
        * pending refactor
    - seed database with data
        * build class/function for registration data
- build DB connector
    - when submitting, check if entry exists - update/create accordingly with appropriate response
        - based off of... email? hash?
    - adds in all relevant server-side fields (checking for RSVP, etc.)
- build form for people to fill out
- build out RSVP page 
	- uses hash from URL param to pull from database 
	- mark accordingly; save to DB
    - build route - figure out how to pull params from the URL into python datatypes/primitives
- build section for corporate sponsors to respond with who they will be sending