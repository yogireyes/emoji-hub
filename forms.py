from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Regexp
from models import User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=4, max=20)]
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8),
            EqualTo("confirm_password", message=" Both password must match! "),
            Regexp(
                r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^\w\d\s]).{6,12}$",
                message="Please enter a password with at least one uppercase letter, one lowercase letter, one number, and one special character.",
            ),
        ],
    )
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already exists.")
