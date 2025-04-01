import sqlite3
def connect_db():
#     connect and store same connecction for reuse
    conn = sqlite3.connect('snippets.db')
    return conn,conn.cursor()

def close_db(conn):
    conn.close()



def create_table():
    conn,cursor = connect_db()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS snippets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        code TEXT,
        language TEXT,
        tags TEXT,
        created_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    close_db(conn)

def table_exists(table):
    conn,cursor = connect_db()
    cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name=?', (table,))
    result = cursor.fetchone()
    close_db(conn)
    return result is not None

def add_snippet(title, code, language, tags, created_by):
    conn,cursor = connect_db()
    cursor.execute('''
    INSERT INTO snippets (title, code, language, tags, created_by)
    VALUES (?, ?, ?, ?, ?)
    ''', (title, code, language, tags, created_by))
    conn.commit()
    close_db(conn)

# Function to list all snippets
def list_snippets(filters):
    """
    List all snippets with optional filters.

    Args:
        filters (dict): A dictionary of filters with keys 'language', 'tags', and 'created_by'.

    Returns:
        list: A list of dictionaries representing the snippets.
    """


    if not all(key in ['language', 'tags', 'created_by'] for key in filters.keys()):
        return 'Invalid filter key(s)'

    conn, cursor = connect_db()
    query = 'SELECT * FROM snippets WHERE 1=1'
    for key, value in filters.items():
        query += f' AND {key}=?'

    cursor.execute(query, tuple(filters.values()))
    rows = cursor.fetchall()
    close_db(conn)

    # Convert rows to list of dictionaries
    snippets = []
    for row in rows:
        snippet = {
            'id': row[0],
            'title': row[1],
            'code': row[2],
            'language': row[3],
            'tags': row[4],
            'created_by': row[5],
            'created_at': row[6]
        }
        snippets.append(snippet)

    return snippets



# Function to search snippets by keyword (searching within title and tags)
def search_snippets(keyword):
    conn,cursor = connect_db()
    cursor.execute('''
    SELECT * FROM snippets WHERE title LIKE ? OR tags LIKE ?
    ''', ('%' + keyword + '%', '%' + keyword + '%'))
    results = cursor.fetchall()
    close_db(conn)
    return results


def delete_snippet(snipped_id):
    try:
        co,cu = connect_db()
        cu.execute('''
        DELETE FROM snippets WHERE id = ?
        ''', (snipped_id,))
        co.commit()
        close_db(co)
        return True
    except Exception as e:
        return False


def update_snippet(snippet_id, title, code, language, tags, created_by):
    try:
        conn,cursor = connect_db()
        cursor.execute('''
        UPDATE snippets
        SET title=?, code=?, language=?, tags=?, created_by=?
        WHERE id=?
        ''', (title, code, language, tags, created_by, snippet_id))
        conn.commit()
        close_db(conn)
        return True
    except Exception as e:
        return False
