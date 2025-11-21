# tests/test_unit.py
from synapse_ws.server import add_numbers

def test_add_numbers():
    assert add_numbers(1, 2) == 3
    assert add_numbers(3.5, 0.5) == 4.0
