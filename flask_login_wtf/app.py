from datetime import datetime
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
import os

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
prompt = "LOGIN_FAILED"


class LoginForm(FlaskForm):
    name = StringField('NAME')
    password = PasswordField('PASSWORD')
    catch_phrase = StringField("CATCH_PHRASE")


local_db = dict()


def fetch_form_details(form):
    name = form.data["name"]
    password = form.data["password"]
    catch_phrase = form.data["catch_phrase"]
    return name, password, catch_phrase


def handle_get_workflow(form):
    return render_template('signup_in_form.html', form=form, msg="Please enter your login details")


def handle_post_workflow(form):
    if form.validate_on_submit():
        name, password, catch_phrase = fetch_form_details(form)
        msg, time_past, success = "", "", False
        if len(password) < 5:
            msg = "[{}] Password length should at least be 5".format(prompt)

        elif name not in local_db:
            time_past = datetime.now().isoformat()
            local_db[name] = (password, catch_phrase, time_past)
            success = True
        else:
            password_, catch_phrase_, time_past = local_db[name]
            if password_ != password:
                msg = "[{}] {} password doesnt match, try again".format(prompt, name)
            elif catch_phrase_ != catch_phrase:
                new_catch_phrase = [catch_phrase_[i] if i % 2 == 0 else '_' for i in range(len(catch_phrase_))]
                new_catch_phrase = ''.join(new_catch_phrase)
                msg = "[{}] Wrong catch phrase, hint => {}".format(prompt, new_catch_phrase)
            else:
                success = True
        if success:
            return render_template("success.html", user=name, log_time=time_past)
        else:
            return render_template("signup_in_form.html", form=form, msg=msg)


@app.route('/', methods=['GET', 'POST'])
def handle_form():
    form = LoginForm()
    if request.method == "GET":
        return handle_get_workflow(form)
    else:
        return handle_post_workflow(form)


if __name__ == '__main__':
    app.run(port=8089, debug=True)
