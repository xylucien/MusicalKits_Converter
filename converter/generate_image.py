import os
from flask import current_app, Blueprint, flash, send_file, redirect
from music21 import *
from zipfile import ZipFile

bp = Blueprint("get_image", __name__)

#download result image
@bp.route('/get-image/', methods=['GET', 'POST'])
def generate_image():
    try:
        #create zip file for download
        zipObj = ZipFile(current_app.config['OUTPUT_ZIP'], 'w')
        #get temp result images path
        result_image_path = converter.parse(current_app.config['PROCESS_FILE']).write('musicxml.png')
        
        #detect for multiple outputs
        #1 < image num < 10
        if '-1.png' in df:
            b = result_image_path[:-6]
            for i in range(1,10):
                try:
                    zipObj.write(b+'-'+str(i)+'.png')
                except:
                    break
        #10 < image num < 100
        elif '-01.png' in result_image_path:
            b = result_image_path[:-7]
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
        #100 < image num < 1000                
        elif '-001.png' in result_image_path:
            b = result_image_path[:-8]
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
        #only one image
        else:
            zipObj.write(result_image_path)
        zipObj.close()
        return send_file(current_app.config['OUTPUT_ZIP'], 
            attachment_filename="result.zip" ,as_attachment=True, cache_timeout=0)
    except Exception as e:
        flash(str(e), 'danger')
        return redirect('/')
