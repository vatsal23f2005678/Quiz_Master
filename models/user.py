from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(100),unique=True, nullable=False)
    password=db.Column(db.String(100),nullable=False)
    full_name=db.Column(db.String(100),nullable=False)
    qualification=db.Column(db.String(100))
    dob=db.Column(db.String(100),nullable=False)
    is_admin=db.Column(db.Boolean, default=False)
    def __init__(self, email, password, full_name, qualification, dob,is_admin=False):
        self.email=email
        self.password=password
        self.full_name=full_name
        self.qualification=qualification
        self.dob=dob
        self.is_admin=is_admin
    def __repr__(self):
         return f"<User{self.email}>"