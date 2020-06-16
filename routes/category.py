from flask import Flask, render_template, jsonify, request, Blueprint
from models import db, Category
from flask_jwt_extended import jwt_required

route_categories = Blueprint('route_categories', __name__)
@route_categories.route('/categories', methods=['POST'])
@route_categories.route('/categories/<int:id>', methods=['PUT','DELETE'])
@jwt_required
def categories(id=None):
    if request.method == 'POST':
        name = request.json.get('name')
        name_esp = request.json.get('name_esp')
        consumer_id = request.json.get('consumer_id')
        if not name:
            return jsonify({"error": "Name is required"}), 422 
        if not name_esp:
            return jsonify({"error": "Name in spanish is required"}), 422 
        if not consumer_id:
            return jsonify({"error": "consumer_id is required"}), 422 
        category = Category()
        category.name = name
        category.name_esp = name_esp
        category.consumer_id = consumer_id
        db.session.add(category)
        db.session.commit()
        return jsonify(category.serialize()), 201
    
    if request.method == 'PUT':
        category = Category.query.get(id)
        category.name_esp = request.json.get('name_esp')
        category.name = request.json.get('name')
        db.session.commit()
        return jsonify(category.serialize()), 200

    if request.method == 'DELETE':
        category = Category.query.get(id)
        db.session.delete(category)
        db.session.commit()
        return jsonify({'success':'Deleted'}), 200

@route_categories.route('/category', methods=['GET'])
@route_categories.route('/category/<int:id>', methods=['GET'])
@route_categories.route('/categories/<int:not_all>', methods=['GET'])
def freecategories(id=None, not_all = None):
    if request.method == 'GET':
        if id is not None:
            category = Category.query.get(id)
            if category:
                return jsonify(category.serialize()), 200
            else:
                return jsonify({"error": "Not found"})
        else:
            if not_all is 0:
                categories = Category.query.all()
                categories = list(map(lambda category: category.serialize(),categories))
                return jsonify(categories), 200
            else:
                categories = Category.query.filter(Category.id != not_all).all()
                categories = list(map(lambda category: category.serialize(),categories))
                return jsonify(categories), 200