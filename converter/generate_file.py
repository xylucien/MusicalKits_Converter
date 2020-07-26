from flask import current_app, Blueprint, flash, send_file, redirect
from music21 import *
from subprocess import Popen, PIPE

bp = Blueprint("get_file", __name__)

#suffic dict
suffix_dict = {
    'musicxml': '.musicxml',
    'abc': '.abc',
    'vexflow': '.html',
    'lilypond': 'ly',
    'braille': '.txt',
    'scala': '.scl'
}

#download result file
@bp.route('/get-file/<file_format>', methods = ['GET', 'POST'])
def download_result(file_format):
    #use xml2abc.py to process abc output
    if file_format == 'abc':
        #execute the converter script and listen for result
        process = Popen(['converter/xml2abc.py', current_app.config['PROCESS_FILE']], 
            stdout=PIPE, stderr = PIPE, encoding='utf-8')
        
        #listen for success message
        stdout, stderr = process.communicate()
        result = stdout

        #load error message
        if(process.returncode!=0 or not result): 
            flash("There is something wrong with your input. Please check again!", 'danger')
            return redirect('/')
        #read result from the file generated from script
        else: 
            try:
                return send_file(current_app.config['OUTPUT_ABC_FILE'], 
                    attachment_filename="result.abc" ,as_attachment=True, cache_timeout=0)
            except Exception as e:
                flash(str(e), 'danger')
                return redirect('/')
    #process other formats using music21
    else:
        try:
            return send_file(converter.parse(current_app.config['PROCESS_FILE']).write(file_format), 
                attachment_filename="result"+suffix_dict[file_format] ,as_attachment=True, cache_timeout=0)
        except Exception as e:
            flash(str(e), 'danger')
            return redirect('/')