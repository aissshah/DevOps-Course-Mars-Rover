from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField, validators

class DateForm(FlaskForm):
  Date = DateField('Date', format='%d/%M/%Y', validators=validators.DataRequired)
  Explore = SubmitField('Explore')