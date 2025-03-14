import sqlite3


def connection():
    return sqlite3.connect('db1')

if connection():
    print('yes')
else:
    print('no')

def create_db():
    conn = connection()
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS name (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL
    )
    
    ''')

    print('Table created')

# create_db()

def insert_data(name, age):
    con = connection()
    cursor = con.cursor()

    # cursor.execute(
    #     'INSERT INTO names (name, age) VALUES (?, ?)', ('John', 34))

    cursor.execute('INSERT INTO name (name, age) VALUES (?, ?)', (name, age))

    con.commit()
    print('Names entered')


# insert_data()

def query():
    conn = connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM name')
    rows = cursor.fetchall()

    return rows

answer = query()

print(answer)

