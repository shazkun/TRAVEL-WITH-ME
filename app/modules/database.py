import sqlite3
import datetime

current_datetime = datetime.datetime.now()

# Format date and time separately
date_today = current_datetime.strftime("%Y-%m-%d")
time_today = current_datetime.strftime("%H:%M:%S")


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
        
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            action TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS packages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            package_type TEXT NOT NULL,
            destination TEXT NOT NULL,
            cost TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        """)
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
            cost TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        self.conn.commit()

    def set_bg(self, user_id, dark_mode_value):
        try:
            dark_mode_int = int(dark_mode_value)
            self.cursor.execute(
                'UPDATE users SET dark_mode = ? WHERE id = ?', (dark_mode_int, user_id))
            self.conn.commit()
        except Exception as e:
            print("An error occurred while setting background:", e)

    def get_bg(self, user_id):
        try:
            self.cursor.execute(
                'SELECT dark_mode FROM users WHERE id = ?', (user_id,))
            dark_mode_value = self.cursor.fetchone()
            if dark_mode_value is not None:
                return bool(dark_mode_value[0])
            else:
                return None
        except Exception as e:
            print("An error occurred while getting background:", e)
            return None

# USER-----------------------------------------------------------------

    def register_user(self, username, password):
        try:
            self.cursor.execute(
                'INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Username already exists
        except Exception as e:
            print("An error occurred while registering user:", e)
            return False

    def login_user(self, username, password):
        try:
            self.cursor.execute(
                'SELECT id FROM users WHERE username = ? AND password = ?', (username, password))
            user = self.cursor.fetchone()
            if user:
                return user[0]  # Return user ID
            return None
        except Exception as e:
            print("An error occurred while logging in user:", e)
            return None
# CLIENTS-----------------------------------------------------------------

    def insert_client(self, user_id, name, contact, date, time, pax, location, type, destination, cost):
        try:
            self.cursor.execute('''
                INSERT INTO clients (user_id, name, contact, date, time, pax, location, type, destination, cost)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, name, contact, date, time, pax, location, type, destination, cost))
            self.insert_logs(user_id, date_today, time_today,'add client')
            self.conn.commit()
        except Exception as e:
            print("An error occurred while inserting client:", e)

    def fetch_user_clients(self, user_id):
        try:
            self.cursor.execute(
                "SELECT id, name, contact, date, time, pax, location, type, destination, cost FROM clients WHERE user_id = ?", (user_id,))
            return self.cursor.fetchall()
        except Exception as e:
            print("An error occurred while fetching user clients:", e)
            return []

    def fetch_user_clients_by_date(self, user_id, date):
        try:
            with self.conn:
                cursor = self.conn.cursor()
                query = "SELECT * FROM clients WHERE user_id = ?  AND date = ?"
                cursor.execute(query, (user_id, date))
                return cursor.fetchall()
        except Exception as e:
            print("An error occurred while fetching user clients by date:", e)
            return []

    def fetch_user_clients_one(self, user_id, cid):
        try:
            self.cursor.execute(
                "SELECT id, name, contact, date, time, pax, location, type, destination, cost FROM clients WHERE user_id = ? AND id = ?", (user_id, cid))
            user_data = self.cursor.fetchone()
            print("Fetched user data:", user_data)
            if user_data:
                columns = ['id', 'name', 'contact', 'date', 'time',
                           'pax', 'location', 'type', 'destination', 'cost']
                return dict(zip(columns, user_data))
            else:
                return None
        except Exception as e:
            print("An error occurred while fetching user clients one:", e)
            return None

    def update_client(self, user_id, client_id, name, contact, date, time, pax, location, type, destination, cost):
        try:
            self.cursor.execute("""
                UPDATE clients
                SET name = ?, contact = ?, date = ?, time = ?, pax = ?, location = ?, type = ?, destination = ?, cost = ?
                WHERE user_id = ? AND id = ?""",
                                (name, contact, date, time, pax, location, type, destination, cost,user_id, client_id ))
            self.insert_logs(user_id,date_today, time_today,'update client')
            self.conn.commit()
        except Exception as e:
            print("An error occurred while updating client:", e)

    def delete_client(self, user_id, client_id):
        try:
            self.cursor.execute(
                "DELETE FROM clients WHERE user_id = ? AND id = ?", (user_id, client_id))
            self.insert_logs(user_id,date_today, time_today,'delete client')
            self.conn.commit()
        except Exception as e:
            print("An error occurred while deleting client:", e)



# PACKAGES-----------------------------------------------------------------



    def insert_package(self, user_id, package_type, destination, cost):
        try:
            self.cursor.execute("INSERT INTO packages (user_id, package_type, destination, cost) VALUES (?, ?, ?, ?)",
                                (user_id, package_type, destination, cost))
            self.insert_logs(user_id, date_today, time_today, 'add package')
            self.conn.commit()
        except Exception as e:
            print("An error occurred while inserting package:", e)

    def fetch_user_packages(self, user_id):
        try:
            self.cursor.execute(
                "SELECT id, package_type,destination,cost FROM packages WHERE user_id = ?", (user_id,))
            return self.cursor.fetchall()
        except Exception as e:
            print("An error occurred while fetching user packages:", e)
            return []

    def fetch_user_packages_one(self, user_id, pid):
        try:
            self.cursor.execute(
                "SELECT id, package_type,destination,cost FROM packages WHERE user_id = ? AND id = ?", (user_id, pid))
            rows = self.cursor.fetchall()

            # Define column names based on your SQL query
            column_names = ["id", "package_type", "destination", "cost"]

            # Convert each row to a dictionary
            result = [dict(zip(column_names, row)) for row in rows]
            return result
        except Exception as e:
            print("An error occurred while fetching user package by id:", e)
            return None

    def get_packages(self, user_id):
        try:
            self.cursor.execute(
                "SELECT id, package_type, destination, cost FROM packages WHERE user_id = ?", (user_id,))
            rows = self.cursor.fetchall()

            # Define column names based on your SQL query
            column_names = ["id", "package_type", "destination", "cost"]

            # Convert each row to a dictionary
            result = [dict(zip(column_names, row)) for row in rows]
            return result
        except Exception as e:
            print("An error occurred while getting packages:", e)
            return []

    def update_package(self, package_id, package_type, destination, cost):
        try:
            self.cursor.execute("UPDATE packages SET package_type = ?, destination = ?, cost = ? WHERE id = ?",
                                (package_type, destination, cost, package_id))
            self.insert_logs(self.user_id, date_today, time_today, 'update package')
            self.conn.commit()
        except Exception as e:
            print("An error occurred while updating package:", e)

    def delete_package(self, package_id, user_id):
        try:
            self.cursor.execute("DELETE FROM packages WHERE id = ? AND user_id", (package_id,user_id))
            self.insert_logs(user_id,date_today, time_today,'delete client')
            self.conn.commit()
        except Exception as e:
            print("An error occurred while deleting package:", e)
#LOGS----------------------------------------------

    def insert_logs(self, user_id, date, time, action):
        try:
            self.cursor.execute("INSERT INTO logs (user_id, date, time, action) VALUES (?, ?, ?, ?)",
                                (user_id, date, time, action))
        except Exception as e:
            print("An error occurred while inserting logs:", e)

    def fetch_data(self, user_id):
        try:
            self.cursor.execute(
                "SELECT date,time,action FROM logs WHERE user_id = ?", (user_id,))
            return self.cursor.fetchall()
        except Exception as e:
            print("An error occurred while fetching data:", e)
            return []

    def delete_logs(self, log_id):
        try:
            self.cursor.execute("DELETE FROM logs WHERE id = ?", (log_id,))
            self.conn.commit()
        except Exception as e:
            print("An error occurred while deleting logs:", e)

    def close(self):
        self.conn.close()
