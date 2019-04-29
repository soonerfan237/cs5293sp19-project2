import pytest
import project2
from project2 import unredactor

def test_entities():
    entity_set_test = unredactor.get_entity_test('/project/cs5293sp19-project2/tests/pos/0_10.txt.redacted')
    assert 5 == len(entity_set_test)

def test_featureset():
    featureset = unredactor.get_features_test('/project/cs5293sp19-project2/tests/pos/0_10.txt.redacted','XXXXX XXXXXXX')
    assert 79 == featureset['textlength']
    assert 2 == featureset['sentiment']
    assert 13 == featureset['namelength']
    assert 'I' == featureset['most_common_word']
    assert 1 == featureset['num_of_spaces']

