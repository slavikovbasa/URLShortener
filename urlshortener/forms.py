from .models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, ValidationError, URL

class URLForm(FlaskForm):
    class Meta:
        csrf = False
    
    url = StringField('URL goes here', [DataRequired(), URL()])
    submit = SubmitField('Shorten')


class LoginForm(FlaskForm):
    class Meta:
        csrf = False
    
    username = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Please use a different username.')
