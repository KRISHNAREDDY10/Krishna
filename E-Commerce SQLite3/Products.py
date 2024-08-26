import sqlite3

conn = sqlite3.connect('E-Commerce.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    selling_price REAL NOT NULL,
    inventory INTEGER NOT NULL
)
''')

class Product:
    def __init__(self, product_id, product_name, selling_price, inventory):
        self.product_id = product_id
        self.product_name = product_name
        self.selling_price = selling_price
        self.inventory = inventory

    def save_to_db(self):
        try:
            if self.product_id is None:
                c.execute("""
                        INSERT INTO products (product_name,selling_price,inventory) 
                        VALUES (?,?,?)""",
                        (self.product_name, self.selling_price, self.inventory))
                self.product_id = c.lastrowid
            else:
                c.execute("""
                        INSERT INTO Product (product_name, selling_price, inventory)
                        values (?,?,?,)""",
                        (self.product_name, self.selling_price, self.inventory, self.product_id))
                
                conn.commit()
                print(f"Product with id {self.product_id} updated successfully")

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def from_db(product_data):
        # Assuming that the inventory is stored in the same list as the other product data
        return Product(product_data[0], product_data[1], product_data[2], product_data[3])