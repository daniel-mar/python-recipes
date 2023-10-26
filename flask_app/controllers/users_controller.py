from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.user import User
# add recipes and bcrypt because we know we will want to create then use them
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    # user will go to website and have a wall to login to, no information otherwise
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    # validate the user has logged
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'user_id': session['user_id']
    }
    user = User.get_by_id(data)
    # we do not need to send data to the recipes, we want to grab everything and then AFTER
    # DICTATE if the user has access to them with jinja / user information
    recipes = Recipe.get_all()

    # many to many access to webpage, for unlike and like

    return render_template("dashboard.html", user = user, recipes = recipes)

# ===============================================
# Registering a user
# ==============================================


@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id

    return redirect('/dashboard')

# ============================================
# Login user
# ============================================


@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password", "login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

# ==============================================
# When user logout
# ==============================================


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# =================================
# Link for when the user likes or unlikes in order to update the database
# =================================

@app.route("/add/like/<int:recipe_id>")
def user_add_fav(recipe_id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        "user_id": session["user_id"],
        "recipe_id": recipe_id
    }
    # I do return .. but I'm seeing where I can use the favorite if I even return it
    user_liked = User.add_like(data)
    return redirect('/dashboard')

# ===========================
# remove the likes href route
# =========================
@app.route("/delete/like/<int:recipe_id>")
def user_del_like(recipe_id):
    if "user_id" not in session:
        return redirect('/logout/')
    # taking the foreign key for the join
    data = {
        "user_id" : session["user_id"],
        "recipe_id" : recipe_id
    }
    # I do not believe I need to store the return variable unfavorite
    # delete expects nothing to really return in model
    user_unliked = User.delete_like(data)
    return redirect("/dashboard")