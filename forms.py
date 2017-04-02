from wtforms import Form, TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField, SelectMultipleField, BooleanField, StringField, validators, ValidationError, HiddenField

class Acquire_Feed_Form(Form):

    trends_url = TextField('turl', [validators.required()])

class Download_CSV(Form):
    csv_name = HiddenField()
    csv_file = HiddenField()
