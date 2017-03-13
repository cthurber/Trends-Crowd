from wtforms import Form, TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField, SelectMultipleField, BooleanField, StringField, validators, ValidationError

class Acquire_Feed_Form(Form):

    trends_url = TextField('turl', [validators.required()])
