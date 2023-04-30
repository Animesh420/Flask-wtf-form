import os

from flask import Flask, request, render_template, url_for
from werkzeug.utils import redirect
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField
from wtforms.csrf.core import CSRFTokenField


class HeroForm(FlaskForm):
    name = StringField(label="Name")
    popularity_rating = IntegerField(label="Popularity Rating out of 100")
    whoami = TextAreaField(label="Who am I?")
    # csrf_token = CSRFTokenField('csrf_token') # HIDDEN !!


app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config["WTF_CSRF_ENABLED"] = False

from flask import Flask, request, render_template, url_for
app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def handle():
    form = HeroForm()
    if request.method == "GET":
        return render_template("form.html", form=form)
    if request.method == "POST":
        print(form.data["name"])
        print(form.data["power_rating"])
        print(form.data["whoami"])
        return redirect(url_for("handle"))


if __name__ == '__main__':
    app.run(port=9090)