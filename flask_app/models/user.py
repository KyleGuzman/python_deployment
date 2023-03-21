from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_bcrypt import Bcrypt
from flask_app import app
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
bcrypt = Bcrypt(app)


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = """
        INSERT INTO users
        (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        results = connectToMySQL('recipes').query_db(query, data)
        return results

    @classmethod
    def get_email(cls, email):
        data = {
            "email": email
        }
        query = """
        SELECT * FROM users
        WHERE email = %(email)s;
        """
        results = connectToMySQL('recipes').query_db(query, data)
        if results:
            result = results[0]
            user = cls(result)
            return user
        else:
            return False

    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data['first_name']) < 2:
            flash("First name must be at least 2 characters.", 'register')
            is_valid = False
        if len(data['last_name']) < 2:
            flash("Last name must be at least 2 characters.", 'register')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address.", 'register')
            is_valid = False
        if User.get_email(data['email']):
            flash("Email Address already exists!", 'register')
            is_valid = False
        if len(data['password']) < 2:
            flash("Password must be at least 2 characters.", 'register')
            is_valid = False
        if data['password'] != data['password_check']:
            flash("Password does not match!", 'register')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(data):
        is_valid = True
        found_user = User.get_email(data['email'])
        if found_user:
            if bcrypt.check_password_hash(found_user.password, data['password']):
                return found_user
            else:
                flash("Invalid Email or Password", 'login')
                is_valid = False
        else:
            flash("Invalid Email or Password", 'login')
            is_valid = False
        return is_valid
