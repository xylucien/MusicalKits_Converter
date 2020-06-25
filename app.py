from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect, flash, send_file, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from subprocess import Popen, PIPE
from werkzeug.utils import secure_filename
import io, os, sys, tempfile

UPLOAD_FOLDER = os.path.join(os.getcwd(),'musicxmlCache')
ALLOWED_EXTENSIONS = {'musicxml'}

#initialize app and create session (flash function is disabled without a secret key)
app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDataBase.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)
output_file = 'result.abc'

class Convert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.TEXT, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    is_file = db.Column(db.Integer, default=0)
    def __repr__(self):
        return '<Task %r>' % self.id

#only accepting limited file formats
#format whitelist is in ALLOWED_EXTENSIONS
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#helper function
def generate_result(result, converted_text):
    #put result in a new Convert instance
    if not converted_text:
        result = "There is something wrong with your input. Please check again!\n"
    return Convert(content= result + converted_text) 

@app.route('/', methods=['POST', 'GET'])
def index():
    tasks = Convert.query.order_by(Convert.date_created).all()
    return render_template('index.html', tasks=tasks)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file(): 
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file found!')
            return redirect('/')
        
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if not file.filename:
            flash('No selected file!')
            return redirect('/')

        #if upload is valid
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_task = Convert(content = filename, is_file = 1)
            db.session.add(new_task)
            db.session.commit()

            # prompt that upload is successful
            # may add more features in this page later
            return render_template("upload.html")
    return redirect('/')

@app.route('/submission', methods=['GET', "POST"])
def submit_text():
    if request.method == 'POST':
        task_content = request.form['content']
        if not task_content:
            flash('You cannot submit empty text!')
            return redirect('/')

        new_task = Convert(content = task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return render_template('submission.html')
        except:
            flash('There was an issue appending the result!!')
    return redirect('/')    

#saved for future re-designing this functionality
'''
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Convert.query.get_or_404(id)

    try:
        if task_to_delete.is_file != 0:
            try:
                os.remove(os.path.join(UPLOAD_FOLDER,task_to_delete.content))
            except NameError as error: 
                flash(str(error) + 'n' + "File cannot be removed") 
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        flash('There was a problem deleting that task!' + str(e))
        return redirect('/')
'''

@app.route('/convert_result/<int:id>', methods=['GET', 'POST'])
def to_convert(id):
    task = Convert.query.get_or_404(id)
    converted_text = ''

    #if user copy-pasted
    if task.is_file == 0:
        #get user input and write into a temp file
        temp_inputfile = tempfile.NamedTemporaryFile(mode='w+', encoding='utf-8', delete=True, suffix='.musicxml')
        temp_inputfile.write(task.content)
        target_path = temp_inputfile.name
    #if user uploaded a file
    else:
        target_path = os.path.join(UPLOAD_FOLDER, task.content)
    
    #execute the converter script and listen for result
    process = Popen(['python3', 'xml2abc.py', target_path], stdout=PIPE, stderr = PIPE, encoding='utf-8')
    stdout, stderr = process.communicate()
    
    result = stdout

    #display error message
    if(process.returncode!=0 or not result): 
        result = stderr + '\n' + "There is something wrong with your input. Please check again!\n"
    #write result text into a file for future access
    else: 
        with io.open(output_file, "r+", encoding='utf-8') as temp_outputfile:
            converted_text = temp_outputfile.read()
    
    #temp file automatically deleted on close()
    if task.is_file == 0: temp_inputfile.close()

    if request.method == 'POST':
        return redirect('/')

    else:
        return render_template('convert_result.html', task=generate_result(result, converted_text))

@app.route('/return-files/')
def return_files_tut():
    try:
        return send_file(output_file, attachment_filename="result.abc" ,as_attachment=True)
    except Exception as e:
        flash(str(e))
        return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, threaded=True)