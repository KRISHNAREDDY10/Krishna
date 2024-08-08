class Customer:
    def __init__(self,customer_id,customer_name,phone,email,address):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.phone = phone
        self.email = email 
        self.address = address
        self.order = {}

    def add_order(self, order):
        self.order[order.order_id] = order

    def remove_order(self, order_id):
        if order_id in self.order:
            del self.order[order_id]

    def __str__(self):
        return (f"        Customers\n"
                
                f"customer_id = {self.customer_id},\n"

                f"name = {self.customer_name},\n"

                f"phone = {self.phone},\n"

                f"email = {self.email},\n"

                f"address = {self.address}")