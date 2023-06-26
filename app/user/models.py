from app.database import db
from app.user.utils import hash_password, password_compare
from sqlalchemy import exc
from sqlalchemy import delete


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=False)
    superadmin = db.Column(db.Boolean, nullable=False, default=False)

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except exc.SQLAlchemyError:
            return None

    @classmethod
    def findone(cls, id):
        try:
            user = cls.query.filter_by(id=id).first()
            if user:
                return user
            else:
                return None
        except:
            return None

    @classmethod
    def findall(cls):
        try:
            users = cls.query.filter()
            if users:
                return users
            else:
                return None
        except:
            return None

    @classmethod
    def email_exist(cls, email):
        try:
            email_exist = cls.query.filter_by(email=email).first()
            if email_exist is None:
                return False
            else:
                return True

        except exc.SQLAlchemyError:
            return None

    @classmethod
    def username_exist(cls, username):
        try:
            username_exist = cls.query.filter_by(username=username).first()
            print(username_exist)
            if username_exist is None:
                return False
            else:
                return True

        except exc.SQLAlchemyError:
            return "something went wrong username validation"

    @classmethod
    def authenticate_user(cls, email, password):
        try:
            user = cls.query.filter_by(email=email).first()
            if user:
                compare = password_compare(user.password, password)
                if compare:
                    return user
                return None
            else:
                return None

        except:
            return None

    @classmethod
    def update_password(cls, id, password):
        try:
            update = cls.query.filter_by(id=id).first()
            update.password = hash_password(password)
            db.session.commit()
            return True
        except:
            return None

    @classmethod
    def update(cls, id, data):
        try:
            update = cls.query.filter_by(id=id).update(
                data, synchronize_session=False)
            db.session.commit()
            return update
        except:
            return None

    @classmethod
    def delete(cls, id):
        try:
            delete = cls.query.filter_by(id=id).delete()
            db.session.commit()
            return True
        except:
            return False
