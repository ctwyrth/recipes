from recipes_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

DB = 'recipes'

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[*.!@$%^&(){}[\]:;<>,.?/~_+-=|]).{8,32}$')  # password info pop up or explanation: Must be 8-24 characters long and contain: -1 upper case letter, -1 lower case letter, -1 number, -2 special characters (?!@$%&*-_)
FIRSTNAME_REGEX = re.compile(r'^[A-Za-z]+(((\'|\-)?([A-Za-z])+))?$')
LASTNAME_REGEX = re.compile(r'^(\s)*[A-Za-z]+((\s)?((\'|\-|\.)?([A-Za-z])*))*(\s)*$')

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
    def save_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(fname)s, %(lname)s, %(email)s, %(password)s);"
        return connectToMySQL(DB).query_db(query,data)

    @classmethod
    def show_all_users(cls):
        query = "SELECT * FROM users;"
        users_from_db = connectToMySQL(DB).query_db(query)
        all_users = []
        for user in users_from_db:
            all_users.append(cls(user))
        return all_users

    @classmethod
    def show_user(cls, data):
        query = "SELECT * FROM users WHERE users.id = %(id)s;"
        result = connectToMySQL(DB).query_db(query,data)
        user = cls(result[0])
        return user

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE users.email = %(email)s;"
        result = connectToMySQL(DB).query_db(query,data)
        return result

    @classmethod
    def update_user(cls,data):
        query = "UPDATE users SET first_name=%(fname)s, last_name=%(lname)s, email=%(email)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query,data)

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query,data)

    @staticmethod
    def validate_user(user):
        is_valid = True
        if not user['fname']:
            flash('This is a required field', 'error_firstname')
            is_valid = False
        elif len(user['fname']) < 3:
            flash('Should be more than 3 characters.', 'error_firstname')
            is_valid = False
        elif not FIRSTNAME_REGEX.match(user['fname']):
            flash('The name entered is invalid.', 'error_firstname')
            is_valid = False
        if not user['lname']:
            flash('This is a required field.', 'error_lastname')
            is_valid = False
        elif len(user['lname']) < 3:
            flash('Should be more than 3 characters.', 'error_lastname')
            is_valid = False
        elif not LASTNAME_REGEX.match(user['lname']):
            flash('The name entered is invalid.', 'error_lastname')
            is_valid = False
        if not user['email']:
            flash('This is a required field.', 'error_email')
        elif not User.validate_unique(user['email']):
            flash('That email already exists in our system', 'error_email')
            is_valid = False
        elif not EMAIL_REGEX.match(user['email']):
            flash('That email is invalid', 'error_email')
            is_valid = False
        if not user['password']:
            flash('This is a required field.', 'error_password')
            is_valid = False
        if not user['password1']:
            flash('This is a required field.', 'error_password1')
            is_valid = False
        elif user['password'] != user['password1']:
            flash('The passwords you entered do not match.', 'error_password')
            is_valid = False
        elif not PASSWORD_REGEX.match(user['password']):
            flash('Must be 8-32 characters long, contain 1 upper and lower case letter, 1 number, and 1 special character.' 'error_password')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_unique(email):
        data = {
            'email': email
        }
        isUnique = False
        if not User.get_by_email(data):
            isUnique = True
        return isUnique

    @staticmethod
    def validate_login(login):
        is_valid = True
        if not login['email']:
            flash('This is a required field', 'error_email_login')
            is_valid = False
        elif not EMAIL_REGEX.match(login['email']):
            flash('This is not a valid email address', 'error_email_login')
            is_valid = False
        if not login['password']:
            flash('This is a required field.', 'error_password_login')
            is_valid = False
        elif not PASSWORD_REGEX.match(login['password']):
            flash('Must be 8-24 characters long, contain 1 upper and lower case letter, 1 number, and 1 special character (?!@$%&*-_).' 'error_password_login')
            is_valid = False
        return is_valid

# bcrypt.generate_password_hash(password_string) <--- create hash
# bcrypt.check_password_hash(hashed_password, password_string) <--- compare hash to pwd