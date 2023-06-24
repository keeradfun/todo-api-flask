from app.database import db
from app.user.utils import hash_password,password_compare
from sqlalchemy import exc

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(100),nullable=False)
    username = db.Column(db.String(200),unique=True,nullable=False)
    password = db.Column(db.String(200),nullable=False)
    active = db.Column(db.Boolean,nullable=False,default=False)

    @staticmethod
    def create_user(username:str,email:str,password:str):
        try:
            new_user = User(
                username = username,
                email = email,
                password = hash_password(password),
                active = False
            )
            db.session.add(new_user)
            db.session.commit()
            return "User created successfully"
        
        except exc.SQLAlchemyError:
            return "Something went wrong"


    def email_exist(email):
        try:
            email_exist = User.query.filter_by(email = email).first()
            if email_exist is None:
                return False
            else:
                return True
            
        except exc.SQLAlchemyError:
            return "something went wrong with email validation homeboy"
        
    
    def username_exist(username):
        try:
            username_exist = User.query.filter_by(username = username).first()
            if username_exist is None:
                return False
            else:
                return True
            
        except exc.SQLAlchemyError:
            return "something went wrong username validation"

    def validate_user(username,email):
        try:
            if User.email_exist(email) and User.username_exist(username):
                return True
            else:
                return False
        except exc.SQLAlchemyError:
            return "Something went wrong while validating"

    def authenticate_user(email,password):
        # try:
            user = User.query.filter_by(email = email).first()
            if user:
                compare = password_compare(user.password,password)
                return compare
            else:
                return False
            
        # except:
        #     return "Something went wrong while authencticating"
