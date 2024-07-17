# services.py
from src.connection.connection import connect_to_database

def fetch_menu():
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
    
    return menu_items

def insert_menu_item(name, description, price, available):
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

    return new_id

def update_menu_item_in_db(item_id, name, description, price, available):
    conn = connect_to_database()
    cur = conn.cursor()

    cur.execute('''
        UPDATE menu SET name = %s, description = %s, price = %s, available = %s WHERE id = %s
    ''', (name, description, price, available, item_id))
    
    conn.commit()
    cur.close()
    conn.close()

def delete_menu_item_from_db(item_id):
    conn = connect_to_database()
    cur = conn.cursor()
    cur.execute('DELETE FROM menu WHERE id = %s', (item_id,))
    conn.commit()
    cur.close()
    conn.close()
