from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, Form
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, ValidationError

# Form where user can choose stocks to get data for in a given time period
class StocksForm(FlaskForm):
    stock1 = StringField('Stock ticker', validators=[DataRequired(), Length(min=1, max=4)])
    stock2 = StringField('Stock ticker', validators=[Length(max=4)])
    stock3 = StringField('Stock ticker', validators=[Length(max=4)])
    stock4 = StringField('Stock ticker', validators=[Length(max=4)])
    stock5 = StringField('Stock ticker', validators=[Length(max=4)])
    start_date = DateField('Start date', validators=[DataRequired()])
    end_date = DateField('End date', validators=[DataRequired()])
    submit = SubmitField('Submit')
