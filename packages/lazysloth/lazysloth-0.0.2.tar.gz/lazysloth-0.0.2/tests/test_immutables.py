import pytest
from src.lazysloth import ImmutableVariable

class SampleData:
    def __init__(self):
        self.attr = "test attribute"
        self.data = {"key": "test value"}

    def callable_attr(self):
        return "callable result"



def test_immutable_variable_initialization():
    sample = SampleData()
    immutable_var = ImmutableVariable(sample)
    assert immutable_var._value == sample, "ImmutableVariable did not initialize correctly."

def test_immutable_variable_attribute_access():
    sample = SampleData()
    immutable_var = ImmutableVariable(sample)
    assert immutable_var.attr == "test attribute", "Attribute access failed."

def test_immutable_variable_item_access():
    sample = {"key": "value"}
    immutable_var = ImmutableVariable(sample)
    assert immutable_var["key"] == "value", "Item access failed."

def test_immutable_variable_callable_behavior():
    sample = SampleData()
    immutable_var = ImmutableVariable(sample)
    assert immutable_var.callable_attr() == "callable result", "Callable behavior failed."

def test_immutable_variable_modification_attempt():
    sample = SampleData()
    immutable_var = ImmutableVariable(sample)
    with pytest.raises(AttributeError, match="Cannot modify immutable variable"):
        immutable_var.attr = "modified"

def test_immutable_variable_deletion_attempt():
    sample = SampleData()
    immutable_var = ImmutableVariable(sample)
    with pytest.raises(AttributeError, match="Cannot delete immutable variable attributes"):
        del immutable_var.attr

