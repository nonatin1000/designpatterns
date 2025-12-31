"""Examples demonstrating the Facade pattern for sales system.

These examples show how the SalesFacade simplifies interaction with
the complex sales subsystem (Order, Payment, Email).
"""

from customer import Customer
from product import Product
from sales_facade import SalesFacade


def example_without_facade():
    """Example 1: Processing order WITHOUT Facade (complex).

    This shows how complex it is to interact directly with the subsystem.
    The client needs to know about Order, Payment, and Email classes.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Order Processing WITHOUT Facade (Complex)")
    print("=" * 80)

    from order import Order
    from payment import CreditCardPayment
    from email_service import OrderEmail

    # Create customer
    customer = Customer("Luiz da Silva", "12345678910", "luiz@email.com")

    # Create products
    product1 = Product("Pink Blouse", "Women's pink blouse", 80.99)
    product2 = Product("Black T-Shirt", "Men's black t-shirt", 49.90)
    product3 = Product("Jeans", "Men's jeans pants", 119.90)

    print("\nClient must manually:")
    print("  1. Create Order")
    print("  2. Add products to Order")
    print("  3. Create Payment")
    print("  4. Process payment")
    print("  5. Create Email service")
    print("  6. Send email")
    print()

    # Client needs to know about Order class
    order = Order(customer)
    order.add_product(product1)
    order.add_product(product2)
    order.add_product(product3)

    # Client needs to know about Payment classes
    payment = CreditCardPayment(order)
    email = OrderEmail(order)

    # Client needs to handle payment and email logic
    if payment.process_payment():
        email.send_payment_success_email("Credit Card")
    else:
        email.send_payment_failure_email("Credit Card")

    print("\n[RESULT] Order processed but client code is complex!")
    print()


def example_with_facade():
    """Example 2: Processing order WITH Facade (simple).

    This shows how the Facade simplifies the same process.
    The client only needs to know about the SalesFacade.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Order Processing WITH Facade (Simple)")
    print("=" * 80)

    # Create customer
    customer = Customer("Luiz da Silva", "12345678910", "luiz@email.com")

    # Create products
    product1 = Product("Pink Blouse", "Women's pink blouse", 80.99)
    product2 = Product("Black T-Shirt", "Men's black t-shirt", 49.90)
    product3 = Product("Jeans", "Men's jeans pants", 119.90)

    print("\nUsing Facade - Client only needs:")
    print("  1. Create SalesFacade")
    print("  2. Add products")
    print("  3. Call process_credit_card_order()")
    print()

    # Create facade (automatically creates Order and Email)
    facade = SalesFacade(customer)

    # Add products through facade
    facade.add_product(product1)
    facade.add_product(product2)
    facade.add_product(product3)

    # Process payment (automatically handles Payment and Email)
    facade.process_credit_card_order()

    print("\n[RESULT] Much simpler! Facade handles all complexity!")
    print()


def example_credit_card_payment():
    """Example 3: Complete credit card payment flow."""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Credit Card Payment Flow")
    print("=" * 80)

    customer = Customer("Maria Santos", "98765432100", "maria@email.com")

    product1 = Product("Laptop", "High-performance laptop", 3500.00)
    product2 = Product("Mouse", "Wireless mouse", 89.90)

    facade = SalesFacade(customer)
    facade.add_product(product1)
    facade.add_product(product2)

    print(f"\nOrder Details:")
    print(f"  Customer: {facade.get_customer_name()}")
    print(f"  Products: {facade.get_product_count()} items")
    print(f"  Total: R$ {facade.get_order_total():.2f}")
    print()

    # Process with credit card
    success = facade.process_credit_card_order()

    if success:
        print("[OK] Credit card payment completed successfully!")
    print()


def example_bank_slip_payment():
    """Example 4: Complete bank slip payment flow."""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Bank Slip Payment Flow")
    print("=" * 80)

    customer = Customer("João Silva", "11122233344", "joao@email.com")

    product1 = Product("Smartphone", "Latest model smartphone", 2500.00)

    facade = SalesFacade(customer)
    facade.add_product(product1)

    print(f"\nOrder Details:")
    print(f"  Customer: {facade.get_customer_name()}")
    print(f"  Products: {facade.get_product_count()} items")
    print(f"  Total: R$ {facade.get_order_total():.2f}")
    print()

    # Process with bank slip
    success = facade.process_bank_slip_order()

    if success:
        print("[OK] Bank slip generated successfully!")
    print()


def example_multiple_products():
    """Example 5: Order with multiple products."""
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Order with Multiple Products")
    print("=" * 80)

    customer = Customer("Ana Paula", "55566677788", "ana@email.com")

    facade = SalesFacade(customer)

    # Add multiple products
    products = [
        Product("Dress", "Summer dress", 129.90),
        Product("Sandals", "Beach sandals", 59.90),
        Product("Hat", "Sun hat", 39.90),
        Product("Sunglasses", "UV protection sunglasses", 89.90),
    ]

    print("\nAdding products to order:")
    for product in products:
        facade.add_product(product)
        print(f"  + {product.name} - R$ {product.price:.2f}")

    print(f"\nOrder Summary:")
    print(f"  Total Products: {facade.get_product_count()}")
    print(f"  Total Amount: R$ {facade.get_order_total():.2f}")
    print()

    # Process payment
    facade.process_credit_card_order()

    print("[OK] Order processed successfully!")
    print()


def example_facade_benefits():
    """Example 6: Demonstrating Facade benefits."""
    print("\n" + "=" * 80)
    print("EXAMPLE 6: Facade Pattern Benefits")
    print("=" * 80)

    print("\nBENEFITS OF USING FACADE:")
    print()
    print("1. SIMPLIFIED INTERFACE")
    print("   - Client only interacts with SalesFacade")
    print("   - No need to know about Order, Payment, Email classes")
    print()
    print("2. REDUCED COUPLING")
    print("   - Client is decoupled from subsystem classes")
    print("   - Changes in subsystem don't affect client")
    print()
    print("3. EASE OF USE")
    print("   - Single entry point for complex operations")
    print("   - Less code required from client")
    print()
    print("4. FLEXIBILITY")
    print("   - Client can still access subsystem directly if needed")
    print("   - Facade doesn't restrict access")
    print()

    # Demonstrate with simple code
    customer = Customer("Test User", "00000000000", "test@email.com")
    facade = SalesFacade(customer)

    print("COMPARISON:")
    print()
    print("Without Facade (7+ lines of code):")
    print("  order = Order(customer)")
    print("  order.add_product(product)")
    print("  payment = CreditCardPayment(order)")
    print("  email = OrderEmail(order)")
    print("  if payment.process_payment():")
    print("      email.send_payment_success_email(...)")
    print()
    print("With Facade (3 lines of code):")
    print("  facade = SalesFacade(customer)")
    print("  facade.add_product(product)")
    print("  facade.process_credit_card_order()")
    print()


if __name__ == "__main__":
    print("\n")
    print("=" * 80)
    print(" " * 28 + "FACADE PATTERN - EXAMPLES")
    print(" " * 28 + "Sales System Simplification")
    print("=" * 80)

    example_without_facade()
    example_with_facade()
    example_credit_card_payment()
    example_bank_slip_payment()
    example_multiple_products()
    example_facade_benefits()

    print("=" * 80)
    print("To test the API: python main.py")
    print("Access: http://localhost:8000/docs")
    print("=" * 80 + "\n")
