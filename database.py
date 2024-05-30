import sqlite3

class DatabaseHandler:
    def __init__(self, db_name='user_clients.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.setup_db()

    def setup_db(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        dark_mode BOOLEAN DEFAULT 0
    )
    ''')
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT NOT NULL,
            contact TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            pax TEXT NOT NULL,
            location TEXT NOT NULL,
            type TEXT NOT NULL,
            destination TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        self.conn.commit()

    def set_bg(self, user_id, dark_mode_value):
        dark_mode_int = int(dark_mode_value)
        self.cursor.execute('UPDATE users SET dark_mode = ? WHERE id = ?', (dark_mode_int, user_id))
        self.conn.commit()

    def get_bg(self, user_id):
        self.cursor.execute('SELECT dark_mode FROM users WHERE id = ?', (user_id,))
        dark_mode_value = self.cursor.fetchone()
        if dark_mode_value is not None:
            return bool(dark_mode_value[0])
        else:
            return None

    def register_user(self, username, password):
        try:
            self.cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            self.conn.commit()
        except sqlite3.IntegrityError:
            return False  # Username already exists
        return True

    def login_user(self, username, password):
        self.cursor.execute('SELECT id FROM users WHERE username = ? AND password = ?', (username, password))
        user = self.cursor.fetchone()
        if user:
            return user[0]  # Return user ID
        return None

    def insert_client(self, user_id, name, contact, date, time, pax, location, type, destination):
        self.cursor.execute('''
        INSERT INTO clients (user_id, name, contact, date, time, pax, location, type, destination)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, name, contact, date, time, pax, location, type, destination))
        self.conn.commit()

        

    def fetch_user_clients(self, user_id):
        self.cursor.execute("SELECT id, name, contact, date, time, pax, location, type, destination FROM clients WHERE user_id = ?", (user_id,))
        return self.cursor.fetchall()
    

    def fetch_user_clients_by_date(self, user_id, date):
        with self.conn:
            cursor = self.conn.cursor()
            query = "SELECT * FROM clients WHERE user_id = ?  AND date = ?"
            cursor.execute(query, (user_id, date))
            return cursor.fetchall()
        

    def fetch_user_clients_one(self, user_id, cid):
        self.cursor.execute("SELECT id, name, contact, date, time, pax, location, type, destination FROM clients WHERE user_id = ? AND id = ?", (user_id, cid))
        user_data = self.cursor.fetchone()
        print("Fetched user data:", user_data)  
        if user_data:
            columns = ['id', 'name', 'contact', 'date', 'time', 'pax', 'location', 'type', 'destination']
            return dict(zip(columns, user_data))
        else:
            return None
    

    def update_client(self, user_id, client_id, name, contact, date, time, pax, location, type, destination):
        self.cursor.execute("""
            UPDATE clients
            SET name = ?, contact = ?, date = ?, time = ?, pax = ?, location = ?, type = ?, destination = ?
            WHERE user_id = ? AND id = ?""",
            (name, contact, date, time, pax, location, type, destination, user_id, client_id))
        self.conn.commit()
    

    def delete_client(self, user_id,client_id):
        self.cursor.execute("DELETE FROM clients WHERE user_id = ? AND id = ?", (user_id,client_id))
        self.conn.commit()
    

    def close(self):
        self.conn.close()
