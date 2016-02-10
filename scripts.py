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
config = Config()

# define the WTForm for easy validation
class RegistrationForm(Form):
    first_name   = StringField('First Name', [validators.Length(min=2, max=25), validators.InputRequired()])
    last_name    = StringField('Last Name', [validators.Length(min=2, max=25), validators.InputRequired()])
    email        = StringField('Email Address', [validators.Email(), validators.InputRequired()])
    age          = IntegerField('Age', [validators.NumberRange(min=10, max=125), validators.InputRequired()])
    cell         = IntegerField('Phone', [validators.NumberRange(min=0, max=9999999999), validators.InputRequired()])
    year         = IntegerField('Year in school', [validators.NumberRange(min=0, max=6), validators.InputRequired()])
    shirt_size   = StringField('Shirt Size', [validators.Length(min=1, max=4), validators.InputRequired()])
    reimbursement= BooleanField('Reimbursement needed', [])
    no_edu       = BooleanField('No .edu email', [validators.Optional()])
    gender       = StringField('Gender', [validators.Optional()])
    ethnicity    = FieldList(config.ethnicity_field)
    dietary      = FieldList(config.dietary_field)
    other_dietary= StringField('Other dietary restrictions', [validators.Length(min=2, max=35), validators.Optional()])
    first        = BooleanField('First hackathon', [validators.Optional()])
    user_id      = StringField('User ID', [validators.Length(min=36, max=36), validators.Optional()])

class RsvpForm(Form):
    email        = StringField('Email Address', [validators.Email(), validators.InputRequired()])
    cell         = IntegerField('Cell Phone', [validators.NumberRange(min=0, max=9999999999), validators.InputRequired()])
    user_id      = StringField('User ID', [validators.Length(min=36, max=36), validators.InputRequired()])


def validate_registration_field(attendee):
    wtforms_json.init()
    # clean up the phone number
    form = RegistrationForm.from_json(json.loads(attendee))
    if form.validate():
        return form


def validate_rsvp_field(form):
    wtforms_json.init()

    form = RsvpForm.from_json(json.loads(form))
    if form.validate():
        return form


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
                'first': entry.get('first', {}).get('BOOL', '')
                })
        return all_users
    else:
        return None


# handling user on the rsvp URL
# assume params will be stripped from request URL
def get_attendee_from_db(attendee_id):
    attendee_id = params.attendee_id
    pass



def send_registration_email(form_data):
    ses = boto3.client('ses', region_name='us-east-1')
    
    # get the message file
    with open(os.path.expanduser('./email_templates/message.json')) as message_file:
        message = json.load(message_file)
    
    message['Body']['Html']['Data'] = message['Body']['Html']['Data'].format(first_name=form_data.get('first_name'), user_id=form_data.get('user_id'))

    # this is temporary
    with open(os.path.expanduser('./email_templates/destination.json')) as destination_file:
        destination = json.load(destination_file)

    source = 'registration@hackpsu.org'
    # source = 'andrewalex1992@gmail.com'

    response = ses.send_email(
        Source=source,
        Destination=destination,
        Message=message
    )

    return response


def send_emails(attendee_list):
    pass


def send_alerts(sns_topic):
    pass


def add_new_attendee(attendee):
    config = Config()

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
    'user_id': str(user_id)}

    # Need to check for empties since DynamoDB complains
    for key, value in new_attendee.iteritems():
        if not value:
            new_attendee[key] = 'Null'

    # get our db and put the new item in
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    try:
        table = dynamodb.Table(config.db_name)
        response = table.put_item(Item=new_attendee)    
    except ClientError, e:
        return None

    res = {'aws_response': response,
           'new_attendee': new_attendee}
    return res

def add_rsvp(rsvp_data):
    client = boto3.client('dynamodb', region_name='us-east-1')

    aws_response = client.get_item(TableName=config.db_name, Key = {'email': { 'S': rsvp_data.get('email')}})
    rsvp_response = None
    if aws_response.get('ResponseMetadata', {}).get('HTTPStatusCode', 0) == 200:
        # make sure IDs match using email as key
        if aws_response.get('Item').get('user_id').get('S') == rsvp_data.get('user_id')\
        and int(aws_response.get('Item').get('cell').get('N')) == rsvp_data.get('cell'):
            new_item = aws_response.get('Item')
            new_item.update({'rsvp': {'BOOL': True}})
            
            rsvp_response = client.put_item(TableName=config.db_name, Item=new_item)

    response = {'aws_response': aws_response,
                'rsvp_response': rsvp_response}
            
    return response


def seed_db(db_name):
    dynamodb = boto3.resource('dynamodb')

    # TODO: switch to a config json
    # with open('test_hackpsu_table_config.json') as table_config:
    #     config = json.load(table_config)
    try:
        # Try to get an existing database
        table = dynamodb.Table(name=db_name)
        table.load()
    except ClientError as e:
        # create database since it doesn't exist
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            # TODO: switch to a config json
            # table = dynamodb.create_table(
            #     TableName=config.TableName,
            #     KeySchema=config.KeySchema,
            #     AttributeDefinitions=config.AttributeDefinitions,
            #     ProvisionedThroughput=config.ProvisionedThroughput
            # )
            table = dynamodb.create_table(
                TableName=db_name,
                KeySchema=[
                    {
                        'AttributeName': 'email',
                        'KeyType': 'HASH'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'email',
                        'AttributeType': 'S'
                    }

                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 1
                }
            )
        else:
            # if we got a different exception, it wasn't a good thing; let's get out
            raise e
    try:
        # Wait until the table exists.
        table.meta.client.get_waiter('table_exists').wait(TableName=db_name)
    
    except ClientError as e:
        raise e

    return table
