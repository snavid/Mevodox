from flask import Blueprint, render_template, flash, request, redirect, url_for, send_file, Response 
from flask_login import login_required, login_user, current_user
from .models import User, Note
from websites import db
from datetime import datetime
import json
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet
import random
import os




views = Blueprint("views", __name__)

@views.route('/home', methods=['POST', 'GET'])
@login_required
def homepage():
    notice = bool(current_user.notes)
    print(notice)
    return render_template('homepage.html', user=current_user, notice=notice)


@views.route('/review_notes')
@login_required
def rev():
    notice = bool(current_user.notes)
    return render_template('review.html',user=current_user, notice=notice,)


@views.route('/add_notes', methods=['POST', 'GET'])
@login_required
def add_memo():
    if request.method == 'POST':
        title = request.form.get('title')
        memo = request.form.get('memo')
        file = request.files['image1']
        note = Note(data=memo, title=title,filename=file.filename, user_id=current_user.id)
        file.save('main/websites/statics/images/' + file.filename) 
        db.session.add(note)
        db.session.commit()
        flash('Your memo was successfully stored', category='info')
        return redirect(url_for("views.rev"))
    return render_template('test.html',user=current_user)


@views.route('/download_pdf/<note_id>', methods=['GET'])
@login_required
def download_pdf(note_id):
    # Create a PDF file using reportlab
    file = random.randint(10000, 99999)
    pdf_file = f'{file}.pdf'  # Specify the name of the output PDF file
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)

    # Define styles for the title and text
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    title_style.leading = 40
    title_style.fontSize = 25
    date_style = styles['Title']
    date_style.fontSize = 20
    date_style.textColor = 'blue'
    
    doc_style = styles['Normal']
    doc_style.FontSize = 8
    doc_style.textColor = 'red'
    
    text_style = styles['Normal']
    text_style.fontSize = 15
    text_style.firstLineIndent = 15
    text_style.textColor = 'black'
    text_style.fontName = 'Helvetica'
    text_style.leading = 20

    # Create a list to hold the flowables (elements) for the PDF content
    flowables = []

    # Retrieve the note with the specified note_id
    note = Note.query.get(note_id)
    if note:
        title = str(note.title)
        text = str(note.data)
        parr = "Mevodox (made by Yunus Siraju Contact:0786392008) Enjoy your memories with no limit.                                             "                                                          
        date = str(note.date)
        title = title.upper()
        image_file = 'main/websites/statics/images/' + note.filename

        # Add the title to the flowables list
        title_paragraph = Paragraph(title, title_style)
        flowables.append(title_paragraph)
        date_paragraph = Paragraph(date, date_style)
        flowables.append(date_paragraph)

        # Add the image to the flowables list
        flowables.append(Image(image_file, width=400, height=300))
        space_paragraph = Paragraph(parr, doc_style)
        flowables.append(space_paragraph)

        # Add the text to the flowables list
        text_paragraph = Paragraph(text, text_style)
        flowables.append(text_paragraph)

        # Build the PDF document with the flowables
        doc.build(flowables)
        path = f'D:/current/{pdf_file}'
        return send_file(path, download_name=f"{note.title}.pdf", as_attachment=True)
    else:
        return "Note Not Found!"


@views.route('/edit/<note_id>', methods=['GET'])
@login_required
def edit(note_id):
    note = Note.query.get(note_id)
    print(url_for("static", filename='male.png'))
    flash(f'{current_user.username} select any field to begin editing your mevedox', category="info")
    return render_template('edit.html', user=current_user, note_data=note.data, note_title=note.title, note_id=note_id)


@views.route('/mevodox_editor/<user_id>', methods=['POST', 'GET'])
@login_required
def editor(user_id):
    if request.method == 'POST':
        content1 = request.form.get('content1')
        content2 = request.form.get('content2')
        # Perform further actions with the submitted content
        update = Note.query.get(user_id)
        print(update.title)
        update.title = content1
        update.data = content2
        db.session.commit()
        flash("You have successfully edited your mevodox", category='info')
    return redirect(url_for('views.rev'))


@views.route('/delete_note', methods=['POST'])
@login_required
def delete_note():
    note = json.loads(request.data)
    noteId = note['note_id']
    dot = Note.query.get(noteId)
    
    def delete_pdf_files(directory_path):
        try:
            # List all files in the directory
            files = os.listdir(directory_path)
            # Iterate through the files and delete PDF files
            for file in files:
                if file == dot.filename:
                    file_path = os.path.join(directory_path, file)
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
            print("Deletion of PDF files completed.")
        except Exception as e:
            print(f"Error occurred: {e}")
    directory_path = "D:\current\main\websites\statics\images"
    delete_pdf_files(directory_path)
    db.session.delete(dot)
    db.session.commit()
    flash(f'Memo with title {dot.title} was deleted', category='info')
    return 'Every thing is done'
    
    
@views.route('/admin')
@login_required
def admin():
    if current_user.username == 'admin':
        users = User.query.all()
        notice = bool(users)
        len = User.query.count()
        return render_template('admin.html', users=users, notice=notice, len = len)
    return redirect(url_for('views.homepage'))

@views.route('/bridge/<username>')
@login_required
def bridge(username):
    user = User.query.filter_by(username=username).first()
    login_user(user, remember=True)
    return redirect(url_for('views.homepage'))



@views.route('/delete_pdf')
def delete_pdf():
    def delete_pdf_files(directory_path):
        try:
            # List all files in the directory
            files = os.listdir(directory_path)
            # Iterate through the files and delete PDF files
            for file in files:
                if file.endswith(".pdf"):
                    file_path = os.path.join(directory_path, file)
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
            print("Deletion of PDF files completed.")
        except Exception as e:
            print(f"Error occurred: {e}")
    directory_path = "D:/current"
    delete_pdf_files(directory_path)
    return redirect(url_for('views.admin'))


@views.route('/practice')
def particle():
    return render_template('practice.html')


@views.route('/api')
def api_parser():
    data = { "name": "YUNUS",
             "AGE" : 19,
             "date" : datetime.now().date()
            }
    return data