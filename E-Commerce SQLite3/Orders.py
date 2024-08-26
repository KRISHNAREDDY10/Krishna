import sqlite3

conn = sqlite3.connect('E-Commerce.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    total_price REAL NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
)
''')

class Order:
    def __init__(self,order_id,customer, product, quantity):
        self.order_id = order_id
        self.customer = customer.customer_name
        self.product = product.product_name
        self.quantity = quantity 
        self.total_price = product.selling_price * quantity


    def save_to_db(self):
        try:
            if self.order_id is None:
                c.execute("""
                        INSERT INTO Order (order_id, customer, product, quantity, total_price ) 
                        VALUES (?,?,?)""",
                        (self.order_id, self.customer, self.product, self.quantity, self.total_price))
                self.order_id = c.lastrowid
            else:
                c.execute("""
                        INSERT INTO Order (order_id, customer, product, quantity, total_price) 
                        VALUES (?,?,?)""",
                        (self.order_id, self.customer, self.product, self.quantity, self.total_price))
                
                conn.commit()
                print(f"Order with id {self.order_id} updated successfully")

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def from_db(order_data):
        # Assuming that the inventory is stored in the same list as the other order data
        return Order(order_data[0], order_data[1], order_data[2], order_data[3])
