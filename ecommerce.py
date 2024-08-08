from customer import Customer
class ECommerce:
    def __init__(self):
        self.products = {}
        self.customers = {}
        self.orders = {} 
        self.quantity = True
        self.login_user = None
        self.order_id = 1
        self.product_id = 1

    def add_product(self, product):
        self.products[product.product_id] = product

    def new_product_id(self):
        product_id = self.product_id
        self.product_id += 1
        return product_id
    

    def add_customer(self, customer):
        self.customers[customer.customer_id] = customer
    def login(self):
        while True:
            print("\n  ***  Customer Login  ***")
            print("1. Login")
            print("2. Create new Customer")
            print("3. View existing Customers")
            print("4. Exit")
            choice = input("Enter choice: ")
            if choice == '1':
               if choice == '1':
                customer_id = input("Enter your Customer ID: ")
                if customer_id in self.customers:
                    self.login_user = self.customers[customer_id]
                    print(f"Logged in as {self.login_user.customer_name}")
                    return
                else:
                    print("Customer ID not found. Please try again.")
            elif choice == '2':
                max_id = max(int(customer_id) for customer_id in self.customers.keys())
                new_customer_id = str(max_id + 1)
                name = input("Enter your Name: ")
                phone = int(input("Enter your Phone Number: "))
                email = input("Enter your Email: ")
                address = input("Enter your Address: ")
                new_customer = Customer(new_customer_id, name, phone , email, address)
                self.add_customer(new_customer)
                print(f"Account created successfully! Your Customer ID is {new_customer_id}.")
                self.login_user = new_customer
                return 
            elif choice == '3':
                if not self.customers:
                    print("No customers found.")
                else:
                   print("---     List of existing customers     ---")
                   for customer_id, customer in self.customers.items():
                      print(f"Customer ID: {customer_id}, Name: {customer.customer_name}, Email: {customer.email}, Address: {customer.address}")
            elif choice == '4':
                print("Logged out from the page. Visit Again 😊!")
                return None
            else:
                print("Invalid choice. Please choose above options.")
       
    def logout(self):
        self.login_user = None
        print("Logged out Successfully")


    def create_order(self, order):
        if order.product.product_id not in self.products:
            print("Product not found!")
            return
        if order.customer.customer_id not in self.customers:
            print("Customer not found!")
            return
        if self.products[order.product.product_id].inventory < order.quantity:
            print("Insufficient product!")
            return

        self.products[order.product.product_id].update_inventory(-order.quantity)
        self.orders[order.order_id] = order
        if order.customer.customer_id in self.customers:
            self.customers[order.customer.customer_id].add_order(order)

    def new_order_id(self):
        order_id = self.order_id
        self.order_id += 1
        return order_id

    def return_order(self, order_id):
        for customer in self.customers.values():
            if order_id in customer.orders:
                order = customer.orders[order_id]
                self.products[order.product.product_id].update_inventory(order.quantity)
                customer.remove_order(order_id)
                del self.orders[order_id]
                print(f"Order {order_id} returned successfully!")
                return
        print("Order not found or you are not logged in!")
    def __str__(self):
        return (f"ECommerce(\nProducts: {[str(p) for p in self.products.values()]}, "     
                f"\nCustomers: {[str(c) for c in self.customers.values()]}, "
                f"\nOrders: {[str(o) for o in self.orders.values()]})")
