from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')

def connect_to_database():
    conn = None
    try:
        conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_pass,
        host=db_host,
        port=db_port
        )
    except Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
    return conn

# read all
@app.get('/menu')
def get_menu():
    conn = connect_to_database()
    cur = conn.cursor()
    cur.execute('SELECT * FROM menu ORDER BY id')
    menu_items = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(menu_items)

# create
@app.post('/menu')
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
@app.put('/menu/<int:item_id>')
def update_menu_item(item_id):
    data = request.get_json()
    name = data.get('name', )
    description = data.get('description')
    price = data.get('price')
    available = data.get('available')  

    if name:
        conn = connect_to_database()
        cur = conn.cursor()
        cur.execute('UPDATE menu SET name = (%s, %s, %s, %s) WHERE id = %s', (name, description, price, available, item_id))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'id': item_id, 'name': name,  'description': description, 'price': price, 'avaliable': available})
    else:
        return jsonify({'message': 'Name not provided for menu item'}), 400

# delete
@app.delete('/menu/<int:item_id>')
def delete_menu_item(item_id):
    conn = connect_to_database()
    cur = conn.cursor()
    cur.execute('DELETE FROM menu WHERE id = %s', (item_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Menu item deleted successfully'})

if __name__ == '__main__':
    app.run()
