from abc import ABC, abstractmethod
from typing import Dict


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


# Subclass 3 : Subscription_Product
class SubscriptionProduct(Product):
    """
    Represents recurring software or access services with billing options.
    """

    def __init__(self, product_id: str, name: str, base_price: float, billing_cycle: str):
        super().__init__(product_id, name, base_price)
        self.billing_cycle: str = billing_cycle.lower()  # "monthly" or "annual"

    def calculate_total_price(self) -> float:
        # Apply a 15% discount for annual plans
        if self.billing_cycle == "annual":
            return self.base_price * 12 * 0.85
        return self.base_price

    def fulfill(self) -> str:
        return (
            f"Activated {self.billing_cycle.capitalize()} Subscription for '{self.name}'. "
            f"Auto-renewal scheduled."
        )


# DEMONSTRATION & POLYMORPHISM CHECK

if __name__ == "__main__":
    # Create one instance of each product type
    items: list[Product] = [
        PhysicalProduct("P100", "Gaming Laptop", 1200.00, weight_kg=2.5, stock_quantity=10),
        DigitalProduct("D200", "Python Mastering eBook", 29.99, file_size_mb=15.4, download_url="https://store.com/dl/python-ebook"),
        SubscriptionProduct("S300", "Cloud Storage 1TB", 10.00, billing_cycle="annual"),
    ]

    print("--- DEMONSTRATING POLYMORPHISM ---")
    for item in items:
        print(f"\nItem: {item.name}")
        print(f"Total Computed Price: ${item.calculate_total_price():.2f}")
        print(f"Fulfillment Status:   {item.fulfill()}")



# entity 2 : - Payment gateway    


class PaymentGateway(ABC):
    """
    Abstract interface for payment processing.
    Enforces a standard contract for all payment service providers.
    """

    @abstractmethod
    def authorize(self, amount: float) -> bool:
        """Verify funds or account validity before capturing payment."""
        pass

    @abstractmethod
    def process_payment(self, amount: float) -> str:
        """Capture the funds and return a transaction reference ID."""
        pass

    @abstractmethod
    def refund(self, transaction_id: str, amount: float) -> bool:
        """Reverse a completed transaction."""
        pass



class CreditCardGateway(PaymentGateway):
    """
    Handles secure credit card transactions via third-party bank APIs.
    """

    def __init__(self, card_number: str, cvv: str):
        # Mask card number for security logging
        self.masked_card: str = f"****-****-****-{card_number[-4:]}"
        self.cvv: str = cvv

    def authorize(self, amount: float) -> bool:
        print(f"[CreditCard] Authorizing ${amount:.2f} on card {self.masked_card}...")
        # Mock validation check
        return len(self.cvv) == 3

    def process_payment(self, amount: float) -> str:
        print(f"[CreditCard] Processing payment of ${amount:.2f}...")
        # Returns a mock transaction reference ID
        return "CC_TXN_987654321"

    def refund(self, transaction_id: str, amount: float) -> bool:
        print(f"[CreditCard] Refunding ${amount:.2f} for transaction {transaction_id}...")
        return True



class PayPalGateway(PaymentGateway):
    """
    Handles transactions via PayPal API tokens and user emails.
    """

    def __init__(self, paypal_email: str):
        self.paypal_email: str = paypal_email

    def authorize(self, amount: float) -> bool:
        print(f"[PayPal] Verifying account {self.paypal_email} for ${amount:.2f}...")
        return "@" in self.paypal_email

    def process_payment(self, amount: float) -> str:
        print(f"[PayPal] Executing instant transfer of ${amount:.2f} from {self.paypal_email}...")
        return "PP_TXN_123456789"

    def refund(self, transaction_id: str, amount: float) -> bool:
        print(f"[PayPal] Issuing refund of ${amount:.2f} to {self.paypal_email}...")
        return True


# entity 3 :- Customer and Shopping Cart




class Customer:
    """
    Represents a registered buyer in the e-commerce system.
    """

    def __init__(self, customer_id: str, name: str, email: str):
        self.customer_id: str = customer_id
        self.name: str = name
        self.email: str = email

    def __str__(self) -> str:
        return f"Customer: {self.name} ({self.email})"



class Cart:
    """
    Manages a temporary collection of products selected by a customer prior to checkout.
    """

    def __init__(self, customer: Customer):
        self.customer: Customer = customer
        # Maps product_id to a dictionary containing the product object and its quantity
        self._items: Dict[str, dict] = {}

    def add_item(self, product: Product, quantity: int = 1) -> None:
        """Adds a product to the cart or increases quantity if already present."""
        if product.product_id in self._items:
            self._items[product.product_id]["quantity"] += quantity
        else:
            self._items[product.product_id] = {
                "product": product,
                "quantity": quantity
            }
        print(f"Added {quantity}x '{product.name}' to {self.customer.name}'s cart.")

    def remove_item(self, product_id: str) -> None:
        """Removes a product completely from the cart."""
        if product_id in self._items:
            removed = self._items.pop(product_id)
            print(f"Removed '{removed['product'].name}' from cart.")
        else:
            print("Product ID not found in cart.")

    def get_subtotal(self) -> float:
        """Calculates total cost of all items in the cart (including category fees)."""
        subtotal = 0.0
        for item_data in self._items.values():
            product: Product = item_data["product"]
            qty: int = item_data["quantity"]
            subtotal += product.calculate_total_price() * qty
        return subtotal

    def get_items_summary(self) -> list[dict]:
        """Returns a list of items currently in the cart."""
        return list(self._items.values())

    def clear(self) -> None:
        """Empties the cart after checkout."""
        self._items.clear()

    def __str__(self) -> str:
        return f"Cart for {self.customer.name}: {len(self._items)} unique items, Subtotal: ${self.get_subtotal():.2f}"