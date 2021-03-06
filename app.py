from posixpath import split
from flask import Flask, render_template, flash, request, redirect, url_for, send_file

import os
from os import path

from werkzeug.utils import secure_filename
from markupsafe import escape

from pdf_manager import split_pdf_get_images

UPLOAD_FOLDER = 'raw_pdf'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = 'super secret'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash('Not a PDF')
            return redirect(request.url)

        # Get page numbers
        form_data = request.form

        start_page = int(form_data['start_page'])
        end_page = int(form_data['end_page'])
    
      

        if start_page > end_page and end_page != -1:
            flash('End page must be greater than start page')
            return redirect(request.url)

        # print(start_page, end_page)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filename_nodot = filename.split(".pdf")[0]
           # print(filename)
            final_name = split_pdf_get_images(filename_nodot, start_page, end_page) + ".pdf"
            # if no file named final_name ... then flash error and redirect
            if not path.isfile(f"pdf\{filename_nodot}_extracted.pdf"):
                flash("Error, cannot extract figures from file")
                return redirect(request.url)
            #pdf\bio_extracted.pdf
            return redirect('/downloadfile/'+ final_name)
            #return redirect('/downloadfile/extracted.pdf')
             #url_for('static', filename='css/main.css')

    # GET: return index.html         
    return render_template("index.html")



@app.route("/downloadfile/<filename>", methods = ['GET'])
def download_file(filename):
    return render_template('download.html',value=filename)

@app.route('/return-files/<filename>')
def return_files_tut(filename):
    file_path = "pdf" + "\\" + filename
    
    return send_file(file_path, as_attachment=True, attachment_filename='')


if __name__ == '__main__':
    app.run()


