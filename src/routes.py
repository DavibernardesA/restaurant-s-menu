from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from src.models.menu import MenuItem
from src.services import fetch_menu, insert_menu_item, update_menu_item_in_db, delete_menu_item_from_db

app_routes = Blueprint('app_routes', __name__)

@app_routes.get('/menu')
def get_menu():
    menu_items = fetch_menu()
    return jsonify(menu_items)

@app_routes.post('/menu')
def add_menu_item():
    data = request.get_json()
    try:
        menu_item = MenuItem(**data)
    except ValidationError as e:
        return jsonify(e.erros()), 400
    # description = data.get('description')
    # price = data.get('price')
    # available = data.get('available')

    new_item = insert_menu_item(menu_item.name)

    return jsonify(new_item), 201

@app_routes.put('/menu/<int:item_id>')
def update_menu_item(item_id):
    data = request.get_json()
    try:
        menu_item = MenuItem(**data)
    except ValidationError as e:
        return jsonify(e.erros()), 400
    # description = data.get('description')
    # price = data.get('price')
    # available = data.get('available')

    update_menu_item_in_db(item_id, menu_item.name)

    if(update_menu_item_in_db['status'] == 'success'):

        return jsonify({
            'id': item_id,
            'name': menu_item.name,
            # 'description': description,
            # 'price': price,
            # 'available': available
        })
    else:
        return jsonify({'message': 'Menu item not found'})

@app_routes.delete('/menu/<int:item_id>')
def delete_menu_item(item_id):
    try:
        delete_menu_item_from_db(item_id)
        return jsonify({'message': 'Menu item deleted successfully'})
    except Exception:
        return jsonify({'message': 'Menu item deleted unsuccessfully'})
