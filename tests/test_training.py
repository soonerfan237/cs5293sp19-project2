import pytest
import project2
from project2 import unredactor

def test_entities():
    unredactor.doextraction('/tests/*/*.txt',20)
    labels_text_name = unredactor.return_labels_text_name()
    assert 132 == len(labels_text_name)

def test_featureset():
    featureset = unredactor.get_features_training('/project/cs5293sp19-project2/tests/pos/0_10.txt','Kevin Costner')
    assert 79 == featureset['textlength']
    assert 2 == featureset['sentiment']
    assert 13 == featureset['namelength']
    assert 'I' == featureset['most_common_word']
    assert 1 == featureset['num_of_spaces']
