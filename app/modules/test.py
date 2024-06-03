import unittest
import sqlite3
from database import DatabaseHandler  # Assuming your database handler is in a file named database_handler.py


class TestDatabaseFunctionality(unittest.TestCase):
    def setUp(self):
        # Connect to the test database
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()

        # Create tables in the test database
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
                cost TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS packages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                package_type TEXT NOT NULL,
                destination TEXT NOT NULL,
                cost TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        # Initialize DatabaseHandler with the test database
        self.db_handler = DatabaseHandler(db_name=':memory:')

    def tearDown(self):
        # Close the database connection
        self.conn.close()

    def test_register_and_login_user(self):
        # Register a user
        self.assertTrue(self.db_handler.register_user('test_user', 'test_password'))

        # Check if the user was successfully registered
        self.assertEqual(self.db_handler.login_user('test_user', 'test_password'), 1)

    def test_insert_and_fetch_user_clients(self):
        # Insert a client
        self.db_handler.insert_client(1, 'John Doe', '1234567890', '2024-06-02', '12:00', 2, 'Location', 'Type', 'Destination', '100')

        # Fetch the inserted client
        clients = self.db_handler.fetch_user_clients(1)
        self.assertEqual(len(clients), 1)
        self.assertEqual(clients[0][1], 'John Doe')

    def test_update_and_delete_client(self):
        # Insert a client
        self.db_handler.insert_client(1, 'John Doe', '1234567890', '2024-06-02', '12:00', 2, 'Location', 'Type', 'Destination', '100')

        # Update the client
        self.db_handler.update_client(1, 1, 'Jane Doe', '0987654321', '2024-06-03', '13:00', 3, 'New Location', 'New Type', 'New Destination', '200')

        # Fetch the updated client
        updated_client = self.db_handler.fetch_user_clients_one(1, 1)
        self.assertEqual(updated_client['name'], 'Jane Doe')
        self.assertEqual(updated_client['contact'], '0987654321')
        self.assertEqual(updated_client['date'], '2024-06-03')
        self.assertEqual(updated_client['time'], '13:00')

        # Delete the client
        self.db_handler.delete_client(1, 1)

        # Ensure the client is deleted
        self.assertIsNone(self.db_handler.fetch_user_clients_one(1, 1))

    def test_insert_and_fetch_user_packages(self):
        # Insert a package
        self.db_handler.insert_package(1, 'Standard', 'Destination', '100')

        # Fetch the inserted package
        packages = self.db_handler.fetch_user_packages(1)
        self.assertEqual(len(packages), 1)
        self.assertEqual(packages[0][1], 'Standard')

    def test_update_and_delete_package(self):
        # Insert a package
        self.db_handler.insert_package(1, 'Standard', 'Destination', '100')

        # Update the package
        self.db_handler.update_package(1, 'Deluxe', 'New Destination', '200')  # Change the package ID to an integer

        # Fetch the updated package
        updated_package_list = self.db_handler.fetch_user_packages_one(1, 1)
        if updated_package_list:  # Check if the package exists
            updated_package = updated_package_list[0]  # Get the first item from the list
            self.assertEqual(updated_package['package_type'], 'Deluxe')
            self.assertEqual(updated_package['destination'], 'New Destination')
            self.assertEqual(updated_package['cost'], '200')
        else:
            self.fail("Failed to fetch the updated package")

        # Delete the package
        self.db_handler.delete_package(1)

        # Ensure the package is deleted
        self.assertEqual(self.db_handler.fetch_user_packages(1), [])


    # Add more test methods for other functionalities...

if __name__ == '__main__':
    unittest.main()
