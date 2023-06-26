from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def hash_password(pw):
    return bcrypt.generate_password_hash(pw,10).decode('utf-8')


def password_compare(hashed_pw,pw):
    return bcrypt.check_password_hash(hashed_pw, pw)

