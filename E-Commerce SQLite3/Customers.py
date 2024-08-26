import sqlite3

conn = sqlite3.connect('E-Commerce.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL,
    address TEXT NOT NULL
)
''')


class Customer:
    def __init__(self,customer_id,customer_name,phone,email,address):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.phone = phone
        self.email = email 
        self.address = address
        self.order = {}

    def save_to_db(self):
        try:
            if self.customer_id is None:
                c.execute("""
                        INSERT INTO Customer (customer_name, phone, email, address) 
                        VALUES (?,?,?)""",
                        (self.customer_name,self.phone,self.email,self.address))
                self.customer_id = c.lastrowid
            else:
                c.execute("""
                        INSERT INTO Customer (customer_name, phone, email, address) 
                        VALUES (?,?,?)""",
                        (self.customer_name,self.phone,self.email,self.address,self.customer_id))
                
                conn.commit()
                print(f"Customer with id {self.customer_id} updated successfully")

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def from_db(customer_data):
        # Assuming that the inventory is stored in the same list as the other customer data
        return Customer(customer_data[0], customer_data[1], customer_data[2], customer_data[3], customer_data[4])