"""Comprehensive tests for Facade pattern implementation."""

import sys
from pathlib import Path
from io import StringIO
from contextlib import redirect_stdout

# Add src directory to path for standalone execution
if __name__ == "__main__":
    src_dir = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(src_dir))

try:
    # Try relative imports first
    from .customer import Customer
    from .product import Product
    from .order import Order
    from .payment import Payment, CreditCardPayment, BankSlipPayment
    from .email_service import OrderEmail
    from .sales_facade import SalesFacade
except ImportError:
    # Fall back to direct module imports
    import importlib.util
    import types
    test_dir = Path(__file__).parent
    
    # Create module structure
    structural = types.ModuleType("structural")
    structural_facade = types.ModuleType("structural.facade")
    sys.modules["structural"] = structural
    sys.modules["structural.facade"] = structural_facade
    
    # Load modules in dependency order
    customer_spec = importlib.util.spec_from_file_location(
        "structural.facade.customer",
        test_dir / "customer.py"
    )
    customer_module = importlib.util.module_from_spec(customer_spec)
    sys.modules["structural.facade.customer"] = customer_module
    structural_facade.customer = customer_module
    customer_spec.loader.exec_module(customer_module)
    
    product_spec = importlib.util.spec_from_file_location(
        "structural.facade.product",
        test_dir / "product.py"
    )
    product_module = importlib.util.module_from_spec(product_spec)
    sys.modules["structural.facade.product"] = product_module
    structural_facade.product = product_module
    product_spec.loader.exec_module(product_module)
    
    order_spec = importlib.util.spec_from_file_location(
        "structural.facade.order",
        test_dir / "order.py"
    )
    order_module = importlib.util.module_from_spec(order_spec)
    sys.modules["structural.facade.order"] = order_module
    structural_facade.order = order_module
    order_spec.loader.exec_module(order_module)
    
    payment_spec = importlib.util.spec_from_file_location(
        "structural.facade.payment",
        test_dir / "payment.py"
    )
    payment_module = importlib.util.module_from_spec(payment_spec)
    sys.modules["structural.facade.payment"] = payment_module
    structural_facade.payment = payment_module
    payment_spec.loader.exec_module(payment_module)
    
    email_service_spec = importlib.util.spec_from_file_location(
        "structural.facade.email_service",
        test_dir / "email_service.py"
    )
    email_service_module = importlib.util.module_from_spec(email_service_spec)
    sys.modules["structural.facade.email_service"] = email_service_module
    structural_facade.email_service = email_service_module
    email_service_spec.loader.exec_module(email_service_module)
    
    sales_facade_spec = importlib.util.spec_from_file_location(
        "structural.facade.sales_facade",
        test_dir / "sales_facade.py"
    )
    sales_facade_module = importlib.util.module_from_spec(sales_facade_spec)
    sys.modules["structural.facade.sales_facade"] = sales_facade_module
    structural_facade.sales_facade = sales_facade_module
    sales_facade_spec.loader.exec_module(sales_facade_module)
    
    # Extract classes
    Customer = customer_module.Customer
    Product = product_module.Product
    Order = order_module.Order
    Payment = payment_module.Payment
    CreditCardPayment = payment_module.CreditCardPayment
    BankSlipPayment = payment_module.BankSlipPayment
    OrderEmail = email_service_module.OrderEmail
    SalesFacade = sales_facade_module.SalesFacade


def test_customer_creation():
    """Test customer creation and validation."""
    customer = Customer("John Silva", "12345678900", "john@email.com")
    
    assert customer.name == "John Silva"
    assert customer.tax_id == "12345678900"
    assert customer.email == "john@email.com"
    
    print("[OK] Test Customer Creation: PASSED")


def test_customer_validation():
    """Test customer validation."""
    try:
        Customer("", "123", "email@test.com")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    try:
        Customer("Name", "", "email@test.com")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    try:
        Customer("Name", "123", "invalid-email")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    print("[OK] Test Customer Validation: PASSED")


def test_product_creation():
    """Test product creation."""
    product = Product("Notebook", "High performance laptop", 2500.00)
    
    assert product.name == "Notebook"
    assert product.description == "High performance laptop"
    assert product.price == 2500.00
    
    print("[OK] Test Product Creation: PASSED")


def test_product_validation():
    """Test product validation."""
    try:
        Product("", "Description", 100.0)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    try:
        Product("Name", "", 100.0)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    try:
        Product("Name", "Description", -100.0)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    try:
        Product("Name", "Description", 0.0)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    print("[OK] Test Product Validation: PASSED")


def test_order_creation():
    """Test order creation."""
    customer = Customer("John Silva", "12345678900", "john@email.com")
    order = Order(customer)
    
    assert order.customer == customer
    assert order.get_product_count() == 0
    assert order.get_total() == 0.0
    
    print("[OK] Test Order Creation: PASSED")


def test_order_add_product():
    """Test adding products to order."""
    customer = Customer("John Silva", "12345678900", "john@email.com")
    order = Order(customer)
    product = Product("Notebook", "Laptop", 2500.00)
    
    order.add_product(product)
    
    assert order.get_product_count() == 1
    assert order.get_total() == 2500.00
    
    print("[OK] Test Order Add Product: PASSED")


def test_order_multiple_products():
    """Test order with multiple products."""
    customer = Customer("John Silva", "12345678900", "john@email.com")
    order = Order(customer)
    
    product1 = Product("Notebook", "Laptop", 2500.00)
    product2 = Product("Mouse", "Wireless mouse", 50.00)
    
    order.add_product(product1)
    order.add_product(product2)
    
    assert order.get_product_count() == 2
    assert order.get_total() == 2550.00
    
    print("[OK] Test Order Multiple Products: PASSED")


def test_facade_initialization():
    """Test SalesFacade initialization."""
    customer = Customer("John Silva", "12345678900", "john@email.com")
    facade = SalesFacade(customer)
    
    assert facade.get_customer_name() == "John Silva"
    assert facade.get_product_count() == 0
    assert facade.get_order_total() == 0.0
    
    print("[OK] Test Facade Initialization: PASSED")


def test_facade_add_product():
    """Test facade add_product method."""
    customer = Customer("John Silva", "12345678900", "john@email.com")
    facade = SalesFacade(customer)
    product = Product("Notebook", "Laptop", 2500.00)
    
    facade.add_product(product)
    
    assert facade.get_product_count() == 1
    assert facade.get_order_total() == 2500.00
    
    print("[OK] Test Facade Add Product: PASSED")


def test_facade_process_credit_card_order():
    """Test facade process_credit_card_order method."""
    customer = Customer("John Silva", "12345678900", "john@email.com")
    facade = SalesFacade(customer)
    product = Product("Notebook", "Laptop", 2500.00)
    
    facade.add_product(product)
    
    f = StringIO()
    with redirect_stdout(f):
        success = facade.process_credit_card_order()
    
    assert success is True
    output = f.getvalue()
    assert "CreditCardPayment" in output or "credit card" in output.lower()
    assert "EMAIL SENT" in output
    
    print("[OK] Test Facade Process Credit Card Order: PASSED")


def test_facade_process_bank_slip_order():
    """Test facade process_bank_slip_order method."""
    customer = Customer("John Silva", "12345678900", "john@email.com")
    facade = SalesFacade(customer)
    product = Product("Notebook", "Laptop", 2500.00)
    
    facade.add_product(product)
    
    f = StringIO()
    with redirect_stdout(f):
        success = facade.process_bank_slip_order()
    
    assert success is True
    output = f.getvalue()
    assert "BankSlipPayment" in output or "bank slip" in output.lower()
    assert "EMAIL SENT" in output
    
    print("[OK] Test Facade Process Bank Slip Order: PASSED")


def test_facade_empty_order_validation():
    """Test facade validates empty order."""
    customer = Customer("John Silva", "12345678900", "john@email.com")
    facade = SalesFacade(customer)
    
    try:
        facade.process_credit_card_order()
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "products" in str(e).lower()
    
    try:
        facade.process_bank_slip_order()
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "products" in str(e).lower()
    
    print("[OK] Test Facade Empty Order Validation: PASSED")


def test_facade_none_customer_validation():
    """Test facade validates None customer."""
    try:
        SalesFacade(None)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "customer" in str(e).lower() and "none" in str(e).lower()
    
    print("[OK] Test Facade None Customer Validation: PASSED")


def test_credit_card_payment():
    """Test CreditCardPayment class."""
    customer = Customer("John Silva", "12345678900", "john@email.com")
    order = Order(customer)
    product = Product("Notebook", "Laptop", 2500.00)
    order.add_product(product)
    
    payment = CreditCardPayment(order)
    
    f = StringIO()
    with redirect_stdout(f):
        success = payment.process_payment()
    
    assert success is True
    assert payment.get_payment_amount() == 2500.00
    
    print("[OK] Test Credit Card Payment: PASSED")


def test_bank_slip_payment():
    """Test BankSlipPayment class."""
    customer = Customer("John Silva", "12345678900", "john@email.com")
    order = Order(customer)
    product = Product("Notebook", "Laptop", 2500.00)
    order.add_product(product)
    
    payment = BankSlipPayment(order)
    
    f = StringIO()
    with redirect_stdout(f):
        success = payment.process_payment()
    
    assert success is True
    assert payment.get_payment_amount() == 2500.00
    
    print("[OK] Test Bank Slip Payment: PASSED")


def test_payment_empty_order_validation():
    """Test payment validates empty order."""
    customer = Customer("John Silva", "12345678900", "john@email.com")
    order = Order(customer)
    
    try:
        CreditCardPayment(order)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "product" in str(e).lower()
    
    print("[OK] Test Payment Empty Order Validation: PASSED")


def test_email_service():
    """Test OrderEmail service."""
    customer = Customer("John Silva", "12345678900", "john@email.com")
    order = Order(customer)
    product = Product("Notebook", "Laptop", 2500.00)
    order.add_product(product)
    
    email = OrderEmail(order)
    
    f = StringIO()
    with redirect_stdout(f):
        result = email.send_email("Test message")
    
    assert result is True
    output = f.getvalue()
    assert "EMAIL SENT" in output
    assert "john@email.com" in output
    
    print("[OK] Test Email Service: PASSED")


def test_email_service_methods():
    """Test OrderEmail service methods."""
    customer = Customer("John Silva", "12345678900", "john@email.com")
    order = Order(customer)
    product = Product("Notebook", "Laptop", 2500.00)
    order.add_product(product)
    
    email = OrderEmail(order)
    
    f = StringIO()
    with redirect_stdout(f):
        email.send_payment_success_email("Credit Card")
        email.send_payment_failure_email("Credit Card")
        email.send_order_confirmation_email()
    
    output = f.getvalue()
    assert output.count("EMAIL SENT") == 3
    
    print("[OK] Test Email Service Methods: PASSED")


def test_order_remove_product():
    """Test order remove_product method."""
    customer = Customer("John Silva", "12345678900", "john@email.com")
    order = Order(customer)
    product = Product("Notebook", "Laptop", 2500.00)
    
    order.add_product(product)
    assert order.get_product_count() == 1
    
    removed = order.remove_product(product)
    assert removed is True
    assert order.get_product_count() == 0
    
    # Try to remove again
    removed = order.remove_product(product)
    assert removed is False
    
    print("[OK] Test Order Remove Product: PASSED")


def test_order_clear_products():
    """Test order clear_products method."""
    customer = Customer("John Silva", "12345678900", "john@email.com")
    order = Order(customer)
    
    order.add_product(Product("Item1", "Desc1", 100.0))
    order.add_product(Product("Item2", "Desc2", 200.0))
    
    assert order.get_product_count() == 2
    
    order.clear_products()
    assert order.get_product_count() == 0
    assert order.get_total() == 0.0
    
    print("[OK] Test Order Clear Products: PASSED")


def test_order_products_returns_copy():
    """Test that order.products returns a copy."""
    customer = Customer("John Silva", "12345678900", "john@email.com")
    order = Order(customer)
    product = Product("Notebook", "Laptop", 2500.00)
    order.add_product(product)
    
    products1 = order.products
    products2 = order.products
    
    assert products1 is not products2
    assert products1 == products2
    
    # Try to modify the copy - shouldn't affect original
    fake_product = Product("Fake", "Fake product", 100.0)
    products1.append(fake_product)
    assert len(order.products) == 1
    
    print("[OK] Test Order Products Returns Copy: PASSED")


def test_facade_repr():
    """Test facade string representation."""
    customer = Customer("John Silva", "12345678900", "john@email.com")
    facade = SalesFacade(customer)
    product = Product("Notebook", "Laptop", 2500.00)
    facade.add_product(product)
    
    repr_str = repr(facade)
    assert "SalesFacade" in repr_str
    assert "John Silva" in repr_str
    
    print("[OK] Test Facade Repr: PASSED")


def test_facade_str():
    """Test facade string representation."""
    customer = Customer("John Silva", "12345678900", "john@email.com")
    facade = SalesFacade(customer)
    product = Product("Notebook", "Laptop", 2500.00)
    facade.add_product(product)
    
    str_repr = str(facade)
    assert "John Silva" in str_repr
    assert "2500" in str_repr
    
    print("[OK] Test Facade Str: PASSED")


def test_complete_sales_workflow():
    """Test complete sales workflow through facade."""
    customer = Customer("John Silva", "12345678900", "john@email.com")
    facade = SalesFacade(customer)
    
    # Add products
    facade.add_product(Product("Notebook", "Laptop", 2500.00))
    facade.add_product(Product("Mouse", "Wireless", 50.00))
    
    assert facade.get_product_count() == 2
    assert facade.get_order_total() == 2550.00
    
    # Process payment
    f = StringIO()
    with redirect_stdout(f):
        success = facade.process_credit_card_order()
    
    assert success is True
    output = f.getvalue()
    assert "EMAIL SENT" in output
    
    print("[OK] Test Complete Sales Workflow: PASSED")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("RUNNING FACADE PATTERN TESTS")
    print("=" * 60 + "\n")

    try:
        test_customer_creation()
        test_customer_validation()
        test_product_creation()
        test_product_validation()
        test_order_creation()
        test_order_add_product()
        test_order_multiple_products()
        test_facade_initialization()
        test_facade_add_product()
        test_facade_process_credit_card_order()
        test_facade_process_bank_slip_order()
        test_facade_empty_order_validation()
        test_facade_none_customer_validation()
        test_credit_card_payment()
        test_bank_slip_payment()
        test_payment_empty_order_validation()
        test_email_service()
        test_email_service_methods()
        test_order_remove_product()
        test_order_clear_products()
        test_order_products_returns_copy()
        test_facade_repr()
        test_facade_str()
        test_complete_sales_workflow()

        print("\n" + "=" * 60)
        print("ALL TESTS PASSED! [OK]")
        print("=" * 60 + "\n")

    except AssertionError as e:
        print(f"\n[ERROR] TEST FAILED: {e}\n")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"\n[ERROR] ERROR: {e}\n")
        import traceback
        traceback.print_exc()

