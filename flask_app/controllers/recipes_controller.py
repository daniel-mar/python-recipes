from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User


@app.route('/new/recipe')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "user_id": session['user_id']
    }
    return render_template('add.html', user=User.get_by_id(data))


@app.route('/create/recipe', methods=['POST'])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/logout')

    if not Recipe.validate_recipe(request.form):
        return redirect('/new/recipe')

    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "under_30_minutes": request.form.getlist("under_30_minutes"),
        "date_made_on": request.form["date_made_on"],
        "user_id": session["user_id"]
    }
    Recipe.save(data)
    return redirect('/dashboard')



@app.route('/edit/recipe/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    user_data = {
        "user_id": session['user_id']
    }
    user = User.get_by_id(user_data)
    recipe = Recipe.get_one(data)
    return render_template("edit_recipe.html", recipe = recipe, user = user, recipe_id = data)


@app.route('/update/recipe/<int:id>', methods=['POST'])
def update_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect('/new/recipe')
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "under_30_minutes": request.form.getlist("under_30_minutes"),
        "date_made_on": request.form["date_made_on"],
        "id": id
    }
    print(data)
    Recipe.update(data)
    return redirect('/dashboard')

# VIEW INSTRUCTIONS ========== works ====================
@app.route('/recipe/<int:id>')
def show_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    user_data = {
        "user_id": session['user_id']
    }
    user = User.get_by_id(user_data)
    recipe = Recipe.get_one(data)
    # like not working, I want to be able to look at the table specific recipe, that has the user in it
    one_user = recipe.user
    likes = Recipe.get_likes_count(data)

    return render_template("view.html", recipe = recipe, user = user, likes = likes, one_user = one_user)


# works
@app.route('/destroy/recipe/<int:id>')
def destroy_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    Recipe.destroy(data)
    return redirect('/dashboard')
