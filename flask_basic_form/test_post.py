from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateTimeField
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False


class MyLoginForm(FlaskForm):
    name = StringField("name")
    password = PasswordField("password")
    address = StringField("address")
    birthday = StringField("birthday")

@app.route('/post_form_data', methods=['GET', 'POST'])
def handle_form():
    form = MyLoginForm()
    username, password = None, None
    address, birthday = None, None

    if request.method == 'GET':
        pass
    if request.method == 'POST':
        if form.validate_on_submit():
            pass
            username = form.data["name"]
            password = form.data["password"]
            address = form.data["address"]
            birthday = form.data["birthday"]

    return jsonify(
        name=username,
        password=password,
        address=address,
        birthday=birthday
    )

TESTNAME = "Joe"
TESTPASSWORD = "Pwd"
TESTADDRESS = "Addr"
TESTBIRTHDAY = "2020-10-10"




errors = []
with app.test_client() as c:
    with app.test_request_context():
        form = MyLoginForm()

    data = {
        "name": TESTNAME,
        "password": TESTPASSWORD,
        "address": TESTADDRESS,
        "birthday": TESTBIRTHDAY
    }
    response = c.post(
        '/post_form_data', data=data, follow_redirects=True)
    import json

    valid_data = json.loads(response.data.decode())
    names = ["name", "password", "address", "birthday"]
    values = [TESTNAME, TESTPASSWORD, TESTADDRESS, TESTBIRTHDAY]
    for n, v in zip(names, values):
        if valid_data.get(n) != v:
            errors.append(f"Validation failed for field {n}, mismatch !! {{ {v} != {valid_data.get(n)} }}")

if errors:
    error_msg = "\n".join(errors)
    print(error_msg)
else:
    print("correct")
