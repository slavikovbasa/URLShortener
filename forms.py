from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators

class URLForm(FlaskForm):
    class Meta:
        csrf = False
    
    url = StringField('URL goes here', [validators.DataRequired()])
    submit = SubmitField('Shorten')

class LoginForm(FlaskForm):
    class Meta:
        csrf = False
    
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    submit = SubmitField('Sign In')