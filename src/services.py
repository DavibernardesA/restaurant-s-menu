from typing import Union
from pydantic import ValidationError
from src.connection.connection import connect_to_database
from src.models.menu import MenuItem

def fetch_menu() -> list[MenuItem]:
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
        menu_item = MenuItem(id=row[0], name=row[1])
        menu_items.append(menu_item)
    
    return menu_items

def insert_menu_item(name: str) -> MenuItem:
    conn = connect_to_database()
    cur = conn.cursor()
    new_id, new_name = cur.fetchone()
    try:
        menu_item = MenuItem(id=new_id, name=name)
    except ValidationError as e:
        return {'status': 'failure', 'message': e.errors()}

    cur.execute('''
        INSERT INTO menu (name) 
        VALUES (%s) RETURNING id, name
    ''', (menu_item.name,))

    conn.commit()
    cur.close()
    conn.close()

    return MenuItem(id=new_id, name=new_name)

def update_menu_item_in_db(item_id: int, name: str) -> dict[str, str]:
    conn = connect_to_database()
    cur = conn.cursor()

    try:
        cur.execute('SELECT id FROM menu WHERE id = %s', (item_id,))
        item = cur.fetchone()

        if item:
            cur.execute('UPDATE menu SET name = %s WHERE id = %s', (name, item_id))
            conn.commit()
            return {'status': 'success', 'message': 'Item updated successfully'}
        else:
            return {'status': 'failure', 'message': 'Item not found'}
    except Exception as e:
        conn.rollback()
        return {'status': 'failure', 'message': str(e)}
    finally:
        cur.close()
        conn.close()

def delete_menu_item_from_db(item_id: int) -> dict[str, str]:
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

