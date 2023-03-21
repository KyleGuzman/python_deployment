from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask import flash


class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_cooked = data['date_cooked']
        self.under_thirty = data['under_thirty']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def add_recipe(cls, data):
        query = """
        INSERT INTO recipes
        (name, description, instructions, date_cooked, under_thirty, user_id)
        VALUES (%(name)s, %(description)s, %(instructions)s, %(date_cooked)s, %(under_thirty)s, %(user_id)s);
        """
        results = connectToMySQL('recipes').query_db(query, data)
        return results

    @classmethod
    def get_all_recipes(cls):
        query = """
        SELECT * FROM recipes
        JOIN users
        ON recipes.user_id = users.id;
        """
        results = connectToMySQL('recipes').query_db(query)
        all_recipes = []
        if results:
            for row in results:
                recipe = cls(row)
                user_data = {
                    **row,
                    'id': row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at']
                }
                recipe.creator = User(user_data)
                all_recipes.append(recipe)
            return all_recipes

    @classmethod
    def get_one(cls, id):
        data = {
            "id": id
        }
        query = """
        SELECT * FROM recipes
        JOIN users
        ON recipes.user_id = users.id
        WHERE recipes.id = %(id)s;
        """
        results = connectToMySQL('recipes').query_db(query, data)
        result = results[0]
        recipe = cls(result)
        user_data = {
            **result,
            'id': result['users.id'],
            'created_at': result['users.created_at'],
            'updated_at': result['users.updated_at']
        }
        recipe.creator = User(user_data)
        return recipe

    @classmethod
    def update_recipe(cls, data):
        query = """
        UPDATE recipes
        SET name = %(name)s,
        description = %(description)s,
        instructions = %(instructions)s,
        date_cooked = %(date_cooked)s,
        under_thirty = %(under_thirty)s
        WHERE id = %(id)s;
        """
        results = connectToMySQL('recipes').query_db(query, data)
        return results

    @classmethod
    def delete_recipe(cls, id):
        data = {
            "id": id
        }
        query = """
        DELETE FROM recipes
        WHERE id = %(id)s;
        """
        results = connectToMySQL('recipes').query_db(query, data)
        return results

    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if len(data['name']) < 3:
            flash("Name must be at least 3 characters.", 'add')
            is_valid = False
        if len(data['description']) < 3:
            flash("Description must be at least 3 characters.", 'add')
            is_valid = False
        if len(data['instructions']) < 3:
            flash("Instructions must be at least 3 characters.", 'add')
            is_valid = False
        if data['date_cooked'] == '':
            flash("Please input date when recipe was cooked / made.", 'add')
            is_valid = False
        if data['under_thirty'] == '':
            flash("Please select if recipe is under 30 minutes or not.", 'add')
            is_valid = False
        return is_valid
