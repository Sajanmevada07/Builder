from abc import ABC, abstractmethod


#Base Class


class Product(ABC):


    def __init__(self, product_id: str, name: str, base_price: float):
        self.product_id: str = product_id
        self.name: str = name
        self.base_price: float = base_price

    @abstractmethod
    def calculate_total_price(self) -> float:
        """Calculate final price including category-specific fees/discounts."""
        pass

    @abstractmethod
    def fulfill(self) -> str:
        """Execute the delivery/fulfillment workflow for the customer."""
        pass

    def __str__(self) -> str:
        return f"[{self.product_id}] {self.name} - Base Price: ${self.base_price:.2f}"



#Subclass 1 - Physical_product

class PhysicalProduct(Product):
    """
    Represents tangible goods that require inventory tracking and shipping.
    """

    def __init__(self, product_id: str, name: str, base_price: float, weight_kg: float, stock_quantity: int):
        super().__init__(product_id, name, base_price)
        self.weight_kg: float = weight_kg
        self.stock_quantity: int = stock_quantity

    def calculate_total_price(self) -> float:
        # Calculates shipping fee at $5.00 per kg
        shipping_fee = self.weight_kg * 5.0
        return self.base_price + shipping_fee

    def fulfill(self) -> str:
        if self.stock_quantity <= 0:
            raise ValueError(f"Fulfillment failed: '{self.name}' is out of stock.")
        
        self.stock_quantity -= 1
        return (
            f"Package dispatched for '{self.name}' (Weight: {self.weight_kg}kg). "
            f"Remaining inventory: {self.stock_quantity} units."
        )


# Subclass 2 : Digital_product

class DigitalProduct(Product):
    """
    Represents downloadable goods with no shipping costs or inventory limits.
    """

    def __init__(self, product_id: str, name: str, base_price: float, file_size_mb: float, download_url: str):
        super().__init__(product_id, name, base_price)
        self.file_size_mb: float = file_size_mb
        self.download_url: str = download_url

    def calculate_total_price(self) -> float:
        # Digital goods have zero shipping cost
        return self.base_price

    def fulfill(self) -> str:
        return (
            f"Generated single-use download link for '{self.name}' "
            f"({self.file_size_mb} MB): {self.download_url}"
        )

