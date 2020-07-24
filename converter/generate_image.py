from flask import current_app, Blueprint, send_file, flash, redirect
from music21 import *
from zipfile import ZipFile
import os
bp = Blueprint("get_image", __name__)

#download result image
@bp.route('/get-image/')
def generate_image():
    try:
        zipObj = ZipFile(current_app.config['OUTPUT_ZIP'], 'w')
        a = converter.parse('musicxmlCache/ActorPreludeSample.musicxml').write('musicxml.png')
        
        if a[-6:] == '-1.png':
            b = a[:-6]
            for i in range(1,10):
                try:
                    zipObj.write(b+'-'+str(i)+'.png')
                except:
                    break
        elif a[-7:] == '-01.png':
            b = a[:-7]
            for i in range(1,10):
                try:
                    zipObj.write(b+'-0'+str(i)+'.png')
                except:
                    break
            for i in range(10,100):
                try:
                    zipObj.write(b+'-'+str(i)+'.png')
                except:
                    break                
        elif a[-8:] == '-001.png':
            b = a[:-8]
            for i in range(1,10):
                try:
                    zipObj.write(b+'-00'+str(i)+'.png')
                except:
                    break
            for i in range(10,100):
                try:
                    zipObj.write(b+'-0'+str(i)+'.png')
                except:
                    break 
            for i in range(100,1000):
                try:
                    zipObj.write(b+'-'+str(i)+'.png')
                except:
                    break
        else:
            zipObj.write(a)
        zipObj.close()
        return send_file(current_app.config['OUTPUT_ZIP'], 
            attachment_filename="result.zip" ,as_attachment=True, cache_timeout=0)
    except Exception as e:
        flash(str(e), 'danger')
        return redirect('/')
