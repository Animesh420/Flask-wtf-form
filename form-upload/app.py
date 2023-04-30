from flask import render_template, Flask
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


from flask_wtf import FlaskForm
from flask_wtf.file import FileField

class FileUploadForm(FlaskForm):
    file = FileField()


@app.route('/', methods=['GET', 'POST'])
def upload():
    form = FileUploadForm()

    if form.validate_on_submit():
        f = form.data["file"]
        filename = secure_filename(f.filename)
        f.save(os.path.join(
            app.instance_path, 'uploaded', filename
        ))
        return render_template('success.html', fname=filename)

    return render_template('form-upload.html', form=form)

if __name__ == '__main__':
    app.run(port=8089, debug=True)
