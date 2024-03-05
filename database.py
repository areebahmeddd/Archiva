import sqlite3

DATABASE_PATH = "database.db"

def create_table():
    query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );
    """

    try:
        with sqlite3.connect(DATABASE_PATH) as connection:
            connection.execute(query)
            print("[Database] Table 'users' created or already exists.")

    except sqlite3.Error as exc:
        print(f'[Database] Error creating or checking table "users": {exc}')

def execute_query(query, parameters = None):
    try:
        with sqlite3.connect(DATABASE_PATH) as connection:
            connection.execute(query, parameters)
            connection.commit()
            print("[Database] Query executed successfully.")

    except sqlite3.Error as exc:
        print(f'[Database] Error executing query: {exc}')

def fetch_query(query, parameters = None):
    result = None

    try:
        with sqlite3.connect(DATABASE_PATH) as connection:
            result = connection.execute(query, parameters).fetchone()
            print("[Database] Data fetched successfully.")

    except sqlite3.Error as exc:
        print(f'[Database] Error fetching data: {exc}')

    return result