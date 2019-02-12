from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import lzma

UPLOAD_FOLDER = '.'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return '''
            <!doctype html>
            <title>Upload new File</title>
            <h1>Upload new File</h1>
            <form method=post enctype=multipart/form-data>
              <input type=file name=file>
              <input type=submit value=Upload>
            </form>
            '''

    file = request.files['file']

    # check if the post request has the file part
    if 'file' not in request.files or not file.filename:
        return

    # compress and return the size
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        return jsonify((filename, len(lzma.compress(file.read()))))


if __name__ == '__main__':
    app.run(debug=True)
