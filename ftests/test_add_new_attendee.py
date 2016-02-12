import scripts
import json

with open('form_data.json') as form_file:
	attendee = json.load(form_file)
# attendee = {"first_name":"Andrew","last_name":"Alexander","email":"andrewalex1992@gmail.com","cell":8142322883,"reimbursement":False,"first":False,"ethnicity":["other"],"dietary":["allergy_egg"],"age":24,"gender":"male","year":"6","shirt_size":"m"}

# att_dict = json.dumps(attendee)

# counter = 0 
# for i in att_dict.iteritems():
# 	counter = counter + 1
# 	print counter
# 	print i
form = scripts.validate_registration_field(json.dumps(attendee))
resp = scripts.add_new_attendee(form)

print resp 