from flask import Blueprint, request, jsonify
from src.connection.connection import connect_to_database

app_routes = Blueprint('app_routes', __name__)

@app_routes.get('/menu')
def get_menu():
    conn = connect_to_database()
    cur = conn.cursor()
    cur.execute('SELECT * FROM menu ORDER BY id')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    menu_items = []
    for row in rows:
        menu_item = {
            'id': row[0],
            'name': row[1],
            'description': row[2],
            'price': row[3],
            'available': row[4]
        }
        menu_items.append(menu_item)
    
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

@app_routes.delete('/menu/<int:item_id>')
def delete_menu_item(item_id):
    conn = connect_to_database()
    cur = conn.cursor()
    cur.execute('DELETE FROM menu WHERE id = %s', (item_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Menu item deleted successfully'})
