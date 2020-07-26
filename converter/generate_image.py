import os
from flask import current_app, Blueprint, flash, send_file, redirect
from music21 import *
from zipfile import ZipFile

bp = Blueprint("get_image", __name__)

# determine range of the number of images
# 0 if only one file
# 1 if 1 < image num < 10
# 2 if 10 < image num < 100
# 3 if 100 < image num < 1000    
def get_range_and_prefix(result_image_path):
    if '-1.png' in result_image_path:
        return 1, result_image_path[:-6]
    elif '-01.png' in result_image_path:
        return 2, result_image_path[:-7]
    elif '-001.png' in result_image_path:
        return 3, result_image_path[:-8]
    else:
        return 0, result_image_path[:-4]

# return calculated suffic name for images    
def calc_suffix(image_range, cur_num):
    if image_range == 1:
        return '-'+str(cur_num)
    if image_range == 2:
        if cur_num < 10:
            return '-0'+str(cur_num)
        else:
            return '-'+str(cur_num)
    if image_range == 3:
        if cur_num < 10:
            return '-00'+str(cur_num)
        elif cur_num < 100:
            return '-0'+str(cur_num)            
        else:
            return '-'+str(cur_num)

# download result image
@bp.route('/get-image/', methods=['GET', 'POST'])
def generate_image():
    try:
        # create zip file for download
        zipObj = ZipFile(current_app.config['OUTPUT_ZIP'], 'w')
        # get temp result images path
        result_image_path = converter.parse(current_app.config['PROCESS_FILE']).write('musicxml.png')
        
        image_range, image_temp_prefix = get_range_and_prefix(result_image_path)
        max_image_number = 999

        # only one image
        if image_range == 0:
            zipObj.write(result_image_path)
        else:
            for i in range(1,max_image_number+1):
                image_suffix = calc_suffix(image_range, i)
                image_name = image_temp_prefix + image_suffix + ".png"           
                try:
                    zipObj.write(image_name)
                except:
                    break
        zipObj.close()
        return send_file(current_app.config['OUTPUT_ZIP'], 
            attachment_filename="result.zip" ,as_attachment=True, cache_timeout=0)
    except Exception as e:
        flash(str(e), 'danger')
        return redirect('/')
