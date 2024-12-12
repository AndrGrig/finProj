from flask import Blueprint, render_template, request, redirect, url_for, flash
from .s3_utils import list_photos, upload_to_s3
from .db import add_photo_record

main = Blueprint('main', __name__)

@main.route('/')
def index():
    photos = list_photos()
    return render_template('index.html', photos=photos)

@main.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        upload_to_s3(file)
        add_photo_record(file.filename)
        flash(f"Photo '{file.filename}' uploaded successfully!", 'success')
    else:
        flash("No file selected!", 'danger')
    return redirect(url_for('main.index'))