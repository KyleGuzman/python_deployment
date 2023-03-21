from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    session['first_name'] = data['first_name']
    session['id'] = User.create(data)
    return redirect('/show')


@app.route('/login', methods=['POST'])
def login():
    user_logged_in = User.validate_login(request.form)
    if not user_logged_in:
        return redirect('/')
    session['id'] = user_logged_in.id
    session['first_name'] = user_logged_in.first_name
    return redirect('/show')


@app.route('/show')
def show_recipes():
    if 'first_name' not in session:
        return redirect('/')
    recipes = Recipe.get_all_recipes()
    return render_template('/recipes.html', recipes=recipes)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
