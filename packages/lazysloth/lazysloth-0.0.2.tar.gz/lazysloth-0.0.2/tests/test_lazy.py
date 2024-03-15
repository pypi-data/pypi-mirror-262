import pytest
from src.lazysloth import LazyVariable


class ComputationResult:
    def __init__(self, arg1, arg2, option=True):
        self.arg1 = arg1
        self.arg2 = arg2
        self.option = option

    def callable_method(self, x):
        return f"Callable with {x}"

def expensive_computation(arg1, arg2, option=True):
    return ComputationResult(arg1, arg2, option)

@pytest.fixture
def lazy_var():
    return LazyVariable(expensive_computation, "value1", "value2", option=False)

def test_lazy_variable_lazy_evaluation(lazy_var):
    # Using a method call to demonstrate lazy loading
    result = lazy_var.callable_method("test")
    assert result == "Callable with test", "Lazy loading or method call failed"

def test_lazy_variable_attribute_access(lazy_var):
    # Accessing dynamically loaded attributes
    assert lazy_var.arg1 == "value1", "Attribute 'arg1' access failed"
    assert lazy_var.option == False, "Attribute 'option' access failed"

def test_lazy_variable_callable_behavior(lazy_var):
    # Verifying callable behavior post lazy loading
    assert lazy_var.callable_method("test") == "Callable with test", "Callable method access failed"

def test_immutable_modification_attempt(lazy_var):
    # Trigger lazy loading
    _ = lazy_var.callable_method("test")
    # Attempt to modify a dynamically loaded attribute
    with pytest.raises(AttributeError, match="Cannot modify attributes of a lazy immutable variable"):
        lazy_var.arg1 = "new value"

def test_immutable_deletion_attempt(lazy_var):
    # Trigger lazy loading
    _ = lazy_var.callable_method("test")
    # Attempt to delete a dynamically loaded attribute
    with pytest.raises(AttributeError, match="Cannot delete attributes of a lazy immutable variable"):
        del lazy_var.arg1


# Adjusted test for various return types might look like this if LazyVariable wraps an object that allows item access.
@pytest.mark.parametrize("return_value, access_method, expected_value", [
    (ComputationResult(42, 'unused', False), 'arg1', 42),
    (ComputationResult('test string', 'unused', False), 'arg1', 'test string'),
    # Add more cases as necessary
])
def test_initialization_with_various_return_types(return_value, access_method, expected_value, lazy_var):
    lazy_var = LazyVariable(lambda: return_value)
    assert getattr(lazy_var, access_method) == expected_value, "Failed to handle different types of return values"

#

def test_repeated_access_preserves_value(lazy_var):
    first_access = lazy_var.arg1
    second_access = lazy_var.arg1
    assert first_access is second_access, "Repeated access to an attribute should not change its value or reinitialize"

def failing_initializer():
    raise ValueError("Initialization failed")

def test_exception_handling_during_initialization():
    lazy_var = LazyVariable(failing_initializer)
    with pytest.raises(ValueError, match="Initialization failed"):
        _ = lazy_var.arg1


