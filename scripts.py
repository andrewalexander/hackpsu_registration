import boto3
import json
from flask import Flask, render_template
from botocore.exceptions import ClientError

app = Flask(__name__)

# this will be a placeholder for all functions until some better way to organize them makes itself known


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
