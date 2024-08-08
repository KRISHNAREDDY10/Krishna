class Order:
    def __init__(self,order_id,customer, product, quantity):
        self.order_id = order_id
        self.customer = customer.customer_name
        self.product = product.product_name
        self.quantity = quantity 
        self.total_price = product.selling_price * quantity


    def __str__(self):
        return (f"        Orders\n"
                
                f"order_id={self.order_id}\n"

                f"customer={self.customer}\n"

                f"product={self.product}\n"

                f"quantity={self.quantity},\n"

                f"total_price={self.total_price}")
