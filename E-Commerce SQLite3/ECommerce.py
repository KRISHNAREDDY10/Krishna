import sqlite3

conn = sqlite3.connect('E-Commerce.db')
c = conn.cursor()

from Customers import Customer

class ECommerce:
    def __init__(self):
        self.conn = sqlite3.connect('E-Commerce.db')
        self.c = self.conn.cursor()
        self.products = {}
        self.customers = {}
        self.orders = {}
        self.order_id = 1
        self.login_user = None
        self.product_id = 1

    def add_product(self, product):
        try:
            self.c.execute("""
                INSERT INTO products (product_id, product_name, selling_price, inventory) VALUES (?, ?, ?, ?)""",
                (product.product_id, product.product_name, product.selling_price, product.inventory))
            self.conn.commit()
            print(f"Product {product.product_id}, {product.product_name} added successfully")
        except sqlite3.Error as e:
            print(f"An error occurred in add_product: {e}")

    def new_product_id(self):
        product_id = self.product_id
        self.product_id += 1
        return product_id

    def add_customer(self, customer):
        try:
            self.c.execute("""
                INSERT INTO customers (customer_id, customer_name, phone, email, address) VALUES (?, ?, ?, ?, ?)""",
                (customer.customer_id, customer.customer_name, customer.phone, customer.email, customer.address))
            self.conn.commit()
            print(f"Customer {customer.customer_id}, {customer.customer_name} added successfully")
        except sqlite3.Error as e:
            print(f"An error occurred in add_customer: {e}")

    def login(self):
        while True:
            print("\n  ***  Customer Login  ***")
            print("1. Login")
            print("2. Create new Customer")
            print("3. View existing Customers")
            print("4. Exit")
            choice = input("Enter choice: ")
            if choice == '1':
                customer_id = input("Enter your customer ID: ")
                self.c.execute("SELECT * FROM customers WHERE customer_id = ?", (customer_id,))
                customer = self.c.fetchone()
                if customer:
                    self.login_user = customer_id       # Assign customer_name from fetched tuple
                    customer_name = customer[1]
                    print(f"{customer_id} , {customer_name} logged in successfully")
                else:
                    print("Customer not found")
            elif choice == '2':
                max_id = self.c.execute("SELECT MAX(customer_id) FROM customers").fetchone()[0]
                new_customer_id = max_id + 1
                customer_name = input("Enter your Name: ")
                phone = int(input("Enter your Phone Number: "))
                email = input("Enter your Email: ")
                address = input("Enter your Address: ")
                new_customer = Customer(new_customer_id, customer_name, phone , email, address)
                self.add_customer(new_customer)
                print(f"Account created successfully! Your Customer ID is {new_customer_id}.")
                self.login_user = new_customer
                return
            elif choice == '3':
                self.c.execute("SELECT * FROM customers")
                customers = self.c.fetchall()
                if not customers:
                    print("No customers found.")
                else:
                    print("---     List of existing customers     ---")
                    for customer in customers:
                        print(f"Customer ID: {customer[0]}, Name: {customer[1]}, Email: {customer[3]}, Address: {customer[4]}")
            elif choice == '4':
                print("Logged out from the page. Visit Again 😊!")
                return None
            else:
                print("Invalid choice. Please choose above options.")

    def logout(self):
        self.login_user = None
        print(f"Customer {self.login_user} logged out. Visit Again 😊!")
        

    def create_order(self, customer_id, product_id, quantity):
        try:
            self.c.execute("SELECT selling_price, inventory FROM products WHERE product_id = ?", (product_id,))
            product = self.c.fetchone()
            if product and product[1] >= quantity:
                total_price = product[0] * quantity
                self.c.execute("""
                    INSERT INTO orders (customer_id, product_id, quantity, total_price) VALUES (?, ?, ?, ?, ?)""",
                    (customer_id, product_id, quantity, total_price))
                self.c.execute("""
                    UPDATE products SET inventory = inventory - ? WHERE product_id = ?""",
                    (quantity, product_id))
                self.conn.commit()
                print(f"Order {self.order_id} added successfully")
                self.order_id += 1
            else:
                print("Insufficient inventory or product not found")
        except sqlite3.Error as e:
            print(f"An error occurred in add_order: {e}")

    def new_order_id(self):
        order_id = self.order_id
        self.order_id += 1
        return order_id

    def return_order(self, order_id):
        try:
            self.c.execute("SELECT product_id, quantity FROM orders WHERE order_id = ?", (order_id,))
            order = self.c.fetchone()
            if order:
                self.c.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))
                self.c.execute("""
                    UPDATE products SET inventory = inventory + ? WHERE product_id = ?""",
                    (order[1], order[0]))
                self.conn.commit()
                print(f"Order {order_id} returned successfully")
            else:
                print("Order not found")
        except sqlite3.Error as e:
            print(f"An error occurred in return_order: {e}")
