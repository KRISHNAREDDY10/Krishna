from Products import Product
from Customers import Customer
from Orders import Order
from ECommerce import ECommerce
def initialize_platform(platform):
        initial_products = [
            Product("1", "Laptop", 10000.00, 50),
            Product("2", "Smartphone", 5000.00, 100),
            Product("3", "Headphones", 1500.00, 200),
            Product("4", "Smartwatch", 1250.00, 150),
            Product("5", "Tablet", 100.00, 100)
        ]
        for product in initial_products:
            platform.add_product(product)

def initialize_customers(platform):
        initial_customers = [
            Customer("1", "Krishna", 1234567890, "krishna@gmail.com", "Nellore,AP"),
            Customer("2", "Narasimha", 1234567891, "narasimha@gmail.com", "Delhi,UP"),
            Customer("3", "Akhil", 1234567892, "aakhil@gmail.com", "Madhapur,TG"),
            Customer("4", "Ashiq", 1234567893, "ashiq@gmail.com", "Atmakur,AP"),
        ]
        for customer in initial_customers:
            platform.add_customer(customer)

def main():
    platform = ECommerce()
    initialize_platform(platform)
    initialize_customers(platform)

    while True:
        if platform.login_user is None:
            platform.login()
        else:
            print("\nE-Commerce Management System")
            print("1. Add Product")
            print("2. View Products")
            print("3. View Customers")
            print("4. View Orders")
            print("5. Create Order")
            print("6. Return Order")
            print("7. Customer Logout")
            print("0. Exit")

            choice = input("Enter choice: ")

            if choice == '1':
                product_id = platform.new_product_id()
                product_name = input("Enter product name: ")
                selling_price = float(input("Enter product price: "))
                inventory = int(input("Enter products in inventory: "))
                product = Product(product_id, product_name, selling_price, inventory)
                platform.add_product(product)
                print("Product added successfully!")

            elif choice == '2':
                platform.c.execute("SELECT * FROM products")
                products = platform.c.fetchall()
                print("Products:")
                for product in products:
                    print(product)

            elif choice == '3':
                platform.c.execute("SELECT * FROM customers")
                customers = platform.c.fetchall()
                print("Customers:")
                for customer in customers:
                    print(customer)

            elif choice == '4':
                platform.c.execute("SELECT * FROM orders")
                orders = platform.c.fetchall()
                print("Orders:")
                for order in orders:
                    print(order)

            elif choice == '5':
                order_id = platform.new_order_id()
                customer_id = input("Enter customer ID: ")
                product_id = input("Enter product ID: ")
                quantity = int(input("Enter quantity: "))
                platform.create_order(customer_id, product_id, quantity)

            elif choice == '6':
                order_id = int(input("Enter order ID to return: "))
                platform.return_order(order_id)

            elif choice == '7':
                platform.logout()
                
            elif choice == '0':
                print("Thanks for using the E-Commerce Management System!")
                print("             HAVE A NICE DAY!")
                break

            else:
                print("Invalid choice, please try again.")
                
    return platform.login()

if __name__ == "__main__":
    main()