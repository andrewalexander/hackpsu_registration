import boto3
import json
import wtforms_json
from flask import Flask, render_template
from botocore.exceptions import ClientError
from wtforms import Form, BooleanField, StringField, IntegerField, FieldList, validators

app = Flask(__name__)


ethnicity_field = StringField('Ethnicity', [validators.Length(min=5, max=15), validators.Optional()])
dietary_field = StringField('Dietary restrictions', [validators.Length(min=5, max=15), validators.Optional()])


class RegistrationForm(Form):
    first_name    = StringField('First Name', [validators.Length(min=2, max=25), validators.InputRequired()])
    last_name    = StringField('Last Name', [validators.Length(min=2, max=25), validators.InputRequired()])
    email        = StringField('Email Address', [validators.Length(min=6, max=35), validators.InputRequired()])
    age          = IntegerField('Age', [validators.NumberRange(min=10, max=125), validators.InputRequired()])
    cell         = IntegerField('Phone', [validators.NumberRange(min=0, max=9999999999), validators.InputRequired()])
    year         = IntegerField('Year in school', [validators.NumberRange(min=0, max=6), validators.InputRequired()])
    shirt_size   = StringField('Shirt Size', [validators.Length(min=1, max=1), validators.InputRequired()])
    reimbursement= BooleanField('Reimbursement needed', [validators.DataRequired()])
    no_edu       = BooleanField('No .edu email', [validators.Optional()])
    gender       = StringField('Gender', [validators.Optional()])
    ethnicity    = FieldList(ethnicity_field)
    dietary      = FieldList(dietary_field)
    other_dietary= StringField('Other dietary restrictions', [validators.Length(min=2, max=35), validators.Optional()])
    first        = BooleanField('First hackathon', [validators.Optional()])

def validate_registration_field(attendee):
    wtforms_json.init()

    form = RegistrationForm.from_json(json.loads(attendee))
    if form.validate():
        return form
    else:
        print 'invalid'
        return None


def config_db():
    pass


def get_attendees(max_items='25'):
    pass


def generate_unique_url(attendee_id):
    pass


def update_attendee_entries(attendee_list):
    pass


def send_emails(attendee_list):
    pass


def send_alerts(sns_topic):
    pass


def add_new_attendee(attendee):
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
    'first': attendee.first.data}

    print new_attendee


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
                        'AttributeName': 'username',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'last_name',
                        'KeyType': 'RANGE'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'username',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'last_name',
                        'AttributeType': 'S'
                    },

                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
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


# handling user on the rsvp URL
# assume params will be stripped from request URL
def get_attendee_from_db(params):
    attendee_id = params.attendee_id
    pass
