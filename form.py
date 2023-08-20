from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired, URL
from flask_wtf import FlaskForm

class AddItem(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    link = StringField("Link", validators=[DataRequired()])
    img = StringField("Image Address", validators=[DataRequired()])
    submit = SubmitField("Add Item")
    