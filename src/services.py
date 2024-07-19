from src.connection.connection import connect_to_database

def fetch_menu():
    conn = connect_to_database()
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM menu ORDER BY id')
        rows = cur.fetchall()
    except Exception as e:
        print(f"Erro ao executar a query: {e}")
        conn.rollback()
        return []
    finally:
        cur.close()
        conn.close()
    
    menu_items = []
    for row in rows:
        menu_item = {
            'id': row[0],
            'name': row[1],
            # 'description': row[2],
            # 'price': row[3],
            # 'available': row[4]
        }
        menu_items.append(menu_item)
    
    return menu_items

def insert_menu_item(name):
    conn = connect_to_database()
    cur = conn.cursor()

    cur.execute('''
        INSERT INTO menu (name) 
        VALUES (%s) RETURNING id, name
    ''', (name,))
    
    new_id, new_name = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return {'id': new_id, 'name': new_name}

def update_menu_item_in_db(item_id, name):
    conn = connect_to_database()
    cur = conn.cursor()

    cur.execute('''
        SELECT id FROM menu WHERE id = %s
    ''', (item_id,))
    item = cur.fetchone()

    if item:
        cur.execute('''
            UPDATE menu SET name = %s WHERE id = %s
        ''', (name, item_id))
        conn.commit()
        cur.close()
        conn.close()
        return {'status': 'success', 'message': 'Item updated successfully'}
    else:
        cur.close()
        conn.close()
        return {'status': 'failure', 'message': 'Item not found'}

def delete_menu_item_from_db(item_id):
    conn = connect_to_database()
    cur = conn.cursor()

    cur.execute('''
        SELECT id FROM menu WHERE id = %s
    ''', (item_id,))
    item = cur.fetchone()

    if item:
        cur.execute('DELETE FROM menu WHERE id = %s', (item_id,))
        conn.commit()
        cur.close()
        conn.close()
        return {'status': 'success', 'message': 'Item updated successfully'}
    else:
        conn.commit()
        cur.close()
        conn.close()
        return {'status': 'failure', 'message': 'Item not found'}

