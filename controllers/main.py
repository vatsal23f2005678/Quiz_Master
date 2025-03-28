from flask import Blueprint, session, Flask, render_template, request, redirect, url_for, g
from models.quiz import Subject  
from models.user import db, User

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('index.html')

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            email=request.form['email']
            password = request.form['password']
            full_name = request.form['full_name']
            qualification = request.form.get('qualification', '')
            dob = request.form.get('dob')
            is_admin = request.form.get('is_admin') == 'on'
            new_user = User(email=email, password=password, full_name=full_name, qualification=qualification, dob=dob, is_admin=is_admin)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('main.login'))
        except Exception as e:
            print("Error:", e)  
            return "Error . Check the log.", 500
    return render_template('register.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['user_id'] = user.id
            session['admin'] = user.is_admin 

            return redirect(url_for('main.dashboard'))
        else:
            return "Invalid credentials!"
    return render_template('login.html')

@main_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    g.user = User.query.get(user_id) if user_id else None

@main_bp.route('/dashboard')
def dashboard():
    subjects = Subject.query.all()
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    if g.user.is_admin:
        return render_template('admin/dashboard.html', user=g.user, subjects=subjects)  
    return render_template('user/dashboard.html', user=g.user, subjects=subjects)

@main_bp.route('/logout')
def logout():
    session.pop('user_id',None)
    return redirect(url_for('main.login'))

