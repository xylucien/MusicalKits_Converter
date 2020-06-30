from flask import current_app, Blueprint, send_file, flash, redirect
bp = Blueprint("return_files", __name__)

#download result file
@bp.route('/return-files/')
def return_files_tut():
    try:
        return send_file(current_app.config['OUTPUT_FILE'], attachment_filename="result.abc" ,as_attachment=True)
    except Exception as e:
        flash(str(e), 'danger')
        return redirect('/')