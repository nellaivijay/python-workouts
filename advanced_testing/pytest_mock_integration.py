"""
Advanced Testing - pytest, Mock Objects, and Integration Testing
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import List
import sys
import os


# Sample functions to test
def calculate_discount(price: float, discount_percent: float) -> float:
    """Calculate discounted price"""
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount percent must be between 0 and 100")
    if price < 0:
        raise ValueError("Price cannot be negative")
    return price * (1 - discount_percent / 100)


def divide_numbers(a: float, b: float) -> float:
    """Divide two numbers"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


class ShoppingCart:
    """Simple shopping cart class"""
    
    def __init__(self):
        self.items: List[dict] = []
    
    def add_item(self, name: str, price: float, quantity: int = 1):
        """Add item to cart"""
        if price < 0:
            raise ValueError("Price cannot be negative")
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        self.items.append({
            'name': name,
            'price': price,
            'quantity': quantity
        })
    
    def remove_item(self, name: str):
        """Remove item from cart"""
        self.items = [item for item in self.items if item['name'] != name]
    
    def get_total(self) -> float:
        """Calculate total price"""
        return sum(item['price'] * item['quantity'] for item in self.items)
    
    def clear(self):
        """Clear all items"""
        self.items.clear()


# External service mock
class ExternalAPIService:
    """External API service that we'll mock"""
    
    def fetch_user_data(self, user_id: int) -> dict:
        """Fetch user data from external API"""
        # This would make an actual API call in real implementation
        return {'id': user_id, 'name': 'John Doe', 'email': 'john@example.com'}


class UserService:
    """Service that depends on external API"""
    
    def __init__(self, api_service: ExternalAPIService):
        self.api_service = api_service
    
    def get_user_email(self, user_id: int) -> str:
        """Get user email using external API"""
        user_data = self.api_service.fetch_user_data(user_id)
        return user_data['email']


# Pytest Fixtures
@pytest.fixture
def sample_cart():
    """Fixture that provides a sample shopping cart"""
    cart = ShoppingCart()
    cart.add_item("Laptop", 999.99, 1)
    cart.add_item("Mouse", 29.99, 2)
    return cart


@pytest.fixture
def empty_cart():
    """Fixture that provides an empty shopping cart"""
    return ShoppingCart()


# Pytest Parameterization
@pytest.mark.parametrize("price,discount,expected", [
    (100, 10, 90.0),
    (50, 25, 37.5),
    (200, 0, 200.0),
    (100, 100, 0.0),
])
def test_calculate_discount_valid(price, discount, expected):
    """Test calculate_discount with valid inputs"""
    assert calculate_discount(price, discount) == expected


@pytest.mark.parametrize("price,discount", [
    (100, -1),
    (100, 101),
    (-50, 10),
])
def test_calculate_discount_invalid(price, discount):
    """Test calculate_discount with invalid inputs"""
    with pytest.raises(ValueError):
        calculate_discount(price, discount)


# Test classes
class TestCalculateDiscount:
    """Test class for calculate_discount function"""
    
    def test_normal_discount(self):
        """Test normal discount calculation"""
        assert calculate_discount(100, 20) == 80.0
    
    def test_zero_discount(self):
        """Test zero percent discount"""
        assert calculate_discount(100, 0) == 100.0
    
    def test_full_discount(self):
        """Test 100% discount"""
        assert calculate_discount(100, 100) == 0.0
    
    def test_invalid_discount_negative(self):
        """Test negative discount percent"""
        with pytest.raises(ValueError):
            calculate_discount(100, -10)
    
    def test_invalid_price_negative(self):
        """Test negative price"""
        with pytest.raises(ValueError):
            calculate_discount(-100, 10)


class TestShoppingCart:
    """Test class for ShoppingCart"""
    
    def test_add_item(self, empty_cart):
        """Test adding item to cart"""
        empty_cart.add_item("Test", 10.0, 1)
        assert len(empty_cart.items) == 1
        assert empty_cart.items[0]['name'] == "Test"
    
    def test_add_multiple_items(self, empty_cart):
        """Test adding multiple items"""
        empty_cart.add_item("Item1", 10.0, 1)
        empty_cart.add_item("Item2", 20.0, 2)
        assert len(empty_cart.items) == 2
    
    def test_remove_item(self, sample_cart):
        """Test removing item from cart"""
        sample_cart.remove_item("Laptop")
        assert len(sample_cart.items) == 1
        assert all(item['name'] != "Laptop" for item in sample_cart.items)
    
    def test_get_total(self, sample_cart):
        """Test calculating total"""
        expected_total = 999.99 + (29.99 * 2)
        assert sample_cart.get_total() == expected_total
    
    def test_clear_cart(self, sample_cart):
        """Test clearing cart"""
        sample_cart.clear()
        assert len(sample_cart.items) == 0
    
    def test_add_item_negative_price(self, empty_cart):
        """Test adding item with negative price"""
        with pytest.raises(ValueError):
            empty_cart.add_item("Test", -10.0, 1)
    
    def test_add_item_invalid_quantity(self, empty_cart):
        """Test adding item with invalid quantity"""
        with pytest.raises(ValueError):
            empty_cart.add_item("Test", 10.0, 0)


# Mock Examples
class TestWithMocks:
    """Test class demonstrating mocking"""
    
    def test_mock_external_api(self):
        """Test using mock for external API"""
        # Create mock object
        mock_api = Mock()
        mock_api.fetch_user_data.return_value = {
            'id': 1,
            'name': 'Test User',
            'email': 'test@example.com'
        }
        
        # Use mock in service
        service = UserService(mock_api)
        email = service.get_user_email(1)
        
        assert email == 'test@example.com'
        mock_api.fetch_user_data.assert_called_once_with(1)
    
    @patch('__main__.ExternalAPIService')
    def test_with_patch_decorator(self, mock_api_class):
        """Test using patch decorator"""
        # Configure mock
        mock_instance = mock_api_class.return_value
        mock_instance.fetch_user_data.return_value = {
            'id': 1,
            'name': 'Test User',
            'email': 'test@example.com'
        }
        
        service = UserService(mock_instance)
        email = service.get_user_email(1)
        
        assert email == 'test@example.com'
    
    def test_side_effect(self):
        """Test mock with side effects"""
        mock_func = Mock()
        mock_func.side_effect = [10, 20, 30]
        
        assert mock_func() == 10
        assert mock_func() == 20
        assert mock_func() == 30
    
    def test_mock_exception(self):
        """Test mock that raises exception"""
        mock_func = Mock()
        mock_func.side_effect = ValueError("Test error")
        
        with pytest.raises(ValueError, match="Test error"):
            mock_func()


# Integration Tests
class TestIntegration:
    """Integration tests for combined functionality"""
    
    def test_discount_workflow(self):
        """Test complete discount workflow"""
        cart = ShoppingCart()
        cart.add_item("Laptop", 1000.0, 1)
        
        # Apply 10% discount
        discounted_price = calculate_discount(cart.get_total(), 10)
        assert discounted_price == 900.0
    
    def test_multiple_discounts(self):
        """Test applying multiple discounts"""
        cart = ShoppingCart()
        cart.add_item("Item1", 100.0, 2)
        cart.add_item("Item2", 50.0, 1)
        
        total = cart.get_total()
        discount1 = calculate_discount(total, 10)
        discount2 = calculate_discount(discount1, 5)
        
        assert discount2 < discount1 < total


# Test Discovery and Organization
def test_mark_example():
    """Example of test marks"""
    assert True


@pytest.mark.slow
def test_slow_operation():
    """Example of slow test that can be skipped"""
    import time
    time.sleep(0.1)
    assert True


@pytest.mark.integration
def test_integration_example():
    """Example of integration test"""
    assert True


# Test Configuration
def test_with_setup_teardown():
    """Test with setup and teardown"""
    # Setup
    cart = ShoppingCart()
    
    try:
        # Test
        cart.add_item("Test", 10.0, 1)
        assert len(cart.items) == 1
    finally:
        # Teardown
        cart.clear()


# Run tests function
def run_pytest_tests():
    """Function to run pytest tests"""
    print("Advanced Testing with pytest")
    print("=" * 50)
    
    print("\nTo run these tests:")
    print("1. Install pytest: pip install pytest pytest-mock")
    print("2. Run all tests: pytest advanced_testing.py")
    print("3. Run specific test class: pytest advanced_testing.py::TestShoppingCart")
    print("4. Run with verbose output: pytest -v advanced_testing.py")
    print("5. Run specific marks: pytest -m integration advanced_testing.py")
    print("6. Skip slow tests: pytest -m 'not slow' advanced_testing.py")
    
    print("\nTest Features Demonstrated:")
    print("✓ Pytest fixtures for test setup")
    print("✓ Parameterization for data-driven tests")
    print("✓ Test classes for organization")
    print("✓ Mock objects for isolating dependencies")
    print("✓ Patch decorators for mocking imports")
    print("✓ Integration tests for combined functionality")
    print("✓ Test marks for categorization")
    print("✓ Setup and teardown patterns")
    
    print("\nMocking Techniques:")
    print("✓ Mock objects for external dependencies")
    print("✓ Patch decorators for function replacement")
    print("✓ Side effects for dynamic behavior")
    print("✓ Exception simulation")
    
    print("\nBest Practices:")
    print("• Write isolated unit tests")
    print("• Use mocks for external dependencies")
    print("• Keep tests fast and focused")
    print("• Use descriptive test names")
    print("• Organize tests logically")
    print("• Use fixtures for common setup")


if __name__ == "__main__":
    run_pytest_tests()
    
    # Note: To actually run the tests, use pytest from command line:
    # pytest advanced_testing.py -v