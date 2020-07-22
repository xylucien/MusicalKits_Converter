from flask import Flask
from flask import Blueprint, current_app, json, render_template, request
from subprocess import Popen, PIPE
from werkzeug.utils import secure_filename

import io, os, sys, tempfile

bp = Blueprint("convert", __name__)

@bp.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

class Convert:
    def __init__(self, content, is_file = False):
        self.is_file = is_file
        self.content = content

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
def handleTempInput(text_to_write):
    temp_inputfile = tempfile.NamedTemporaryFile(mode='w+', 
        encoding='utf-8', delete=True, suffix='.musicxml')
    temp_inputfile.write(text_to_write)
    return temp_inputfile

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
        return 'File extention name not valid!'

def submit_text():
    task_content = request.form['text']
    #check for empty submission
    if not task_content:
        return 'You cannot submit empty text!'
    # prompt that submission is successful
    return Convert(task_content, False)

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
    is_success = False
    #if user copy-pasted
    if not task.is_file:
        temp_inputfile = handleTempInput(task.content)
        target_path = temp_inputfile.name
    #if user uploaded a file
    else:
        target_path = os.path.join(current_app.config['UPLOAD_FOLDER'], task.content)
    
    #execute the converter script and listen for result
    process = Popen(['converter/xml2abc.py', target_path], 
        stdout=PIPE, stderr = PIPE, encoding='utf-8')
    
    #listen for success message
    stdout, stderr = process.communicate()
    result = stdout

    #load error message
    if(process.returncode!=0 or not result): 
        result = "There is something wrong with your input. Please check again!"
    #read result from the file generated from script
    else: 
        with io.open(current_app.config['OUTPUT_FILE'], "r+", encoding='utf-8') as temp_outputfile:
            converted_text = temp_outputfile.read()
            is_success = True
    
    #temp file automatically deleted on close()
    if task.is_file == 0: temp_inputfile.close()

    return json.dumps({
        'is_success':is_success,
        'message':result,
        'result':converted_text})
