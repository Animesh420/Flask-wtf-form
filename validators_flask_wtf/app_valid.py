from flask import render_template, Flask, request, url_for
import os

from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField,DateField, EmailField, PasswordField, IntegerField

from wtforms.validators import InputRequired, EqualTo, DataRequired, Length, ValidationError, NumberRange


a = [InputRequired(), DataRequired(), NumberRange(min=12, max=20)]



app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config["WTF_CSRF_ENABLED"] = False

class StudentForm(FlaskForm):
    name = StringField("name")
    address = StringField("address")
    password = StringField("password")

# with app.test_request_context():
#     form_ = StudentForm({"name": "Ani", "password": "ORange123"})
#     s = form_.validate()


msg = '''
        Password failed validation, must contain 1 special character, 1 lowercase letter,
        1 uppercase letter, 1 digit'''


def check_password(form, field, message):
    import string
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase
    digits = string.digits
    special_characters = string.punctuation
    password = field.data

    is_lowercase_present = False
    is_uppercase_present = False
    is_digit_present = False
    is_special_char_present = False

    for letter in password:
        if is_lowercase_present is False and letter in lowercase_letters:
            is_lowercase_present = True

        if is_uppercase_present is False and letter in uppercase_letters:
            is_uppercase_present = True

        if is_digit_present is False and letter in digits:
            is_digit_present = True

        if is_special_char_present is False and letter in special_characters:
            is_special_char_present = True

    value = is_lowercase_present and is_uppercase_present and is_digit_present and is_special_char_present
    if value:
        return value
    raise ValidationError(message)




class PasswordMatcher:
    def __init__(self, message):
        self.message = message

    def __call__(self, form, field):
        return check_password(form, field, self.message)

class LoginForm(FlaskForm):
    name = StringField(label="NAME")
    password = PasswordField(label="PASSWORD")
    confirm_password = PasswordField("CONFIRM_PASSWORD")

class LoginFormWithValidators(FlaskForm):
    name = StringField('NAME', validators=[InputRequired(message="No valid value provided for name variable")])

    password = PasswordField('PASSWORD', validators=[
        Length(min=8, message="Length of password should be at least 8"),
        PasswordMatcher(message=msg)
    ])

    confirm_password = PasswordField('CONFIRM_PASSWORD',
                                     validators=[EqualTo("password", message="The passwords do not match")])


class LoginFormSimple(FlaskForm):

    name = StringField("NAME")
    password = PasswordField("PASSWORD")
    birthday = DateField("BIRTHDAY")
    address = StringField("ADDRESS")
    email = EmailField("Email")

    confirm_password = PasswordField("CONFIRM_PASSWORD")

    from wtforms.meta import DefaultMeta

    # class Meta(DefaultMeta):
    #     csrf = False
    #
    #     placeholder_dict = {
    #         "NAME": "Enter your name here",
    #         "PASSWORD": "Enter your password here",
    #         "CONFIRM_PASSWORD": "Confirm Password"
    #     }
    #
    #     placeholder_dict2 = {
    #         "NAME": "Enter your name here",
    #         "PASSWORD": "Enter your password here",
    #         "CONFIRM_PASSWORD": "Confirm Password"
    #     }
    #
    #     def render_field(self, field, render_kw):
    #
    #         new_render_kw = render_kw.copy()
    #         new_render_kw["placeholder"] = self.placeholder_dict[field.label.text]
    #         return super().render_field(field, new_render_kw)



@app.route("/", methods=["GET", "POST"])
def handle():
    form = LoginFormSimple()
    msg = ''
    if request.method == "POST":
        if form.validate_on_submit():
            pass

    return render_template("form2.html", form=form, msg=msg)

# class MyFormClass:
#
#     field1 = StringField(label="field_label", validators=[ValidatorClass1(), ValidatorClass2()])

@app.route("/", methods=["GET", "POST"])
def handle_request():
    form = LoginForm()
    if request.method == "GET":
        return render_template("form_jinja_template.html", form=form)
    if request.method == "POST":
        print(form.data["name"])
        print(form.data["password"])
        print(form.data["confirm_password"])
        return redirect(url_for('handle_request'))

if __name__ == '__main__':
    app.run(port=9090)
