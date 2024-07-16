# routes.py
from flask import Blueprint, request, jsonify
from connection import connect_to_database

app_routes = Blueprint('app_routes', __name__)

# read all
@app_routes.get('/menu')
def get_menu():
    conn = connect_to_database()
    cur = conn.cursor()
    cur.execute('SELECT * FROM menu ORDER BY id')
    menu_items = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(menu_items)

# create
@app_routes.post('/menu')
def add_menu_item():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    available = data.get('available')

    if not name:
        return jsonify({'message': 'Name not provided for menu item'}), 400

    conn = connect_to_database()
    cur = conn.cursor()

    cur.execute('''
        INSERT INTO menu (name, description, price, available) 
        VALUES (%s, %s, %s, %s) RETURNING id
    ''', (name, description, price, available))
    
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        'id': new_id,
        'name': name,
        'description': description,
        'price': price,
        'available': available
    }), 201

# update
@app_routes.put('/menu/<int:item_id>')
def update_menu_item(item_id):
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    available = data.get('available')

    if not name:
        return jsonify({'message': 'Name not provided for menu item'}), 400

    conn = connect_to_database()
    cur = conn.cursor()

    cur.execute('''
        UPDATE menu SET name = %s, description = %s, price = %s, available = %s WHERE id = %s
    ''', (name, description, price, available, item_id))
    
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        'id': item_id,
        'name': name,
        'description': description,
        'price': price,
        'available': available
    })

# delete
@app_routes.delete('/menu/<int:item_id>')
def delete_menu_item(item_id):
    conn = connect_to_database()
    cur = conn.cursor()
    cur.execute('DELETE FROM menu WHERE id = %s', (item_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Menu item deleted successfully'})
