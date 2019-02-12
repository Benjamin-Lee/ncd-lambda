from flask import Flask, request
from werkzeug.utils import secure_filename
import lzma

UPLOAD_FOLDER = '.'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files or not file.filename:
        return

    file = request.files['file']

    # compress and return the size
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        return str(len(lzma.compress(file.read())))


if __name__ == '__main__':
    app.run(debug=True)
