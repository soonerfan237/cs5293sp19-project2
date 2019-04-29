import pytest
import project2
from project2 import redactor

def test_names():
    results = redactor.main(["tests/pos/*.txt"], "tests/pos/", True, False, False, False, False, None, [])
    assert results[0] == 18
