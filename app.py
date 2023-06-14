import os
from flask import Flask, render_template, url_for, request, redirect, flash, send_from_directory
from werkzeug.utils import secure_filename

import functions
import textract


file_name = "text.txt"
would_name = "w.jpg"

app=Flask(__name__, static_folder='static')
UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'doc', 'docx'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def time_analy_find():
    return os.path.getsize(file_name)//(24*1024)

@app.route('/', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            text = textract.process(filename)
            if os.path.isfile(file_name):
                os.remove(file_name)
            if os.path.isfile('res.txt'):
                os.remove('res.txt')
            if os.path.isfile('static/pict/w.jpg'):
                os.remove('static/pict/w.jpg')
            f = open(file_name, "wb")
            f.write(text)
            f.close()
            os.remove(filename)
            return redirect(url_for('analysis'))
    return render_template('home.html')


@app.route('/analysis', methods=['GET','POST'])
def analysis():
    if request.method == 'POST':
        if 'dict' in request.form:
            functions.func(file_name)
            return redirect(url_for('choose_analyse'))
        elif 'word' in request.form:
            return redirect(url_for('choose_bigram'))
    return render_template('choose.html', time_analy = time_analy_find())

@app.route('/choose_analyse', methods=['GET','POST'])
def choose_analyse():
    if request.method == 'POST':
        return redirect(url_for('choose_analyse2'))
    return render_template('dict.html')

@app.route('/choose_analyse2', methods=['GET','POST'])
def choose_analyse2():
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(uploads, "res.txt")

@app.route('/choose_bigram', methods=['GET','POST'])
def choose_bigram():
    word = request.form['word']
    f = open(file_name, "r", encoding='utf-8')
    f2 = f.read()
    res_file_bi = open("bi.txt", "w+", encoding='utf-8')
    functions.bigram(f2,word, res_file_bi)
    res_file_bi.close()
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(uploads, "bi.txt")

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)