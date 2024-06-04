import sqlite3

class GMS:

    def __init__(self):
        self.conn = None
        self.cur = None
        self.err = ""

    def ConnectDB(self):
        try:
            self.conn = sqlite3.connect("gms.db")
            self.cur = self.conn.cursor()
            return "\n>>> Connected to database and Cursor created successfully <<<\n"
        except sqlite3.Error as e:
            self.err = "\n!!! There was an error establishing connection to the database: " + str(e) + " !!!\n"
            return self.err

    def CreateTable(self):
        try:
            customer_sql = """
                CREATE TABLE IF NOT EXISTS customer (
                    billno INTEGER PRIMARY KEY, 
                    date TEXT, 
                    name TEXT, 
                    no INTEGER
                )"""
            self.cur.execute(customer_sql)
            
            items_sql = """
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    billno INTEGER,
                    productname TEXT,
                    price INTEGER,
                    qty INTEGER,
                    FOREIGN KEY (billno) REFERENCES customer(billno)
                )"""
            self.cur.execute(items_sql)
            return "\n>>> Tables created or opened (if already existing) successfully <<<\n"
        except sqlite3.Error as e:
            self.err = "\n!!! There was an error creating the tables: " + str(e) + " !!!\n"
            self.CloseDB()
            return self.err

    def Save_details(self, b, d, n, no):
        try:
            sql = "INSERT INTO customer (billno, date, name, no) VALUES (?, ?, ?, ?)"
            self.cur.execute(sql, (b, d, n, no))
            self.conn.commit()
            return "\n>>> Customer details added successfully <<<\n"
        except sqlite3.Error as e:
            self.err = "\n!!! There was an error inserting customer details into database: " + str(e) + " !!!\n"
            self.CloseDB()
            return self.err

    def AddItem(self, b, pron, p, q):
        try:
            sql = "INSERT INTO items (billno, productname, price, qty) VALUES (?, ?, ?, ?)"
            self.cur.execute(sql, (b, pron, p, q))
            self.conn.commit()
            return "\n>>> Item added successfully <<<\n"
        except sqlite3.Error as e:
            self.err = "\n!!! There was an error inserting item into database: " + str(e) + " !!!\n"
            self.CloseDB()
            return self.err

    def DeleteItem(self, b):
        try:
            sql = "DELETE FROM items WHERE billno = ?"
            self.cur.execute(sql, (b,))
            self.conn.commit()
            if self.conn.total_changes > 0:
                return "\n>>> Item deleted successfully <<<\n"
            else:
                return "\n!!! No item to delete - check if the bill no is correct !!!\n"
        except sqlite3.Error as e:
            self.err = "\n!!! There was an error deleting item from database: " + str(e) + " !!!\n"
            self.CloseDB()
            return self.err

    def GenerateBill(self, b):
        try:
            sql = """
            SELECT customer.billno, customer.date, customer.name, customer.no, items.productname, items.price, items.qty 
            FROM customer 
            LEFT JOIN items ON customer.billno = items.billno 
            WHERE customer.billno = ?"""
            self.cur.execute(sql, (b,))
            rows = self.cur.fetchall()
            if rows:
                bill = {
                    'bill_no': b,
                    'date': rows[0][1],
                    'customer_name': rows[0][2],
                    'customer_no': rows[0][3],
                    'items': [],
                    'total_price': 0
                }
                total_price = 0
                for row in rows:
                    item = {
                        'product_name': row[4],
                        'price': row[5],
                        'quantity': row[6]
                    }
                    total_price += row[5] * row[6]
                    bill['items'].append(item)
                bill['total_price'] = total_price
                return bill
            else:
                return "\n!!! There are no items in the bill with the given bill number !!!\n"
        except sqlite3.Error as e:
            self.err = "\n!!! There was an error retrieving items from the bill: " + str(e) + " !!!\n"
            self.CloseDB()
            return self.err

    def CloseDB(self):
        try:
            if self.conn:
                self.conn.close()
                return "\n>>> Database connection closed successfully <<<\n"
        except sqlite3.Error as e:
            self.err = "\n!!! There was an error closing the database: " + str(e) + " !!!\n"
            return self.err
