from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, RadioField,FloatField, DateField, SelectField, SubmitField, FileField
from wtforms.validators import DataRequired, length, equal_to, Email



class RegisterForm(FlaskForm):
    username = StringField("your username", validators=[DataRequired()])
    email = StringField("your email", validators=[DataRequired(), Email()])
    password = PasswordField("your password", validators=[DataRequired(), length(min=6, max=64, message="password must be between 6 and 64 characters long")])
    repeat_password = PasswordField("repeat password", validators=[DataRequired(), equal_to("password", message="passwords must be identical")])

    submit = SubmitField("register")


class LoginForm(FlaskForm):
    username = StringField("name")
    email = StringField("email")
    password = PasswordField("password" , validators=[DataRequired()])

    login = SubmitField("Login")



class ProductForm(FlaskForm):
    image = FileField("product image", validators=[FileAllowed(["png", "jpg", "jpeg"])])

    name = StringField("product name")
    price = FloatField("product price")

    submit = SubmitField("Add Product")


class SearchForm(FlaskForm):
    query = StringField("search", validators=[DataRequired()])
    submit = SubmitField("Search")

class DestinationForm(FlaskForm):

    image = FileField(
        "destination image",
        validators=[FileAllowed(["png", "jpg", "jpeg"])]
    )
    name = StringField("destination name", validators=[DataRequired()])
    price = FloatField("destination price", validators=[DataRequired()])
    submit = SubmitField("Save Destination")




