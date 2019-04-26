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

def get_entity(text_path):
    """Prints the entity inside of the text."""
    with io.open(text_path, 'r', encoding='utf-8') as fyl:
        text = fyl.read()
        print(text)
        #get_entity(text)
        for sent in sent_tokenize(text):
            for chunk in ne_chunk(pos_tag(word_tokenize(sent))):
                if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                    #print(chunk.label(), ' '.join(c[0] for c in chunk.leaves()))
                    name = ' '.join(c[0] for c in chunk.leaves())
                    print(name)
                    labels_text_name.append([text_path,name])
                    #features = get_features(text)
                    #feature_textlength = get_feature_textlength(text)
                    #print(features)

def doextraction(glob_text):
    """Get all the files from the given glob and pass them to the extractor."""
    for text_path in glob.glob(glob_text):
        print("text_path = " + text_path)
        get_entity(text_path)
        #with io.open(text_path, 'r', encoding='utf-8') as fyl:
            #text = fyl.read()
            #print(text)
            #get_entity(text)

    for label in labels_text_name:
        print(label)
    
    featuresets = []
    for (text_path, name) in labels_text_name:
        featuresets.append([get_features(text_path),name])
    #featuresets = [(get_features(n), name) for (n, name) in labels_text_name]
    classifier = nltk.NaiveBayesClassifier.train(featuresets)
    result = classifier.classify(get_features(text_path))
    print("RESULTS===================")
    print(result)

#def label_text(text_path,name):
    #labels_text_name.append([text_path,name])
    
def get_features(text_path):
    with io.open(text_path, 'r', encoding='utf-8') as fyl:
        text = fyl.read()
    return {'textlength' : len(text)}

#def get_feature_textlength(text):
#    return {'textlength' : len(text)}

if __name__ == '__main__':
    # Usage: python3 entity-extractor.py 'train/pos/*.txt'
    doextraction(sys.argv[-1])
