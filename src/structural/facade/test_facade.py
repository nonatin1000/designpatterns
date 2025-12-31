"""Unit tests for the Facade pattern implementation."""

from customer import Customer
from product import Product
from order import Order
from payment import CreditCardPayment, BankSlipPayment
from email_service import OrderEmail
from sales_facade import SalesFacade


def test_customer_creation():
    """Test that Customer is created correctly."""
    customer = Customer("John Doe", "12345678910", "john@email.com")

    assert customer.name == "John Doe"
    assert customer.tax_id == "12345678910"
    assert customer.email == "john@email.com"
    print("[OK] Test Customer Creation: PASSED")


def test_product_creation():
    """Test that Product is created correctly."""
    product = Product("Test Product", "Test description", 99.99)

    assert product.name == "Test Product"
    assert product.description == "Test description"
    assert product.price == 99.99
    print("[OK] Test Product Creation: PASSED")


def test_order_creation():
    """Test that Order is created with customer."""
    customer = Customer("Jane Doe", "98765432100", "jane@email.com")
    order = Order(customer)

    assert order.customer.name == "Jane Doe"
    assert order.get_product_count() == 0
    assert order.get_total() == 0.0
    print("[OK] Test Order Creation: PASSED")


def test_order_add_products():
    """Test adding products to order."""
    customer = Customer("Test User", "11111111111", "test@email.com")
    order = Order(customer)

    product1 = Product("Product 1", "Description 1", 10.00)
    product2 = Product("Product 2", "Description 2", 20.00)

    order.add_product(product1)
    order.add_product(product2)

    assert order.get_product_count() == 2
    assert order.get_total() == 30.00
    print("[OK] Test Order Add Products: PASSED")


def test_credit_card_payment():
    """Test credit card payment processing."""
    customer = Customer("Payment Test", "22222222222", "payment@email.com")
    order = Order(customer)
    product = Product("Test Item", "Test", 100.00)
    order.add_product(product)

    payment = CreditCardPayment(order)
    success = payment.process_payment()

    assert success == True
    assert payment.get_payment_amount() == 100.00
    print("[OK] Test Credit Card Payment: PASSED")


def test_bank_slip_payment():
    """Test bank slip payment processing."""
    customer = Customer("Bank Slip Test", "33333333333", "bankslip@email.com")
    order = Order(customer)
    product = Product("Test Item", "Test", 200.00)
    order.add_product(product)

    payment = BankSlipPayment(order)
    success = payment.process_payment()

    assert success == True
    assert payment.get_payment_amount() == 200.00
    print("[OK] Test Bank Slip Payment: PASSED")


def test_email_service():
    """Test email sending functionality."""
    customer = Customer("Email Test", "44444444444", "emailtest@email.com")
    order = Order(customer)
    product = Product("Test Product", "Test", 50.00)
    order.add_product(product)

    email = OrderEmail(order)
    success = email.send_email("Test message")

    assert success == True
    print("[OK] Test Email Service: PASSED")


def test_facade_creation():
    """Test that SalesFacade creates order and email automatically."""
    customer = Customer("Facade Test", "55555555555", "facade@email.com")
    facade = SalesFacade(customer)

    assert facade.order is not None
    assert facade.email is not None
    assert facade.get_customer_name() == "Facade Test"
    assert facade.get_product_count() == 0
    print("[OK] Test Facade Creation: PASSED")


def test_facade_add_product():
    """Test adding products through facade."""
    customer = Customer("Add Test", "66666666666", "add@email.com")
    facade = SalesFacade(customer)

    product1 = Product("Item 1", "Description 1", 25.00)
    product2 = Product("Item 2", "Description 2", 75.00)

    facade.add_product(product1)
    facade.add_product(product2)

    assert facade.get_product_count() == 2
    assert facade.get_order_total() == 100.00
    print("[OK] Test Facade Add Product: PASSED")


def test_facade_credit_card_order():
    """Test processing credit card order through facade."""
    customer = Customer("CC Test", "77777777777", "cc@email.com")
    facade = SalesFacade(customer)

    product = Product("Test Product", "Test", 150.00)
    facade.add_product(product)

    success = facade.process_credit_card_order()

    assert success == True
    print("[OK] Test Facade Credit Card Order: PASSED")


def test_facade_bank_slip_order():
    """Test processing bank slip order through facade."""
    customer = Customer("Boleto Test", "88888888888", "boleto@email.com")
    facade = SalesFacade(customer)

    product = Product("Test Product", "Test", 250.00)
    facade.add_product(product)

    success = facade.process_bank_slip_order()

    assert success == True
    print("[OK] Test Facade Bank Slip Order: PASSED")


def test_invalid_customer():
    """Test that invalid customer raises ValueError."""
    try:
        customer = Customer("", "12345678910", "test@email.com")
        assert False, "Should have raised ValueError"
    except ValueError:
        print("[OK] Test Invalid Customer: PASSED")


def test_invalid_product():
    """Test that invalid product raises ValueError."""
    try:
        product = Product("Test", "Description", -10.00)
        assert False, "Should have raised ValueError"
    except ValueError:
        print("[OK] Test Invalid Product: PASSED")


def test_order_without_products():
    """Test that payment fails for order without products."""
    customer = Customer("Empty Order", "99999999999", "empty@email.com")
    order = Order(customer)

    try:
        payment = CreditCardPayment(order)
        assert False, "Should have raised ValueError"
    except ValueError:
        print("[OK] Test Order Without Products: PASSED")


def test_facade_simplification():
    """Test that facade simplifies subsystem interaction."""
    # WITHOUT FACADE - many steps
    customer1 = Customer("Without", "11111111111", "without@email.com")
    order = Order(customer1)
    product = Product("Test", "Test", 100.00)
    order.add_product(product)
    payment = CreditCardPayment(order)
    email = OrderEmail(order)
    success1 = payment.process_payment()

    # WITH FACADE - fewer steps
    customer2 = Customer("With", "22222222222", "with@email.com")
    facade = SalesFacade(customer2)
    product2 = Product("Test", "Test", 100.00)
    facade.add_product(product2)
    success2 = facade.process_credit_card_order()

    # Both should succeed, but facade is simpler
    assert success1 == success2 == True
    print("[OK] Test Facade Simplification: PASSED")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("RUNNING FACADE PATTERN TESTS")
    print("=" * 60 + "\n")

    try:
        test_customer_creation()
        test_product_creation()
        test_order_creation()
        test_order_add_products()
        test_credit_card_payment()
        test_bank_slip_payment()
        test_email_service()
        test_facade_creation()
        test_facade_add_product()
        test_facade_credit_card_order()
        test_facade_bank_slip_order()
        test_invalid_customer()
        test_invalid_product()
        test_order_without_products()
        test_facade_simplification()

        print("\n" + "=" * 60)
        print("ALL TESTS PASSED! [OK]")
        print("=" * 60 + "\n")
    except AssertionError as e:
        print(f"\n[ERROR] TEST FAILED: {e}\n")
    except Exception as e:
        print(f"\n[ERROR] ERROR: {e}\n")
