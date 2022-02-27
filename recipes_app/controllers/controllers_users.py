from recipes_app import app
from flask import render_template, redirect, request, session
from recipes_app.models.users import User
from recipes_app.models.recipes import Recipe
from flask_bcrypt import Bcrypt
from flask import flash

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_user', methods=['POST'])
def create_user():
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])  # creates hashed pw
    print(pw_hash)
    data = {
        'fname': request.form['fname'],
        'lname': request.form['lname'],
        'email': request.form['email'],
        'password': pw_hash
    }
    user_id = User.save_user(data)  # returns new id from INSERT query
    session['user_id'] = user_id  # to pass information between pages
    session['fname'] = data['fname']
    session['lname'] = data['lname']
    return redirect('/welcome')

@app.route('/login_check', methods=['POST'])
def login():
    if not User.validate_login(request.form):
        return redirect('/')
    data = {
        'email': request.form['email']
    }
    users_in_db = User.get_by_email(data)
    if not users_in_db:
        flash('No such email exists in our records.', 'error_email_login')
        return redirect('/')
    else:
        user_in_db = users_in_db[0]
    if not bcrypt.check_password_hash(user_in_db['password'], request.form['password']):
        flash('The password you entered does not match the username you provided.', 'error_password_login')
        return redirect('/')
    session['user_id'] = user_in_db['id']
    session['fname'] = user_in_db['first_name']
    session['lname'] = user_in_db['last_name']
    return redirect('/welcome')

@app.route('/welcome')
def welcome():
    if 'user_id' not in session:
        return redirect('/')
    recipes = Recipe.show_all_recipes()
    return render_template('/dashboard.html', recipes = recipes)

@app.route('/show/user/<int:id>')
def show_user(id):
    data = {
        'id': id
    }
    return render_template("/details.html", user = User.show_user(data))

@app.route('/edit/user/<int:id>')
def edit_user(id):
    data = {
        'id': id
    }
    return render_template("edit.html", user = User.show_user(data))

@app.route('/update/user/<int:id>') 
def update_user(id):
    data = {
        'id': id,
        'fname':request.form['fname'],
        'lname':request.form['lname'],
        'email':request.form['email']
    }
    User.update_user(data)
    return redirect(f"/show/user/{id}")

@app.route('/delete/user/<int:id>') 
def delete_user(id):
    data = {
        'id': id,
    }
    User.delete_user(data)
    session.clear()
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')