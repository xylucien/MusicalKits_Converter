from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect, flash, send_file, send_from_directory, Markup

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, IntegerField, TextField,\
    FormField, SelectField, FieldList
from wtforms.validators import DataRequired, Length
from wtforms.fields import *

from flask_bootstrap import Bootstrap

from flask_sqlalchemy import SQLAlchemy
from subprocess import Popen, PIPE
from werkzeug.utils import secure_filename

import io, os, sys, tempfile

UPLOAD_FOLDER = os.path.join(os.getcwd(),'musicxmlCache')
ALLOWED_EXTENSIONS = {'musicxml'}
try:
    os.makedirs('musicxmlCache')
except OSError:
    pass

#initialize app and create session (flash function is disabled without a secret key)
app = Flask(__name__)
app.secret_key = os.urandom(24)

bootstrap = Bootstrap(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

output_file = 'result.abc'

class Convert:
    def __init__(self, content, is_file = False):
        self.is_file = is_file
        self.content = content

class ButtonForm(FlaskForm):
    Download = SubmitField()
    Return = SubmitField()

#only accepting limited file formats
#format whitelist is in ALLOWED_EXTENSIONS
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#helper functions

#put result in a new Convert instance
def generate_result(result, converted_text):
    if not converted_text:
        result = "There is something wrong with your input. Please check again!\n"
    flash(result, 'info')
    return Convert(content=converted_text) 

#secure file name and save to data folder
def handleFileSave(raw_file):
    filename = secure_filename(raw_file.filename)
    raw_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return filename

#get user input and write into a temp file
def handleTempInput(text_to_write):
    temp_inputfile = tempfile.NamedTemporaryFile(mode='w+', 
        encoding='utf-8', delete=True, suffix='.musicxml')
    temp_inputfile.write(text_to_write)
    return temp_inputfile

#thinking about how to implement
def handleTempOutput():
    pass

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

def upload_file(): 
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file found!', 'danger')
        return "bruh"
    
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if not file.filename:
        flash('No selected file!', 'danger')
        return "bruh"

    #if upload is valid
    if file and allowed_file(file.filename):
        filename = handleFileSave(file)

        # prompt that upload is successful
        return Convert(file.filename, True)
    else:
        flash('File extention name not valid!', 'danger')
        return "bruh"

def submit_text():
    task_content = request.form['content']

    #check for empty submission
    if not task_content:
        flash('You cannot submit empty text!', 'warning')
        return "bruh"

    # prompt that submission is successful
    return Convert(task_content, False)

@app.route('/convert_result/<is_file>', methods=['GET', 'POST'])
def to_convert(is_file):
    if is_file == "submission":
        task = submit_text()
    else:
        task = upload_file()
    
    #check if returns error message
    if(task=="bruh"): return redirect('/')
    converted_text = ''

    #if user copy-pasted
    if not task.is_file:
        temp_inputfile = handleTempInput(task.content)
        target_path = temp_inputfile.name
    #if user uploaded a file
    else:
        target_path = os.path.join(UPLOAD_FOLDER, task.content)
    
    #execute the converter script and listen for result
    process = Popen(['python3', 'xml2abc.py', target_path], 
        stdout=PIPE, stderr = PIPE, encoding='utf-8')
    
    #listen for success message
    stdout, stderr = process.communicate()
    result = stdout

    #display error message
    if(process.returncode!=0 or not result): 
        result = stderr + '\n' + "There is something wrong with your input. Please check again!"
    #write result text into a file for future access
    else: 
        with io.open(output_file, "r+", encoding='utf-8') as temp_outputfile:
            converted_text = temp_outputfile.read()
    
    #temp file automatically deleted on close()
    if task.is_file == 0: temp_inputfile.close()

    return render_template('convert_result.html', 
        task=generate_result(result, converted_text), button_form = ButtonForm())

#download result file
@app.route('/return-files/')
def return_files_tut():
    try:
        return send_file(output_file, attachment_filename="result.abc" ,as_attachment=True)
    except Exception as e:
        flash(str(e), 'danger')
        return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, threaded=True)