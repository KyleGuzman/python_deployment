from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.recipe import Recipe
from datetime import datetime


@app.route('/save_recipe', methods=['POST'])
def save_recipe():
    data = {
        "name": request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "date_cooked": request.form['date_cooked'],
        "under_thirty": request.form['under_thirty'],
        "user_id": session['id']
    }
    if not Recipe.validate_recipe(data):
        return redirect('/add_recipe')
    Recipe.add_recipe(data)
    return redirect("/show")


@app.route('/add_recipe')
def add_recipes():
    if 'first_name' not in session:
        return redirect('/')
    return render_template('add_recipes.html')


@app.route('/instructions/<int:id>')
def instructions(id):
    if 'first_name' not in session:
        return redirect('/')
    recipe = Recipe.get_one(id)
    date = recipe.date_cooked.strftime("%A - %B %d, %Y")
    return render_template('instructions.html', recipe=recipe, date=date)


@app.route('/edit/<int:id>')
def edit_recipe(id):
    if 'first_name' not in session:
        return redirect('/')
    session['rid'] = id
    recipe = Recipe.get_one(id)
    date = recipe.date_cooked.strftime("%Y-%m-%d")
    return render_template('edit_recipe.html', recipe=recipe, date=date)


@app.route('/update_recipe', methods=['POST'])
def update_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect(f"/edit/{session['rid']}")
    Recipe.update_recipe(request.form)
    return redirect("/show")


@app.route('/delete/<int:id>')
def delete_recipe(id):
    Recipe.delete_recipe(id)
    return redirect('/show')
