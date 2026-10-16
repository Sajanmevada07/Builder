

class product:

    def __init__(self, product_id : str , name: str ,base_price: str ):

        self.productID = product_id
        self.name = name
        self.baseprice = base_price

    def calculate_final_price(self, tax : float , quantity: int):

        self.tax = tax
        self.quantity = quantity

        if self.quantity < 0:
            return False

        return f"final price : {((self.baseprice + (self.baseprice * tax/100))* quantity) }"

    







