#!/usr/bin/python3
# -*- coding: utf-8 -*-

import glob
import io
import os
import pdb
import sys


sys.path.append("/usr/lib/python3/dist-packages")
import nltk
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk import pos_tag
from nltk import ne_chunk
from nltk.classify import apply_features

labels_text_name = []

def get_entity(text):
    """Prints the entity inside of the text."""
    for sent in sent_tokenize(text):
        for chunk in ne_chunk(pos_tag(word_tokenize(sent))):
            if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                #print(chunk.label(), ' '.join(c[0] for c in chunk.leaves()))
                name = ' '.join(c[0] for c in chunk.leaves())
                print(name)
                label_text(text,name)
                feature_textlength = get_feature_textlength(text)
                print(feature_textlength)


def doextraction(glob_text):
    """Get all the files from the given glob and pass them to the extractor."""
    for thefile in glob.glob(glob_text):
        with io.open(thefile, 'r', encoding='utf-8') as fyl:
            text = fyl.read()
            print(text)
            get_entity(text)

    for label in labels_text_name:
        print(label)

    featuresets = [(get_feature_textlength(n), name) for (n, name) in labels_text_name]
    classifier = nltk.NaiveBayesClassifier.train(featuresets)
    result = classifier.classify(get_feature_textlength(text))
    print("RESULTS===================")
    print(result)

def label_text(text,name):
    labels_text_name.append([text,name])
    

def get_feature_textlength(text):
    return {'textlength' : len(text)}

if __name__ == '__main__':
    # Usage: python3 entity-extractor.py 'train/pos/*.txt'
    doextraction(sys.argv[-1])
