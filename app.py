from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from subprocess import Popen, PIPE
import os, io
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '///musicxmlCache'
ALLOWED_EXTENSIONS = {'musicxml'}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDataBase.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)
output_file = 'result.abc'
input_file = 'temp.musicxml'

class Convert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.TEXT, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

#only accepting limited file formats
#format whitelist is in ALLOWED_EXTENSIONS
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        converted_text = ''
        
        #get user input and write into a file
        task_content = request.form['content']
        with io.open("temp.musicxml", "w+", encoding='utf-8') as temp_inputfile:
            temp_inputfile.write(task_content)
        
        #execute the converter script and listen for result
        process = Popen(['./xml2abc.py', 'temp.musicxml'], stdout=PIPE, stderr = PIPE, encoding='utf-8')
        stdout, stderr = process.communicate()
        result = stdout
        
        #display error message
        if(process.returncode!=0): 
            result = stderr + '\n' + "There is something wrong with your input. Please check again!\n"
        #write result text into a file for future access
        else: 
            with io.open(output_file, "r+", encoding='utf-8') as temp_outputfile:
                converted_text = temp_outputfile.read()
        
        #put result in a new Convert instance
        new_task = Convert(content= result + converted_text) 
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue appending the result!!'
        try:
            os.remove(input_file)
            os.remove(output_file)
        except OSError as error: 
            print(error + 'n' + "File path can not be removed") 

    else:
        tasks = Convert.query.order_by(Convert.date_created).all()
        return render_template('index.html', tasks=tasks)

def upload_file(): 
    #still in development
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('upload.html')

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Convert.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that fact!'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Convert.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your fact!'

    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)