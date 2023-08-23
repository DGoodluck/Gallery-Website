from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired, URL, Length
from flask_wtf import FlaskForm

class AddItem(FlaskForm):
    name = StringField("Name")
    category = StringField("Category", validators=[DataRequired()])
    link = StringField("Link", validators=[DataRequired()])
    img = StringField("Image Address", validators=[DataRequired()])
    submit = SubmitField("Add Item")
    
class NewUser(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    submit = SubmitField("Register")

class LoginUser(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")