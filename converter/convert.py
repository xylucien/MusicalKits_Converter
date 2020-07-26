from flask import Flask
from flask import Blueprint, current_app, g, json, render_template, request
from music21 import *
from werkzeug.utils import secure_filename

import io, os, sys, tempfile

bp = Blueprint("convert", __name__)

@bp.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

class Convert:
    def __init__(self, content, is_file = False, formats = ''):
        self.is_file = is_file
        self.content = content
        self.formats = formats

#helper functions

#only accepting limited file formats
#format whitelist is in ALLOWED_EXTENSIONS
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

#put result in a new Convert instance
def generate_result(result, converted_text):
    if not converted_text:
        result = "There is something wrong with your input. Please check again!\n"
        converted_text = "INVALID"
    return Convert(content=converted_text) 

#secure file name and save to data folder
def handleFileSave(raw_file):
    filename = secure_filename(raw_file.filename)
    raw_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    return filename

#get user input and write into a temp file
def handleTextInput(text_to_write, save_format):
    inputfile = io.open( os.path.join (current_app.config['UPLOAD_FOLDER'], 'user_upload' + save_format), 
        'w', encoding='utf-8')
    #tempfile.NamedTemporaryFile(mode='w+', 
    #    encoding='utf-8', delete=True, suffix='.musicxml')
    inputfile.write(text_to_write)
    return inputfile

def upload_file(): 
    # check if the post request has the file part
    if 'file' not in request.files:
        return 'No file found!'
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if not file.filename:
        return 'No selected file!'

    #if upload is valid
    if file and allowed_file(file.filename):
        filename = handleFileSave(file)
        # prompt that upload is successful
        return Convert(filename, True)
    else:
        return 'File extension name not valid!'

def submit_text():
    task_content = request.form['text']
    file_format = request.form['format']
    #check for empty submission
    if not task_content:
        return 'You cannot submit empty text!'
    # prompt that submission is successful
    return Convert(task_content, False, file_format)

@bp.route('/convert_result/<is_file>', methods=['GET', 'POST'])
def to_convert(is_file):
    if is_file == "submission":
        task = submit_text()
    else:
        task = upload_file()

    #check if returns error message
    if not isinstance(task,Convert):
        return json.dumps({'is_success': False, 'message':task, 'result':''})
    converted_text = ''
    #if user copy-pasted
    if not task.is_file:
        temp_inputfile = handleTextInput(task.content, task.formats)
        target_path = temp_inputfile.name
    #if user uploaded a file
    else:
        target_path = os.path.join(current_app.config['UPLOAD_FOLDER'], task.content)
    
    #load file to Music21.Score
    try:
        score = converter.parse(target_path)
        score.write('musicxml', current_app.config['PROCESS_FILE'])
    #return error message immediately if the file is corrupted/not valid
    except:
        message = 'There is something wrong with your input. Please check again!'
        return json.dumps({'is_success': False, 'message':message, 'result':''})

    return json.dumps({
        'is_success': True,
        'message':"Conversion successful!",
        'result':"Upload sucess! Choose ur option"})
