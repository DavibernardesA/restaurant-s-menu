# routes.py
from flask import Blueprint, request, jsonify
from src.services import fetch_menu, insert_menu_item, update_menu_item_in_db, delete_menu_item_from_db

app_routes = Blueprint('app_routes', __name__)

@app_routes.get('/menu')
def get_menu():
    menu_items = fetch_menu()
    return jsonify(menu_items)

@app_routes.post('/menu')
def add_menu_item():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    available = data.get('available')

    if not name:
        return jsonify({'message': 'Name not provided for menu item'}), 400

    new_id = insert_menu_item(name, description, price, available)

    return jsonify({
        'id': new_id['id'],
        'name': name,
        'description': description,
        'price': price,
        'available': available
    }), 201

@app_routes.put('/menu/<int:item_id>')
def update_menu_item(item_id):
    data = request.get_json()
    name = data.get('name')
    # description = data.get('description')
    # price = data.get('price')
    # available = data.get('available')

    if not name:
        return jsonify({'message': 'Name not provided for menu item'}), 400

    update_menu_item_in_db(item_id, name)

    if(update_menu_item_in_db['status'] == 'success'):

        return jsonify({
            'id': item_id,
            'name': name,
            # 'description': description,
            # 'price': price,
            # 'available': available
        })
    else:
        return jsonify({'message': 'Menu item not found'})

@app_routes.delete('/menu/<int:item_id>')
def delete_menu_item(item_id):
    delete_menu_item_from_db(item_id)
    return jsonify({'message': 'Menu item deleted successfully'})
