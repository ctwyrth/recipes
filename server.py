from recipes_app import app
from recipes_app.controllers import controllers_recipes
from recipes_app.controllers import controllers_users

if __name__ == '__main__':
    app.run(debug=True)
