from flask_app import app
from flask_app.controllers import users_controller, recipes_controller





# the bottom portion of our controller routes
if __name__ == '__main__':
    app.run(debug=True)