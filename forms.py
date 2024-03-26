from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, EmailField
from wtforms.validators import InputRequired


class LoginForm(FlaskForm):
    user_id = IntegerField('User ID:', validators=[InputRequired()])
    submit = SubmitField("Check Balances")


class VerificationForm(FlaskForm):
    name = StringField("Name:", validators=[InputRequired()])
    email = EmailField("Email:", validators=[InputRequired()])
    submit = SubmitField("Request Verification")


class ApproveForm(FlaskForm):
    user_id = IntegerField('User ID:', validators=[InputRequired()])
    name = StringField("Name:", validators=[InputRequired()])
    email = EmailField("Email:", validators=[InputRequired()])
    submit = SubmitField("Approve User")


class SetMaxForm(FlaskForm):
    max = IntegerField('New Maximum:', validators=[InputRequired()])
    submit = SubmitField("Set Maximum")