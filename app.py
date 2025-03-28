from flask import Flask
from controllers.main import main_bp
from controllers.admin import admin_bp
from models.user import db
from controllers.quiz import quiz_bp

app = Flask(__name__)
app.register_blueprint(quiz_bp, url_prefix='/quiz')
app.secret_key='secretkey123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_master.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    
app.register_blueprint(main_bp) 
app.register_blueprint(admin_bp)  

if __name__ == "__main__":
    app.run(debug=True)
