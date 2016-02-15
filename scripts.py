import boto3
import json
import wtforms_json
import uuid
import os
import re
from flask import Flask, render_template
from botocore.exceptions import ClientError
from wtforms import Form, BooleanField, StringField, IntegerField, FieldList, validators

# instantiate our Flask app
app = Flask(__name__)

# build Config object
class Config():
    def __init__(self):
        self.db_name = 'hackpsu_registration'
        self.ethnicity_field = StringField('Ethnicity', [validators.Length(min=5, max=15), validators.Optional()])
        self.dietary_field = StringField('Dietary restrictions', [validators.Length(min=5, max=15), validators.Optional()])
        self.source_email = 'registration@hackpsu.org'
config = Config()

# define the WTForm for easy validation
class RegistrationForm(Form):
    first_name      = StringField('First Name', [validators.Length(min=2, max=25), validators.InputRequired()])
    last_name       = StringField('Last Name', [validators.Length(min=2, max=25), validators.InputRequired()])
    email           = StringField('Email Address', [validators.Email(), validators.InputRequired()])
    age             = IntegerField('Age', [validators.NumberRange(min=10, max=125), validators.InputRequired()])
    cell            = IntegerField('Phone', [validators.NumberRange(min=0, max=9999999999), validators.InputRequired()])
    year            = IntegerField('Year in school', [validators.NumberRange(min=0, max=6), validators.InputRequired()])
    shirt_size      = StringField('Shirt Size', [validators.Length(min=1, max=4), validators.InputRequired()])
    reimbursement   = BooleanField('Reimbursement needed', [])
    no_edu          = BooleanField('No .edu email', [validators.Optional()])
    gender          = StringField('Gender', [validators.Optional()])
    ethnicity       = FieldList(config.ethnicity_field)
    dietary         = FieldList(config.dietary_field)
    other_dietary   = StringField('Other dietary restrictions', [validators.Length(min=2, max=35), validators.Optional()])
    first           = BooleanField('First hackathon', [validators.Optional()])
    github          = StringField('Github URL', [validators.Length(min=2, max=25), validators.Optional()])
    linkedin        = StringField('LinkedIn URL', [validators.Length(min=2, max=25), validators.Optional()])
    website         = StringField('Website URL', [validators.Length(min=2, max=25), validators.Optional()])
    university      = StringField('University attended', [validators.Length(min=2, max=100), validators.Optional()])
    travel_address  = StringField('Hopme location travelling from', [validators.Length(min=2, max=100), validators.Optional()])
    software_skills = StringField('Software skills/frameworks', [validators.Length(min=2, max=150), validators.Optional()])
    hardware_skills = StringField('Hardware skills', [validators.Length(min=2, max=150), validators.Optional()])
    travel_from_university = BooleanField('Travelling from university', [validators.Optional()])

class RsvpForm(Form):
    email        = StringField('Email Address', [validators.Email(), validators.InputRequired()])
    cell         = IntegerField('Cell Phone', [validators.NumberRange(min=0, max=9999999999), validators.InputRequired()])
    user_id      = StringField('User ID', [validators.Length(min=36, max=36), validators.InputRequired()])


def validate_registration_field(attendee):
    wtforms_json.init()
    form = RegistrationForm.from_json(json.loads(attendee))
    
    # if form.validate():
    return form



def validate_rsvp_field(form):
    wtforms_json.init()

    form = RsvpForm.from_json(json.loads(form))
    if form.validate():
        return form
    else:
        print 'validation errors:'
        print form.errors


def config_db():
    pass


def get_attendees():
    client = None
    client = boto3.client('dynamodb')
    all_users = []

    response = client.scan(TableName=config.db_name)
    
    if response and response.get('ResponseMetadata').get('HTTPStatusCode') == 200:
        for entry in response.get('Items'):
            all_users.append({
                'first_name': entry.get('first_name', {}).get('S', ''),
                'last_name': entry.get('last_name', {}).get('S', ''),
                'email': entry.get('email', {}).get('S', ''),
                'age': entry.get('age', {}).get('N', ''),
                'cell': entry.get('cell', {}).get('N', ''),
                'year': entry.get('year', {}).get('N', ''),
                'shirt_size': entry.get('shirt_size', {}).get('S', ''),
                'reimbursement': entry.get('reimbursement', {}).get('BOOL', ''),
                'no_edu': entry.get('no_ed', {}).get('BOOL', ''),
                'gender': entry.get('gender', {}).get('S', ''),
                'ethnicity': [item.get('S') for item in entry.get('ethnicity', {}).get('L', '')],
                'dietary': [item.get('S') for item in entry.get('dietary', {}).get('L', '')],
                'other_dietary': entry.get('other_dietary', {}).get('S', ''),
                'first': entry.get('first', {}).get('BOOL', ''),
                'user_id': entry.get('user_id', {}).get('S', ''),
                'rsvp': entry.get('rsvp', {}).get('BOOL', ''),
                'github': entry.get('github', {}).get('S', ''),
                'linkedin': entry.get('linkedin', {}).get('S', ''),
                'website': entry.get('website', {}).get('S', ''),
                'university': entry.get('university', {}).get('S', ''),
                'travel_address': entry.get('travel_address', {}).get('S', ''),
                'software_skills': entry.get('software_skills', {}).get('S', ''),
                'hardware_skills': entry.get('hardware_skills', {}).get('S', ''),
                'travel_from_university': entry.get('travel_from_university', {}).get('BOOL', ''),
                })
        return all_users
    else:
        return None


# handling user on the rsvp URL
# assume params will be stripped from request URL
def get_attendee_from_db(attendee_key):
    client = boto3.client('dynamodb', region_name='us-east-1')
    
    error_response = None
    try:
        aws_response = client.get_item(TableName=config.db_name, Key = {'email': { 'S': attendee_key}})
    except ClientError, e:
        error_response = dict(e)

    res = {'aws_response': aws_response,
           'error_response': error_response}
    
    return res


def send_email(email, data):
    ses = boto3.client('ses', region_name='us-east-1')
    
    with open('./email_templates/destination.json') as destination_file:
        destination = json.load(destination_file)

    destination['ToAddresses'][0] = destination['ToAddresses'][0].format(email=email)

    source = config.source_email
    response = ses.send_email(
        Source=source,
        Destination=destination,
        Message=data
    )

    return response

def send_registration_email(form_data):
   
    with open('./email_templates/registration_email.json') as message_file:
        message = json.load(message_file)
    
    # Read in the message and replace the first name with the entered first name; also get the user_id to build the response URL
    message['Body']['Html']['Data'] = message['Body']['Html']['Data'].format(first_name=form_data.get('first_name'))
    email = form_data.get('email')
    response = send_email(email, message)

    return response


def send_emails(attendee_list):
    pass


def send_alerts(sns_topic):
    pass


def add_new_attendee(attendee):
    # generate a unique hash/uuid:
    user_id = uuid.uuid3(uuid.NAMESPACE_DNS, str(attendee.email.data))

    # build the db entry
    new_attendee = {'first_name': attendee.first_name.data,
    'last_name': attendee.last_name.data,
    'email': attendee.email.data,
    'age': attendee.age.data,
    'cell': attendee.cell.data,
    'year': attendee.year.data,
    'shirt_size': attendee.shirt_size.data,
    'reimbursement': attendee.reimbursement.data,
    'no_edu': attendee.no_edu.data,
    'gender': attendee.gender.data,
    'ethnicity': attendee.ethnicity.data,
    'dietary': attendee.dietary.data,
    'other_dietary': attendee.other_dietary.data,
    'first': attendee.first.data,
    'user_id': str(user_id),
    'github': attendee.github.data,
    'linkedin': attendee.linkedin.data,
    'website': attendee.website.data,
    'university': attendee.university.data,
    'travel_address': attendee.travel_address.data,
    'software_skills': attendee.software_skills.data,
    'hardware_skills': attendee.hardware_skills.data,
    'travel_from_university': attendee.travel_from_university.data
    }

    # check if the user exists already
    # get our db and put the new item in
    response = get_attendee_from_db(new_attendee.get('email'))
    error_response = None
    # if it was able to get an entry, you have already registered...
    if response.get('aws_response', {}).get('Item', ''):
        error_response = 'user_exists'
        res = {'aws_response': response,
               'error_response': error_response}
        
        return res        

    # check for "travel_from_university" boolean and set travel_address accordingly:
    if new_attendee.get('travel_from_university') and new_attendee.get('travel_from_university') == False:
        new_attendee['travel_address'] = new_attendee.get('university')

    # Need to check for empties since DynamoDB complains about empty attributes
    for key, value in new_attendee.iteritems():
        if not value:
            new_attendee[key] = 'Null'
    
    try:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        try:
            table = dynamodb.Table(config.db_name)
            response = table.put_item(Item=new_attendee)  
        except ClientError, e:
            pass
    except ClientError, e:
        response = dynamodb

    res = {'aws_response': response,
           'error_response': error_response,
           'new_attendee': new_attendee}
    return res


def add_rsvp(rsvp_data): 
    response = get_attendee_from_db(rsvp_data.email)

    # return error
    if response.get('error_response', ''):
        return response

    aws_response = response.get('aws_response')

    if aws_response.get('ResponseMetadata', {}).get('HTTPStatusCode', 0) == 200:
        # first check if they've already RSVPd
        if aws_response.get('Item').get('rsvp', False) == False:
            # validation
            if aws_response.get('Item').get('user_id').get('S') == rsvp_data.get('user_id')\
            and int(aws_response.get('Item').get('cell').get('N')) == rsvp_data.get('cell'):
                new_item = aws_response.get('Item')
                new_item.update({'rsvp': {'BOOL': True}})
            
            aws_response = client.put_item(TableName=config.db_name, Item=new_item)
        else:
            error_response = 'user_exists'

    response = {'aws_response': aws_response, 'error_response': error_response}
            
    return response
