from recipes_app import app
from flask import render_template, redirect, request, session
from recipes_app.models.recipes import Recipe


@app.route('/new_recipe')
def new_recipe():
    return render_template('new_recipe.html')

@app.route('/create_recipe', methods=['POST'])
def create_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/?form_route?')
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_made': request.form['dmade'],
        'under30': request.form['under30'],
        'submitted_by': session['user_id']
    }
    id = Recipe.save_recipe(data)
    return redirect(f'/show_recipe/{id}')  # may need to change based on page layout

@app.route('/show_recipes')
def show_all_recipes():
    return render_template('/results', all_recipes = Recipe.show_all_recipes())

@app.route('/show_recipe/<id>')
def show_record(id):
    data = {
        'id': id
    }
    recipes = Recipe.show_recipe(data)
    return render_template("/details.html", recipes = recipes)

@app.route('/edit_recipe/<id>')
def edit(id):
    data = {
        'id': id
    }
    return render_template("edit.html", recipe = Recipe.show_recipe(data))

@app.route('/update_recipe/<id>', methods=['POST'])
def update(id):
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/edit_recipe/{id}')
    data = {
        'id': id,
        "name": request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "dmade": request.form['dmade'],
        "under30": request.form['under30']
    }
    Recipe.update_recipe(data)
    return redirect(f"/show_recipe/{id}")

@app.route('/delete_recipe/<id>') 
def delete(id):
    data = {
        'id': id,
    }
    Recipe.delete_recipe(data)
    return redirect('/show_recipes')