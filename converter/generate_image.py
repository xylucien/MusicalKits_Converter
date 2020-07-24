from flask import current_app, Blueprint, send_file, flash, redirect
from music21 import *
bp = Blueprint("get_image", __name__)

#download result image
@bp.route('/get-image/')
def generate_image():
    try:
        return send_file(converter.parse('musicxmlCache/ActorPreludeSample.musicxml').write('musicxml.png'), 
            attachment_filename="result.png" ,as_attachment=True, cache_timeout=0)
    except Exception as e:
        flash(str(e), 'danger')
        return redirect('/')
