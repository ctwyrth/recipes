from recipes_app.config.mysqlconnection import connectToMySQL
from flask import flash

DB = 'recipes'

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under30 = data['under30']
        self.date_made = data['date_made']
        self.submitted_by = data['submitted_by']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save_recipe(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, under30, date_made, submitted_by) VALUES (%(name)s, %(description)s, %(instructions)s, %(under30)s, %(dmade)s, %(submitted_by)s);"
        return connectToMySQL(DB).query_db(query,data)

    @classmethod
    def show_all_recipes(cls):
        query = "SELECT * FROM recipes;"
        recipes_from_db = connectToMySQL(DB).query_db(query)
        all_recipes = []
        if not recipes_from_db:
            return all_recipes
        elif len(recipes_from_db) == 1:
            all_recipes.append(cls(recipes_from_db[0]))
        else:
            for recipe in recipes_from_db:
                all_recipes.append(cls(recipe))
        return all_recipes

    @classmethod
    def show_recipe(cls, data):
        query = "SELECT * FROM recipes WHERE recipes.id = %(id)s;"
        results = connectToMySQL(DB).query_db(query,data)
        result = cls(results[0])
        print(result)
        return result

    @classmethod
    def update_recipe(cls,data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, date_made=%(dmade)s, under30=%(under30)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query,data)

    @classmethod
    def delete_recipe(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query,data)

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if not recipe['name']:
            flash("This is a required field.", 'error_name')
            is_valid = False
        elif len(recipe['name']) < 3:
            flash('This needs to be longer than 3 characters.', 'error_name')
        if not recipe['description']:
            flash("This is a required field.", 'error_description')
            is_valid = False
        elif len(recipe['description']) < 3:
            flash('This field needs to be more than 3 characters long.', 'error_description')
            is_valid = False
        if not recipe['instructions']:
            flash("This is a required field.", 'error_instructions')
            is_valid = False
        elif len(recipe['instructions']) < 3:
            flash('This field needs to be more than 3 characters long.', 'error_instructions')
            is_valid = False
        if not recipe['dmade']:
            flash('This is a required field.', 'error_dmade')
        if not recipe['under30']:
            flash('This is a required field.')
            is_valid = False
        return is_valid



# bcrypt.generate_password_hash(password_string) <--- create hash
# bcrypt.check_password_hash(hashed_password, password_string) <--- compare hash to pwd