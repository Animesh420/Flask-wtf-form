from datetime import datetime
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateTimeField, EmailField
import os

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
prompt = "LOGIN_FAILED"


class BasicLoginForm(FlaskForm):
    name = StringField('NAME')
    password = PasswordField('PASSWORD')

class LoginForm(FlaskForm):
    name = StringField("NAME")
    password = PasswordField("PASSWORD")
    address = StringField("ADDRESS")
    dob = DateTimeField("BIRTHDAY")
    email = EmailField("EMAIL")

local_db = dict()


@app.route('/', methods=['GET', 'POST'])
def handle_form():
    form = BasicLoginForm()
    if request.method == 'GET':
        return render_template('signup_in_form.html', form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.data["name"]
            password = form.data["password"]
            print(username, password)

        return render_template('signup_in_form.html', form=form)

@app.route('/abc', methods=['GET', 'POST'])
def handle_form2():
    ...
    form = BasicLoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            success_template_name = 'success_template.html'
            failure_template_name = 'failure_template.html'
            username, password = form.data["name"], form.data["password"]
            if not_valid_password(password):
                return render_template(failure_template_name, form=form, msg="Failed")
            if is_user_in_db(username):
                if is_password_same_as_before(password):
                    return render_template(success_template_name, form=form, msg="Success")
                else:
                    return render_template(failure_template_name, form=form, msg="Failed")
            else:
                return render_template(success_template_name, form=form, msg="Success")




            if name not in local_db:
                local_db[name] = password
                msg = "User {} ==> Last login time {}".format(name, datetime.now().isoformat())
            else:
                if local_db[name] != password:
                    msg = "User {} has logged in before with a different password".format(name)
                else:
                    msg = "User {} ==> Last login time {}".format(name, datetime.now().isoformat())

            return render_template("signup_in_form.html", form=form, msg=msg)


if __name__ == '__main__':
    app.run(port=8089, debug=True)
