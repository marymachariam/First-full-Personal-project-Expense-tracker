import sqlite3

def get_connection():
    connect = sqlite3.connect('budget_tracker.db', check_same_thread=False)
    connect.execute("PRAGMA foreign_keys = ON")
    return connect

connect = get_connection()

def get_cursor():
    return connect.cursor()

cursor = connect.cursor() 

# 2. table to store users
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
               user_id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT UNIQUE,
               email TEXT UNIQUE,
               password TEXT NOT NULL,
               created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
               )
''')
connect.commit()

# 3. table for transactions
cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
               transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_id INTEGER,
               category_id INTEGER,
               amount REAL NOT NULL,
               type TEXT NOT NULL,
               description TEXT NOT NULL,
               date DATE NOT NULL,
               created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
               FOREIGN KEY (user_id) REFERENCES users(user_id),
               FOREIGN KEY(category_id) REFERENCES categories(category_id)
               )
''')
connect.commit()

#table for categories
cursor.execute('''
CREATE TABLE IF NOT EXISTS categories (
               category_id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_id INTEGER,
               category_name TEXT NOT NULL,
               UNIQUE(user_id, category_name),
               FOREIGN KEY (user_id) REFERENCES users(user_id)
               )
''')
connect.commit()
# table for setting buget
cursor.execute('''
CREATE TABLE IF NOT EXISTS budgets (
               budget_id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_id INTEGER,
               category_id INTEGER,
               amount REAL NOT NULL,
               month INTEGER,
               year INTEGER,
               FOREIGN KEY (user_id) REFERENCES users(user_id),
               FOREIGN KEY(category_id) REFERENCES categories(category_id)
               )
''')
connect.commit()

