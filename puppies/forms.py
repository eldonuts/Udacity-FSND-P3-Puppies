from wtforms import Form, SelectField, StringField, validators
from wtforms.fields.html5 import DateField
from wtforms_components import DateRange
from datetime import date



class PuppiesForm(Form):

    name            = StringField('Name', [validators.Length(min=4, max=25)])
    gender          = SelectField('Gender')
    dateofbirth     = DateField('Date of Birth', validators=[DateRange(max=date.today(),message='Cannot occur in future')])
    shelter         = SelectField('Shelter', coerce=int)