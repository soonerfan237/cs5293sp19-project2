import pytest
import project2
from project2 import unredactor

def test_validation():
    prediction = unredactor.doextraction('*/pos/4458_7.txt',20)
    assert 18  == prediction[0]
    assert 18 == prediction[1]

