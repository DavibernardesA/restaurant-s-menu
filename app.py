from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import Error

app = Flask(__name__)

db_params = {
    'dbname': 'restaurant_db',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': '5432'
}

def connect_to_database():
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
    except Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
    return conn

# read all
@app.route('/menu', methods=['GET'])
def get_menu():
    conn = connect_to_database()
    cur = conn.cursor()
    cur.execute('SELECT id, name FROM menu ORDER BY id')
    menu_items = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(menu_items)

# create
@app.route('/menu', methods=['POST'])
def add_menu_item():
    data = request.get_json()
    name = data.get('name', None)
    if name:
        conn = connect_to_database()
        cur = conn.cursor()
        cur.execute('INSERT INTO menu (name) VALUES (%s) RETURNING id', (name,))
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'id': new_id, 'name': name}), 201
    else:
        return jsonify({'error': 'Name not provided for menu item'}), 400

# update
@app.route('/menu/<int:item_id>', methods=['PUT'])
def update_menu_item(item_id):
    data = request.get_json()
    name = data.get('name', None)
    if name:
        conn = connect_to_database()
        cur = conn.cursor()
        cur.execute('UPDATE menu SET name = %s WHERE id = %s', (name, item_id))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'id': item_id, 'name': name})
    else:
        return jsonify({'error': 'Name not provided for menu item'}), 400

# delete
@app.route('/menu/<int:item_id>', methods=['DELETE'])
def delete_menu_item(item_id):
    conn = connect_to_database()
    cur = conn.cursor()
    cur.execute('DELETE FROM menu WHERE id = %s', (item_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Menu item deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
