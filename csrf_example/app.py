from datetime import datetime
from flask import Flask, render_template, request
from flask_wtf import FlaskForm, csrf
from wtforms import StringField, PasswordField
import os
from wtforms.csrf.core import CSRFTokenField

from wtforms.csrf.core import CSRFTokenField

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
# prompt = "LOGIN_FAILED"


class LoginForm(FlaskForm):
    name = StringField('NAME')
    password = PasswordField('PASSWORD')
    # csrf_token = CSRFTokenField('csrf_token') HIDDEN !!


def handle_get_workflow(form):
    pass


def handle_post_workflow(form):
    pass

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/', methods=['GET', 'POST'])
def handle_form():
    form = LoginForm()
    if request.method == "GET":
        return render_template("csrf_template.html", form=form, msg="Hi there")
    if request.method == "POST":
        # ....
        if form.validate_on_submit():
            try:
                res = csrf.validate_csrf(data=form.data["csrf_token"],
                                  time_limit=form.meta.csrf_time_limit,
                                  secret_key=app.config.get("SECRET_KEY"),
                                  token_key="csrf_token")
            except Exception as e:
                return "Error"

            print("Valid Request CSRF matched")
        return render_template("csrf_template.html", form=form, msg="Hi there")


if __name__ == '__main__':
    app.run(port=8089, debug=True)
