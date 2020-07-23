from flask import current_app, Blueprint, send_file, flash, redirect
from music21 import *
bp = Blueprint("get_image", __name__)

#download result image
@bp.route('/get-image/')
def generate_image():
    try:
        converter.parse('result.abc').write('lilypond.png', 'result')
        return send_file(current_app.config['OUTPUT_IMG'], 
            attachment_filename="result.png" ,as_attachment=True, cache_timeout=0)
    except Exception as e:
        flash(str(e), 'danger')
        return redirect('/')
