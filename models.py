from database import db
from datetime import datetime, date


class Customer:
    @staticmethod
    def get_all():
        conn = db.get_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM customers ORDER BY date_registered DESC')
        customers = c.fetchall()
        conn.close()

        columns = ['id', 'name', 'phone', 'email', 'address', 'date_registered']
        return db.rows_to_dict_list(customers, columns)

    @staticmethod
    def get_by_id(customer_id):
        conn = db.get_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
        customer = c.fetchone()
        conn.close()

        columns = ['id', 'name', 'phone', 'email', 'address', 'date_registered']
        return db.row_to_dict(customer, columns)

    @staticmethod
    def create(name, phone='', email='', address=''):
        conn = db.get_connection()
        c = conn.cursor()
        c.execute('''INSERT INTO customers (name, phone, email, address, date_registered)
                     VALUES (?, ?, ?, ?, ?)''',
                  (name, phone, email, address, date.today()))
        customer_id = c.lastrowid
        conn.commit()
        conn.close()
        return customer_id

    @staticmethod
    def get_purchases(customer_id):
        conn = db.get_connection()
        c = conn.cursor()
        c.execute('''SELECT * FROM outputs 
                     WHERE customer_id = ? 
                     ORDER BY date_sold DESC''', (customer_id,))
        purchases = c.fetchall()
        conn.close()

        columns = ['id', 'product_name', 'quantity', 'unit', 'price_per_unit',
                   'total_revenue', 'customer_id', 'date_sold', 'transport_cost', 'delivery_status']
        return db.rows_to_dict_list(purchases, columns)


class Input:
    @staticmethod
    def get_all():
        conn = db.get_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM inputs ORDER BY date_purchased DESC')
        inputs = c.fetchall()
        conn.close()

        columns = ['id', 'item_name', 'category', 'quantity', 'unit',
                   'cost_per_unit', 'total_cost', 'supplier', 'date_purchased']
        return db.rows_to_dict_list(inputs, columns)

    @staticmethod
    def create(item_name, category='', quantity=0, unit='', cost_per_unit=0, supplier=''):
        total_cost = quantity * cost_per_unit

        conn = db.get_connection()
        c = conn.cursor()
        c.execute('''INSERT INTO inputs (item_name, category, quantity, unit, cost_per_unit, total_cost, supplier, date_purchased)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                  (item_name, category, quantity, unit, cost_per_unit, total_cost, supplier, date.today()))
        input_id = c.lastrowid
        conn.commit()
        conn.close()
        return input_id, total_cost


class Output:
    @staticmethod
    def get_all():
        conn = db.get_connection()
        c = conn.cursor()
        c.execute('''SELECT o.*, c.name as customer_name 
                     FROM outputs o 
                     LEFT JOIN customers c ON o.customer_id = c.id 
                     ORDER BY o.date_sold DESC''')
        outputs = c.fetchall()
        conn.close()

        columns = ['id', 'product_name', 'quantity', 'unit', 'price_per_unit', 'total_revenue',
                   'customer_id', 'date_sold', 'transport_cost', 'delivery_status', 'customer_name']
        return db.rows_to_dict_list(outputs, columns)

    @staticmethod
    def create(product_name, quantity, unit='', price_per_unit=0, customer_id=None, transport_cost=0):
        total_revenue = quantity * price_per_unit

        conn = db.get_connection()
        c = conn.cursor()
        c.execute('''INSERT INTO outputs (product_name, quantity, unit, price_per_unit, total_revenue, customer_id, date_sold, transport_cost)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                  (product_name, quantity, unit, price_per_unit, total_revenue, customer_id, date.today(),
                   transport_cost))
        output_id = c.lastrowid
        conn.commit()
        conn.close()
        return output_id, total_revenue

    @staticmethod
    def update_delivery_status(output_id, status):
        conn = db.get_connection()
        c = conn.cursor()
        c.execute('UPDATE outputs SET delivery_status = ? WHERE id = ?', (status, output_id))
        rows_affected = c.rowcount
        conn.commit()
        conn.close()
        return rows_affected > 0


class Message:
    @staticmethod
    def get_all():
        conn = db.get_connection()
        c = conn.cursor()
        c.execute('''SELECT m.*, c.name as customer_name, c.phone 
                     FROM messages m 
                     LEFT JOIN customers c ON m.customer_id = c.id 
                     ORDER BY m.date_sent DESC''')
        messages = c.fetchall()
        conn.close()

        columns = ['id', 'customer_id', 'message', 'message_type', 'date_sent', 'customer_name', 'phone']
        return db.rows_to_dict_list(messages, columns)

    @staticmethod
    def create(customer_id, message, message_type='General'):
        conn = db.get_connection()
        c = conn.cursor()
        c.execute('''INSERT INTO messages (customer_id, message, message_type, date_sent)
                     VALUES (?, ?, ?, ?)''',
                  (customer_id, message, message_type, datetime.now()))
        message_id = c.lastrowid
        conn.commit()
        conn.close()
        return message_id


class Dashboard:
    @staticmethod
    def get_stats():
        conn = db.get_connection()
        c = conn.cursor()

        c.execute('SELECT SUM(total_cost) FROM inputs')
        total_inputs = c.fetchone()[0] or 0

        c.execute('SELECT SUM(total_revenue) FROM outputs')
        total_revenue = c.fetchone()[0] or 0

        c.execute('SELECT SUM(transport_cost) FROM outputs')
        total_transport = c.fetchone()[0] or 0

        c.execute('SELECT COUNT(*) FROM customers')
        total_customers = c.fetchone()[0] or 0

        conn.close()

        net_profit = total_revenue - total_inputs - total_transport

        return {
            'total_inputs': float(total_inputs),
            'total_revenue': float(total_revenue),
            'total_transport': float(total_transport),
            'total_customers': int(total_customers),
            'net_profit': float(net_profit)
        }

    @staticmethod
    def get_financial_summary(start_date=None, end_date=None):
        conn = db.get_connection()
        c = conn.cursor()

        # Base queries
        input_query = 'SELECT SUM(total_cost) FROM inputs'
        output_query = 'SELECT SUM(total_revenue), SUM(transport_cost) FROM outputs'

        # Add date filters if provided
        if start_date and end_date:
            input_query += ' WHERE date_purchased BETWEEN ? AND ?'
            output_query += ' WHERE date_sold BETWEEN ? AND ?'
            c.execute(input_query, (start_date, end_date))
        else:
            c.execute(input_query)

        total_expenses = c.fetchone()[0] or 0

        if start_date and end_date:
            c.execute(output_query, (start_date, end_date))
        else:
            c.execute(output_query)

        result = c.fetchone()
        total_revenue = result[0] or 0
        total_transport = result[1] or 0

        conn.close()

        net_profit = total_revenue - total_expenses - total_transport
        profit_margin = (net_profit / total_revenue * 100) if total_revenue > 0 else 0

        return {
            'total_revenue': float(total_revenue),
            'total_expenses': float(total_expenses),
            'total_transport': float(total_transport),
            'net_profit': float(net_profit),
            'profit_margin': round(profit_margin, 2),
            'period': {
                'start_date': start_date,
                'end_date': end_date
            }
        }