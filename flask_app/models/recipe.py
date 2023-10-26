from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30_minutes = data['under_30_minutes']
        self.date_made_on = data['date_made_on']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # make sure to have the user_id foreign key here for jinja on dashboard
        # important for if statement editting
        self.user_id = data['user_id']
        # the following is for many to many
        # then in the controller, call the recipe.likes and store that as a values
        # to push to html for jinja
        self.recipe_likes = []
        self.user = []

    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, date_made_on, under_30_minutes, created_at, updated_at, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made_on)s, %(under_30_minutes)s, NOW(), NOW(), %(user_id)s);"
        return connectToMySQL('user_recipe').query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL('user_recipe').query_db(query)
        all_recipes = []
        for row in results:
            all_recipes.append(cls(row))
        return all_recipes

    # many to many part, get and count likes
    # pass the data id as "id", 
    @classmethod
    def get_likes_count(cls, data):
        query = "SELECT COUNT(users_id) AS liked FROM likes WHERE recipes_id = %(id)s;"
        results = connectToMySQL('user_recipe').query_db(query, data)
        return results

# get 1 recipe
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL('user_recipe').query_db(query, data)
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, date_made_on=%(date_made_on)s, under_30_minutes=%(under_30_minutes)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL('user_recipe').query_db(query, data)

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL('user_recipe').query_db(query, data)

    @staticmethod
    def validate_recipe(data):
        is_valid = True

        size_instruction = len(data['instructions'])

        if len(data['name']) < 3:
            flash("Name must be at least 3 characters")
            is_valid = False
        if size_instruction < 3:
            flash("Instructions must be at least 3 characters")
            is_valid = False
        if len(data['description']) < 3:
            flash("Description must be at least 3 characters")
            is_valid = False
        if not data['date_made_on']:
            flash("Please enter a date")
            is_valid = False
        if not data.getlist('under_30_minutes'):
            flash("You must provide and under or over 30 minutes")
            is_valid = False

        return is_valid
