from flask import Flask, render_template
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


# handling user on the rsvp URL
# assume params will be stripped from request URL
def get_attendee_from_db(params):
    attendee_id = params.attendee_id
    pass
