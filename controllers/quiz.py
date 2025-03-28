from flask import Blueprint,flash, request, session, render_template, redirect, url_for, jsonify
from models.quiz import Chapter, Question
from models.user import db, User
from models.quiz import Score
from models.quiz import Subject

quiz_bp = Blueprint('quiz', __name__, url_prefix='/quiz')

@quiz_bp.route('/')
def quiz_home():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    subjects = Subject.query.all()
    return render_template('quiz.html', subjects=subjects)

@quiz_bp.route('/start/<int:chapter_id>')
def start_quiz(chapter_id):
    print(f"START_QUIZ CALLED: chapter_id = {chapter_id}")  

    if 'user_id' not in session:
        print("User not in session. Redirecting to login.")
        return redirect(url_for('main.login'))  

    questions = Question.query.filter_by(chapter_id=chapter_id).all()
    print(f"Fetched {len(questions)} questions for chapter {chapter_id}")

    if not questions:
        print("No questions found!")
        flash("No questions available for this chapter!", "warning")

    print("Rendering quiz_start.html")  
    return render_template('quiz/quiz_start.html', questions=questions, chapter_id=chapter_id, debug="This page is loading")

@quiz_bp.route('/submit', methods=['POST'])
def submit_quiz():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))

    user_id = session['user_id']
    chapter_id = request.form.get('chapter_id')
    questions = Question.query.filter_by(chapter_id=chapter_id).all()

    total_questions = len(questions)
    correct_answers = 0

    for question in questions:
        selected_option = request.form.get(f'question_{question.id}')
        if selected_option and selected_option == question.correct_option:
            correct_answers += 1

    score = round((correct_answers / total_questions) * 100, 2) if total_questions > 0 else 0

    new_score = Score(user_id=user_id, chapter_id=chapter_id, score=score)
    db.session.add(new_score)
    db.session.commit()

    return render_template('quiz/quiz_result.html', score=score, correct=correct_answers, total=total_questions)

@quiz_bp.route('/test-url')
def test_url():
    test_link = url_for('quiz.start_quiz', chapter_id=1)
    return f"Generated URL: {test_link}"
