import sqlite3
from datetime import datetime, date


class DatabaseManager:
    def __init__(self, db_name='poultry_farm.db'):
        self.db_name = db_name
        self.init_database()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def init_database(self):
        """Initialize all database tables"""
        conn = self.get_connection()
        c = conn.cursor()

        # Customers table
        c.execute('''CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            address TEXT,
            date_registered DATE
        )''')

        # Inputs table (feeds, medicines, equipment, etc.)
        c.execute('''CREATE TABLE IF NOT EXISTS inputs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            category TEXT,
            quantity REAL,
            unit TEXT,
            cost_per_unit REAL,
            total_cost REAL,
            supplier TEXT,
            date_purchased DATE
        )''')

        # Outputs table (eggs, chickens, etc.)
        c.execute('''CREATE TABLE IF NOT EXISTS outputs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            quantity REAL,
            unit TEXT,
            price_per_unit REAL,
            total_revenue REAL,
            customer_id INTEGER,
            date_sold DATE,
            transport_cost REAL,
            delivery_status TEXT DEFAULT 'Pending',
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        )''')

        # Messages table
        c.execute('''CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            message TEXT,
            message_type TEXT,
            date_sent DATETIME,
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        )''')

        conn.commit()
        conn.close()

    def row_to_dict(self,row: columns):
        """Convert SQLite row to dictionary"""
        return dict(zip(columns, row)) if row else None

    def rows_to_dict_list(self, rows, columns):
        """Convert list of SQLite rows to list of dictionaries"""
        return [dict(zip(columns, row)) for row in rows]


# Database instance
db = DatabaseManager()