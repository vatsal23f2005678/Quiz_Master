from flask import Blueprint, redirect, url_for, session, render_template, request, flash
from models.user import db, User
from models.quiz import Chapter, Subject, Question

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def admin_dashboard():
    if not session.get("admin"):
        return redirect(url_for('main.login'))
    subjects = Subject.query.all()
    return render_template('admin/dashboard.html', subjects=subjects)

@admin_bp.route('/subjects')
def manage_subjects():
    if not session.get("admin"):
        return redirect(url_for('main.login'))
    subjects=Subject.query.all()
    return render_template('admin/subjects.html',subjects=subjects)

@admin_bp.route('/subjects/add', methods=['POST'])
def add_subject():
    if not session.get("admin"):
        return redirect(url_for('main.login'))
    name = request.form.get("name")
    if name:
        new_subject = Subject(name=name)
        db.session.add(new_subject)
        db.session.commit()
        flash("Subject added!", "success")
    return redirect(url_for('admin.manage_subjects'))

@admin_bp.route('/subjects/edit/<int:subject_id>', methods=['POST'])
def edit_subject(subject_id):
    if not session.get("admin"):
        return redirect(url_for('main.login'))
    subject = Subject.query.get(subject_id)
    if subject:
        subject.name = request.form.get("name")
        db.session.commit()
        flash("Subject updated successfully!", "success")
    return redirect(url_for('admin.manage_subjects'))

@admin_bp.route('/subjects/delete/<int:subject_id>', methods=['POST'])
def delete_subject(subject_id):
    if not session.get("admin"):
        return redirect(url_for('main.login'))
    subject = Subject.query.get(subject_id)
    if subject:
        db.session.delete(subject)
        db.session.commit()
        flash("Subject deleted successfully!", "success")
    return redirect(url_for('admin.manage_subjects'))

@admin_bp.route('/chapters/add', methods=['GET', 'POST'])
def add_chapter():
    subjects = Subject.query.all()
    if request.method == 'POST':
        name = request.form.get('name')
        subject_id = request.form.get('subject_id')
        if name and subject_id:
            chapter = Chapter(name=name, subject_id=subject_id)
            db.session.add(chapter)
            db.session.commit()
            flash("Chapter added!")
            return redirect(url_for('admin.admin_dashboard'))
    return render_template('admin/add_chapter.html', subjects=subjects)

@admin_bp.route('/questions/add', methods=['GET', 'POST'])
def add_question():
    if not session.get("admin"):
        return redirect(url_for('main.login'))  # Restrict to admins
    
    chapters = Chapter.query.all()
    if request.method == 'POST':
        chapter_id = request.form.get('chapter_id')
        question_text = request.form.get('question_text')
        option_a = request.form.get('option_a')
        option_b = request.form.get('option_b')
        option_c = request.form.get('option_c')
        option_d = request.form.get('option_d')
        correct_option = request.form.get('correct_option')  
        
        if chapter_id and question_text and option_a and option_b and option_c and option_d and correct_option:
            question = Question(
                chapter_id=chapter_id,
                question_text=question_text,
                a=option_a,
                b=option_b,
                c=option_c,
                d=option_d,
                correct_option=correct_option
            )
            db.session.add(question)
            db.session.commit()
            flash("Question added!")
            return redirect(url_for('admin.manage_questions'))
    return render_template('admin/add_question.html', chapters=chapters)
