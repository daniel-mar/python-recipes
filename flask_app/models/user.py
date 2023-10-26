from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # begin by empty user database for storing hashed passwords
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at ) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW() )"
        return connectToMySQL('user_recipe').query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('user_recipe').query_db(query)
        users = []
        # row can be considered each user.
        for row in results:
            users.append(cls(row))
        return users

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('user_recipe').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(user_id)s;"
        results = connectToMySQL('user_recipe').query_db(query, data)
        return cls(results[0])


# many to many attempt: recipes

# adding likes many to many
    @classmethod
    def add_like(cls, data):
        query = "INSERT INTO likes (users_id, recipes_id) VALUES ( %(user_id)s, %(recipes_id)s );"
        results = connectToMySQL('tv_shows_schema').query_db(query, data)
        return

# removing the likes many to many
    @classmethod
    def delete_like(cls, data):
        query = "DELETE FROM likes WHERE user_id = %(user_id)s AND recipe_id = %(recipe_id)s;"
        results = connectToMySQL('user_recipe').query_db(query, data)
        # I could return the results to the front end, but I do not believe it is necessary
        # I could "return connectToMySQL('user_recipe').query_db(query, data)"
        return

    @classmethod
    def get_likes(cls, data):
        # ON first table primary key = 2nd table foreign key, 2nd left join the many table's foreign key on the 2nd tables primary key
        query = "SELECT * FROM users LEFT JOIN likes ON users.id = likes.user_id LEFT JOIN recipes ON recipes.id = likes.recipe_id WHERE users.id = %(user_id)s;"
        results = connectToMySQL('user_recipe').query_db(query, data)
        liked_recipes = []
        for row in results:
            liked_recipes.append(row["recipes.id"])
        return liked_recipes



    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('user_recipe').query_db(query, user)
        # When changing the user table, within the schema, specifically the emails
        # if there is a match or it exists, cannot continue
        if len(results) >= 1:
            flash("Email already taken.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!", "register")
            is_valid = False
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters", "register")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters", "register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords don't match", "register")
        return is_valid
