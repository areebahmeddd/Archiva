import sqlite3
from tabulate import tabulate

DATABASE_PATH = "database.db"

def test():
    try:
        with sqlite3.connect(DATABASE_PATH) as connection:
            user_data = connection.execute("SELECT * FROM users").fetchall()

            if user_data:
                columns = ["User ID", "Username", "Email", "Phone", "Password"]
                print(tabulate(user_data, headers = columns, tablefmt = "grid"))
            else:
                print("No users found in the database.")

    except sqlite3.Error as exc:
        print(f'Error accessing the database: {exc}')

test()