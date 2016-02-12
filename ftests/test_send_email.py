import scripts
import wtforms_json
import json

new_attendee = {'first_name': 'Andrew',
    'last_name': 'Alexander',
    'email': 'andrewalex1992@gmail.com',
    'age': 24,
    'cell': 5558675309,
    'year': 6,
    'shirt_size': 'm',
    'reimbursement': False,
    'no_edu': False,
    'gender': 'Male',
    'ethnicity': [],
    'dietary': [],
    'other_dietary': [],
    'first': False,
    'user_id': '865309ab36cd12e'}

# wtforms_json.init()
# form = scripts.RegistrationForm.from_json(new_attendee)

# if form.validate():
scripts.send_registration_email(new_attendee)
print 'passed'
# else:
# 	print form.errors