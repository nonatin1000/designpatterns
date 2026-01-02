"""Comprehensive tests for Observer pattern implementation."""

import sys
from pathlib import Path
from io import StringIO
from contextlib import redirect_stdout

# Add src directory to path for standalone execution
if __name__ == "__main__":
    src_dir = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(src_dir))

try:
    # Try relative imports first (when used as module)
    from .newsletter import Newsletter
    from .observer import (
        Observer,
        BaseSubscriber,
        ClientSubscriber,
        EmployeeSubscriber,
        PartnerSubscriber,
        SupplierSubscriber
    )
except ImportError:
    # Fall back to direct module imports (bypassing __init__.py)
    # This avoids importing schemas.py which requires pydantic
    import importlib.util
    import types
    test_dir = Path(__file__).parent
    
    # Create module structure for relative imports
    behavioral = types.ModuleType("behavioral")
    behavioral_observer = types.ModuleType("behavioral.observer")
    sys.modules["behavioral"] = behavioral
    sys.modules["behavioral.observer"] = behavioral_observer
    
    # Load observer module first
    observer_spec = importlib.util.spec_from_file_location(
        "behavioral.observer.observer",
        test_dir / "observer.py"
    )
    observer_module = importlib.util.module_from_spec(observer_spec)
    sys.modules["behavioral.observer.observer"] = observer_module
    behavioral_observer.observer = observer_module
    observer_spec.loader.exec_module(observer_module)
    
    # Load subject module (depends on observer)
    subject_spec = importlib.util.spec_from_file_location(
        "behavioral.observer.subject",
        test_dir / "subject.py"
    )
    subject_module = importlib.util.module_from_spec(subject_spec)
    sys.modules["behavioral.observer.subject"] = subject_module
    behavioral_observer.subject = subject_module
    subject_spec.loader.exec_module(subject_module)
    
    # Extract classes
    Newsletter = subject_module.Newsletter
    Observer = observer_module.Observer
    BaseSubscriber = observer_module.BaseSubscriber
    ClientSubscriber = observer_module.ClientSubscriber
    EmployeeSubscriber = observer_module.EmployeeSubscriber
    PartnerSubscriber = observer_module.PartnerSubscriber
    SupplierSubscriber = observer_module.SupplierSubscriber


def test_newsletter_initialization():
    """Test that newsletter starts with no observers and no messages."""
    newsletter = Newsletter()
    
    assert newsletter.get_subscriber_count() == 0
    assert len(newsletter.get_messages()) == 0
    assert len(newsletter.get_subscribers()) == 0
    
    print("[OK] Test Newsletter Initialization: PASSED")


def test_register_single_observer():
    """Test registering a single observer."""
    newsletter = Newsletter()
    subscriber = ClientSubscriber("John Silva", "john@email.com", newsletter)
    
    assert newsletter.get_subscriber_count() == 1
    subscribers = newsletter.get_subscribers()
    assert len(subscribers) == 1
    assert subscribers[0]["name"] == "John Silva"
    assert subscribers[0]["email"] == "john@email.com"
    
    print("[OK] Test Register Single Observer: PASSED")


def test_register_multiple_observers():
    """Test registering multiple observers."""
    newsletter = Newsletter()
    
    sub1 = ClientSubscriber("John Silva", "john@email.com", newsletter)
    sub2 = EmployeeSubscriber("Maria Santos", "maria@email.com", newsletter)
    sub3 = PartnerSubscriber("Tech Corp", "contact@techcorp.com", newsletter)
    
    assert newsletter.get_subscriber_count() == 3
    subscribers = newsletter.get_subscribers()
    assert len(subscribers) == 3
    
    emails = [s["email"] for s in subscribers]
    assert "john@email.com" in emails
    assert "maria@email.com" in emails
    assert "contact@techcorp.com" in emails
    
    print("[OK] Test Register Multiple Observers: PASSED")


def test_duplicate_registration():
    """Test that duplicate registrations are prevented."""
    newsletter = Newsletter()
    subscriber = ClientSubscriber("John Silva", "john@email.com", newsletter)
    
    # Try to register again
    f = StringIO()
    with redirect_stdout(f):
        newsletter.register_observer(subscriber)
    
    output = f.getvalue()
    assert "already subscribed" in output.lower()
    assert newsletter.get_subscriber_count() == 1
    
    print("[OK] Test Duplicate Registration: PASSED")


def test_remove_observer():
    """Test removing an observer."""
    newsletter = Newsletter()
    subscriber = ClientSubscriber("John Silva", "john@email.com", newsletter)
    
    assert newsletter.get_subscriber_count() == 1
    
    newsletter.remove_observer(subscriber)
    assert newsletter.get_subscriber_count() == 0
    assert len(newsletter.get_subscribers()) == 0
    
    print("[OK] Test Remove Observer: PASSED")


def test_remove_nonexistent_observer():
    """Test removing an observer that is not registered."""
    newsletter = Newsletter()
    subscriber = ClientSubscriber("John Silva", "john@email.com", newsletter)
    
    newsletter.remove_observer(subscriber)
    assert newsletter.get_subscriber_count() == 0
    
    # Try to remove again
    f = StringIO()
    with redirect_stdout(f):
        newsletter.remove_observer(subscriber)
    
    output = f.getvalue()
    assert "not subscribed" in output.lower()
    
    print("[OK] Test Remove Nonexistent Observer: PASSED")


def test_publish_message_notifies_observers():
    """Test that publishing a message notifies all observers."""
    newsletter = Newsletter()
    sub1 = ClientSubscriber("John Silva", "john@email.com", newsletter)
    sub2 = EmployeeSubscriber("Maria Santos", "maria@email.com", newsletter)
    
    f = StringIO()
    with redirect_stdout(f):
        newsletter.publish_message("New products available!")
    
    output = f.getvalue()
    assert "john@email.com" in output
    assert "maria@email.com" in output
    assert "New products available!" in output
    assert output.count("[EMAIL]") == 2
    
    print("[OK] Test Publish Message Notifies Observers: PASSED")


def test_publish_multiple_messages():
    """Test publishing multiple messages."""
    newsletter = Newsletter()
    subscriber = ClientSubscriber("John Silva", "john@email.com", newsletter)
    
    newsletter.publish_message("First message")
    assert len(newsletter.get_messages()) == 1
    assert newsletter.get_messages()[0] == "First message"
    
    newsletter.publish_message("Second message")
    assert len(newsletter.get_messages()) == 2
    assert newsletter.get_messages()[1] == "Second message"
    
    # Only latest message should be sent when notify is called
    f = StringIO()
    with redirect_stdout(f):
        newsletter.notify_observers()
    
    output = f.getvalue()
    assert "Second message" in output
    assert "First message" not in output
    
    print("[OK] Test Publish Multiple Messages: PASSED")


def test_empty_message_raises_error():
    """Test that publishing empty message raises ValueError."""
    newsletter = Newsletter()
    
    try:
        newsletter.publish_message("")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "cannot be empty" in str(e).lower()
    
    print("[OK] Test Empty Message Raises Error: PASSED")


def test_notify_with_no_observers():
    """Test that notify works even with no observers."""
    newsletter = Newsletter()
    newsletter.publish_message("Test message")
    
    # Should not raise error
    newsletter.notify_observers()
    assert len(newsletter.get_messages()) == 1
    
    print("[OK] Test Notify With No Observers: PASSED")


def test_notify_with_no_messages():
    """Test that notify does nothing when there are no messages."""
    newsletter = Newsletter()
    subscriber = ClientSubscriber("John Silva", "john@email.com", newsletter)
    
    f = StringIO()
    with redirect_stdout(f):
        newsletter.notify_observers()
    
    output = f.getvalue()
    assert output == ""  # No output when no messages
    
    print("[OK] Test Notify With No Messages: PASSED")


def test_subscriber_unsubscribe():
    """Test subscriber unsubscribe method."""
    newsletter = Newsletter()
    subscriber = ClientSubscriber("John Silva", "john@email.com", newsletter)
    
    assert newsletter.get_subscriber_count() == 1
    
    subscriber.unsubscribe()
    assert newsletter.get_subscriber_count() == 0
    
    print("[OK] Test Subscriber Unsubscribe: PASSED")


def test_subscriber_getters():
    """Test subscriber getter methods."""
    newsletter = Newsletter()
    subscriber = ClientSubscriber("John Silva", "john@email.com", newsletter)
    
    assert subscriber.get_name() == "John Silva"
    assert subscriber.get_email() == "john@email.com"
    
    print("[OK] Test Subscriber Getters: PASSED")


def test_subscriber_validation():
    """Test that subscriber validates name and email."""
    newsletter = Newsletter()
    
    # Empty name
    try:
        ClientSubscriber("", "john@email.com", newsletter)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "cannot be empty" in str(e).lower()
    
    # Empty email
    try:
        ClientSubscriber("John Silva", "", newsletter)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "cannot be empty" in str(e).lower()
    
    print("[OK] Test Subscriber Validation: PASSED")


def test_different_subscriber_types():
    """Test different subscriber types."""
    newsletter = Newsletter()
    
    client = ClientSubscriber("Client", "client@email.com", newsletter)
    employee = EmployeeSubscriber("Employee", "employee@email.com", newsletter)
    partner = PartnerSubscriber("Partner", "partner@email.com", newsletter)
    supplier = SupplierSubscriber("Supplier", "supplier@email.com", newsletter)
    
    assert isinstance(client, ClientSubscriber)
    assert isinstance(employee, EmployeeSubscriber)
    assert isinstance(partner, PartnerSubscriber)
    assert isinstance(supplier, SupplierSubscriber)
    
    assert newsletter.get_subscriber_count() == 4
    
    print("[OK] Test Different Subscriber Types: PASSED")


def test_observer_update_method():
    """Test that observer update method is called correctly."""
    newsletter = Newsletter()
    subscriber = ClientSubscriber("John Silva", "john@email.com", newsletter)
    
    f = StringIO()
    with redirect_stdout(f):
        newsletter.publish_message("Test message")
    
    output = f.getvalue()
    assert "John Silva" in output
    assert "john@email.com" in output
    assert "Test message" in output
    
    print("[OK] Test Observer Update Method: PASSED")


def test_multiple_notifications():
    """Test that observers receive multiple notifications."""
    newsletter = Newsletter()
    subscriber = ClientSubscriber("John Silva", "john@email.com", newsletter)
    
    f = StringIO()
    with redirect_stdout(f):
        newsletter.publish_message("First message")
        newsletter.publish_message("Second message")
        newsletter.publish_message("Third message")
    
    output = f.getvalue()
    assert output.count("[EMAIL]") == 3
    assert "First message" in output
    assert "Second message" in output
    assert "Third message" in output
    
    print("[OK] Test Multiple Notifications: PASSED")


def test_observer_removed_before_notification():
    """Test that removed observers don't receive notifications."""
    newsletter = Newsletter()
    sub1 = ClientSubscriber("John Silva", "john@email.com", newsletter)
    sub2 = EmployeeSubscriber("Maria Santos", "maria@email.com", newsletter)
    
    assert newsletter.get_subscriber_count() == 2
    
    newsletter.remove_observer(sub1)
    
    f = StringIO()
    with redirect_stdout(f):
        newsletter.publish_message("Test message")
    
    output = f.getvalue()
    assert "maria@email.com" in output
    assert "john@email.com" not in output
    assert output.count("[EMAIL]") == 1
    
    print("[OK] Test Observer Removed Before Notification: PASSED")


def test_get_messages_returns_copy():
    """Test that get_messages returns a copy, not the original list."""
    newsletter = Newsletter()
    newsletter.publish_message("Test message")
    
    messages1 = newsletter.get_messages()
    messages2 = newsletter.get_messages()
    
    # Should be different objects
    assert messages1 is not messages2
    # But same content
    assert messages1 == messages2
    
    # Modifying one shouldn't affect the other
    messages1.append("Fake message")
    assert len(newsletter.get_messages()) == 1
    
    print("[OK] Test Get Messages Returns Copy: PASSED")


def test_newsletter_repr():
    """Test newsletter string representation."""
    newsletter = Newsletter()
    subscriber = ClientSubscriber("John Silva", "john@email.com", newsletter)
    newsletter.publish_message("Test message")
    
    repr_str = repr(newsletter)
    assert "Newsletter" in repr_str
    assert "subscribers=1" in repr_str
    assert "messages=1" in repr_str
    
    print("[OK] Test Newsletter Repr: PASSED")


def test_subscriber_repr():
    """Test subscriber string representation."""
    newsletter = Newsletter()
    subscriber = ClientSubscriber("John Silva", "john@email.com", newsletter)
    
    repr_str = repr(subscriber)
    assert "ClientSubscriber" in repr_str
    assert "John Silva" in repr_str
    assert "john@email.com" in repr_str
    
    print("[OK] Test Subscriber Repr: PASSED")


def test_complete_newsletter_lifecycle():
    """Test complete newsletter lifecycle."""
    newsletter = Newsletter()
    
    # Subscribe observers
    sub1 = ClientSubscriber("John Silva", "john@email.com", newsletter)
    sub2 = EmployeeSubscriber("Maria Santos", "maria@email.com", newsletter)
    
    assert newsletter.get_subscriber_count() == 2
    
    # Publish messages
    newsletter.publish_message("Welcome to our newsletter!")
    assert len(newsletter.get_messages()) == 1
    
    newsletter.publish_message("New products available!")
    assert len(newsletter.get_messages()) == 2
    
    # Unsubscribe one
    sub1.unsubscribe()
    assert newsletter.get_subscriber_count() == 1
    
    # Publish another message
    newsletter.publish_message("Special promotion!")
    assert len(newsletter.get_messages()) == 3
    
    # Verify only remaining subscriber receives it
    f = StringIO()
    with redirect_stdout(f):
        newsletter.notify_observers()
    
    output = f.getvalue()
    assert "maria@email.com" in output
    assert "john@email.com" not in output
    
    print("[OK] Test Complete Newsletter Lifecycle: PASSED")


def test_observer_pattern_one_to_many():
    """Test that one subject can notify many observers."""
    newsletter = Newsletter()
    
    # Create many observers
    subscribers = []
    for i in range(10):
        subscriber = ClientSubscriber(f"User {i}", f"user{i}@email.com", newsletter)
        subscribers.append(subscriber)
    
    assert newsletter.get_subscriber_count() == 10
    
    f = StringIO()
    with redirect_stdout(f):
        newsletter.publish_message("Broadcast message")
    
    output = f.getvalue()
    assert output.count("[EMAIL]") == 10
    
    # Verify all emails are in output
    for i in range(10):
        assert f"user{i}@email.com" in output
    
    print("[OK] Test Observer Pattern One To Many: PASSED")


def test_observer_independence():
    """Test that observers are independent of each other."""
    newsletter1 = Newsletter()
    newsletter2 = Newsletter()
    
    sub1 = ClientSubscriber("User 1", "user1@email.com", newsletter1)
    sub2 = ClientSubscriber("User 2", "user2@email.com", newsletter2)
    
    assert newsletter1.get_subscriber_count() == 1
    assert newsletter2.get_subscriber_count() == 1
    
    f = StringIO()
    with redirect_stdout(f):
        newsletter1.publish_message("Newsletter 1 message")
    
    output = f.getvalue()
    assert "user1@email.com" in output
    assert "user2@email.com" not in output
    
    print("[OK] Test Observer Independence: PASSED")


def test_subscriber_auto_registration():
    """Test that subscribers auto-register when created."""
    newsletter = Newsletter()
    
    assert newsletter.get_subscriber_count() == 0
    
    subscriber = ClientSubscriber("John Silva", "john@email.com", newsletter)
    
    # Should be automatically registered
    assert newsletter.get_subscriber_count() == 1
    assert subscriber in newsletter._observers
    
    print("[OK] Test Subscriber Auto Registration: PASSED")


def test_get_subscribers_returns_copy():
    """Test that get_subscribers returns a copy, not the original list."""
    newsletter = Newsletter()
    sub1 = ClientSubscriber("John Silva", "john@email.com", newsletter)
    sub2 = EmployeeSubscriber("Maria Santos", "maria@email.com", newsletter)
    
    subscribers1 = newsletter.get_subscribers()
    subscribers2 = newsletter.get_subscribers()
    
    # Should be different objects
    assert subscribers1 is not subscribers2
    # But same content
    assert subscribers1 == subscribers2
    
    # Modifying one shouldn't affect the other
    subscribers1.append({"name": "Fake", "email": "fake@email.com"})
    assert len(newsletter.get_subscribers()) == 2
    
    print("[OK] Test Get Subscribers Returns Copy: PASSED")


def test_subscriber_unsubscribe_multiple_times():
    """Test that unsubscribing multiple times doesn't cause errors."""
    newsletter = Newsletter()
    subscriber = ClientSubscriber("John Silva", "john@email.com", newsletter)
    
    assert newsletter.get_subscriber_count() == 1
    
    subscriber.unsubscribe()
    assert newsletter.get_subscriber_count() == 0
    
    # Try to unsubscribe again
    f = StringIO()
    with redirect_stdout(f):
        subscriber.unsubscribe()
    
    output = f.getvalue()
    assert "not subscribed" in output.lower()
    assert newsletter.get_subscriber_count() == 0
    
    print("[OK] Test Subscriber Unsubscribe Multiple Times: PASSED")


def test_observer_register_unregister_register():
    """Test observer that registers, unregisters, and registers again."""
    newsletter = Newsletter()
    subscriber = ClientSubscriber("John Silva", "john@email.com", newsletter)
    
    assert newsletter.get_subscriber_count() == 1
    
    # Unregister
    newsletter.remove_observer(subscriber)
    assert newsletter.get_subscriber_count() == 0
    
    # Register again
    newsletter.register_observer(subscriber)
    assert newsletter.get_subscriber_count() == 1
    
    # Should receive notifications again
    f = StringIO()
    with redirect_stdout(f):
        newsletter.publish_message("Welcome back!")
    
    output = f.getvalue()
    assert "john@email.com" in output
    assert "Welcome back!" in output
    
    print("[OK] Test Observer Register Unregister Register: PASSED")


def test_message_with_special_characters():
    """Test publishing message with special characters."""
    newsletter = Newsletter()
    subscriber = ClientSubscriber("John Silva", "john@email.com", newsletter)
    
    special_message = "Mensagem com acentuação: ção, ão, ê, á! E símbolos: @#$%&*()"
    
    f = StringIO()
    with redirect_stdout(f):
        newsletter.publish_message(special_message)
    
    output = f.getvalue()
    assert special_message in output
    assert "ç" in output or "ão" in output
    
    assert len(newsletter.get_messages()) == 1
    assert newsletter.get_messages()[0] == special_message
    
    print("[OK] Test Message With Special Characters: PASSED")


def test_message_with_unicode():
    """Test publishing message with unicode characters."""
    newsletter = Newsletter()
    subscriber = ClientSubscriber("John Silva", "john@email.com", newsletter)
    
    unicode_message = "Hello 世界 🌍 Unicode: ñ, é, ü, 中文"
    
    f = StringIO()
    with redirect_stdout(f):
        newsletter.publish_message(unicode_message)
    
    output = f.getvalue()
    assert unicode_message in output
    
    assert len(newsletter.get_messages()) == 1
    assert newsletter.get_messages()[0] == unicode_message
    
    print("[OK] Test Message With Unicode: PASSED")


def test_long_message():
    """Test publishing a very long message."""
    newsletter = Newsletter()
    subscriber = ClientSubscriber("John Silva", "john@email.com", newsletter)
    
    long_message = "A" * 1000  # 1000 characters
    
    f = StringIO()
    with redirect_stdout(f):
        newsletter.publish_message(long_message)
    
    output = f.getvalue()
    assert long_message in output
    
    assert len(newsletter.get_messages()) == 1
    assert len(newsletter.get_messages()[0]) == 1000
    
    print("[OK] Test Long Message: PASSED")


def test_get_subscribers_format():
    """Test that get_subscribers returns correct format."""
    newsletter = Newsletter()
    sub1 = ClientSubscriber("John Silva", "john@email.com", newsletter)
    sub2 = EmployeeSubscriber("Maria Santos", "maria@email.com", newsletter)
    
    subscribers = newsletter.get_subscribers()
    
    assert len(subscribers) == 2
    assert isinstance(subscribers[0], dict)
    assert isinstance(subscribers[1], dict)
    
    # Check format
    assert "name" in subscribers[0]
    assert "email" in subscribers[0]
    assert "name" in subscribers[1]
    assert "email" in subscribers[1]
    
    # Check values
    names = [s["name"] for s in subscribers]
    emails = [s["email"] for s in subscribers]
    
    assert "John Silva" in names
    assert "Maria Santos" in names
    assert "john@email.com" in emails
    assert "maria@email.com" in emails
    
    print("[OK] Test Get Subscribers Format: PASSED")


def test_observer_in_multiple_newsletters():
    """Test that an observer can be registered in multiple newsletters."""
    newsletter1 = Newsletter()
    newsletter2 = Newsletter()
    
    # Create subscriber for first newsletter
    sub1 = ClientSubscriber("John Silva", "john@email.com", newsletter1)
    
    # Register same subscriber in second newsletter
    newsletter2.register_observer(sub1)
    
    assert newsletter1.get_subscriber_count() == 1
    assert newsletter2.get_subscriber_count() == 1
    
    # Publish in first newsletter
    f1 = StringIO()
    with redirect_stdout(f1):
        newsletter1.publish_message("Newsletter 1 message")
    
    output1 = f1.getvalue()
    assert "john@email.com" in output1
    
    # Publish in second newsletter
    f2 = StringIO()
    with redirect_stdout(f2):
        newsletter2.publish_message("Newsletter 2 message")
    
    output2 = f2.getvalue()
    assert "john@email.com" in output2
    
    print("[OK] Test Observer In Multiple Newsletters: PASSED")


def test_multiple_observers_same_type():
    """Test multiple observers of the same type."""
    newsletter = Newsletter()
    
    # Create multiple clients
    clients = []
    for i in range(5):
        client = ClientSubscriber(f"Client {i}", f"client{i}@email.com", newsletter)
        clients.append(client)
    
    assert newsletter.get_subscriber_count() == 5
    
    # All should receive notifications
    f = StringIO()
    with redirect_stdout(f):
        newsletter.publish_message("Message for all clients")
    
    output = f.getvalue()
    assert output.count("[EMAIL]") == 5
    
    # Verify all clients received
    for i in range(5):
        assert f"client{i}@email.com" in output
    
    print("[OK] Test Multiple Observers Same Type: PASSED")


def test_notify_only_latest_message():
    """Test that notify_observers only sends the latest message."""
    newsletter = Newsletter()
    subscriber = ClientSubscriber("John Silva", "john@email.com", newsletter)
    
    # Publish multiple messages
    newsletter.publish_message("First message")
    newsletter.publish_message("Second message")
    newsletter.publish_message("Third message")
    
    assert len(newsletter.get_messages()) == 3
    
    # Manually call notify - should only send latest
    f = StringIO()
    with redirect_stdout(f):
        newsletter.notify_observers()
    
    output = f.getvalue()
    assert "Third message" in output
    assert "First message" not in output
    assert "Second message" not in output
    
    print("[OK] Test Notify Only Latest Message: PASSED")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("RUNNING OBSERVER PATTERN TESTS")
    print("=" * 60 + "\n")

    try:
        test_newsletter_initialization()
        test_register_single_observer()
        test_register_multiple_observers()
        test_duplicate_registration()
        test_remove_observer()
        test_remove_nonexistent_observer()
        test_publish_message_notifies_observers()
        test_publish_multiple_messages()
        test_empty_message_raises_error()
        test_notify_with_no_observers()
        test_notify_with_no_messages()
        test_subscriber_unsubscribe()
        test_subscriber_getters()
        test_subscriber_validation()
        test_different_subscriber_types()
        test_observer_update_method()
        test_multiple_notifications()
        test_observer_removed_before_notification()
        test_get_messages_returns_copy()
        test_newsletter_repr()
        test_subscriber_repr()
        test_complete_newsletter_lifecycle()
        test_observer_pattern_one_to_many()
        test_observer_independence()
        test_subscriber_auto_registration()
        test_get_subscribers_returns_copy()
        test_subscriber_unsubscribe_multiple_times()
        test_observer_register_unregister_register()
        test_message_with_special_characters()
        test_message_with_unicode()
        test_long_message()
        test_get_subscribers_format()
        test_observer_in_multiple_newsletters()
        test_multiple_observers_same_type()
        test_notify_only_latest_message()

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

