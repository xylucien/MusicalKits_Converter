from flask import current_app, Blueprint, send_file, flash, redirect
from music21 import *
bp = Blueprint("get_sound", __name__)

#download result sound
@bp.route('/get-sound/')
def generate_sound():
    try:
        return send_file(converter.parse('result.abc').write('midi'), 
            attachment_filename="result.mid" ,as_attachment=True, cache_timeout=0)
    except Exception as e:
        flash(str(e), 'danger')
        return redirect('/')