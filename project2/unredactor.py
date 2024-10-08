#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse #for parsing command line arguments
import glob
import io
import os
import pdb
import sys

import re

import redactor
from redactor import main

sys.path.append("/usr/lib/python3/dist-packages")
import nltk
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk import pos_tag
from nltk import ne_chunk
from nltk.corpus import stopwords
from nltk.classify import apply_features

labels_text_name = []
def return_labels_text_name():
    return labels_text_name

def get_entity_training(text_path):
    """Prints the entity inside of the text."""
    with io.open(text_path, 'r', encoding='utf-8') as fyl:
        text = fyl.read()
        #print(text)
        #get_entity(text)
        for sent in sent_tokenize(text):
            for chunk in ne_chunk(pos_tag(word_tokenize(sent))):
                if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                    #print(chunk.label(), ' '.join(c[0] for c in chunk.leaves()))
                    name = ' '.join(c[0] for c in chunk.leaves())
                    #print(name)
                    labels_text_name.append([text_path,name])
                    #features = get_features(text_path,name)
                    #print(features)

def get_entity_test(text_path):
    entity_set_test = []
    with io.open(text_path, 'r', encoding='utf-8') as fyl:
        text = fyl.read()
        #print (text)
        matches = re.findall(r'XXX* ?X?X*? ?X*X',text)
        #print (matches)
        for match in matches:
            match = match.strip()
            entity_set_test.append([text_path,match])
    #print(entity_set_test)
    return entity_set_test

def get_entity_validation(text_path_redacted):
    names = []
    text_path_validation = text_path_redacted.replace(".redacted","")
    text_path_validation = text_path_validation.replace("_redacted","")
    with io.open(text_path_validation, 'r', encoding='utf-8') as fyl:
        text = fyl.read()
        #print (text)
        for sent in sent_tokenize(text):
            for chunk in ne_chunk(pos_tag(word_tokenize(sent))):
                if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                    #print(chunk.label(), ' '.join(c[0] for c in chunk.leaves()))
                    name = ' '.join(c[0] for c in chunk.leaves())
                    #print(name)
                    names.append(name)
    return names

def doextraction(glob_text,arg_training):
    """Get all the files from the given glob and pass them to the extractor."""
    final_result = ""
    max_training_files = 20
    if not (not arg_training):
        max_training_files = arg_training
    count_training_files = 0
    for text_path in glob.glob('aclImdb/train/neg/*.txt'):
    #for text_path in glob.glob(glob_text):
        count_training_files = count_training_files + 1
        print("TRAINING FILE " + str(count_training_files) + ": " + text_path)
        if not ("urls_" in text_path):
            #print("valid path....")
            get_entity_training(text_path)
        if count_training_files > int(max_training_files/2):
            print("checked enough neg training files... moving on.")
            break
    for text_path in glob.glob('aclImdb/train/pos/*.txt'):
    #for text_path in glob.glob(glob_text):
        count_training_files = count_training_files + 1
        print("TRAINING FILE " + str(count_training_files) + ": " + text_path)
        if not ("urls_" in text_path):
            #print("valid path....")
            get_entity_training(text_path)
        if count_training_files > max_training_files:
            print("checked enough pos training files... moving on.")
            break

    #print ("about to start printing labels")
    #for label in labels_text_name:
        #print(label)
    
    print ("GETTING TRAINING FEATURESET")
    featuresets_training = []
    for (text_path, name) in labels_text_name:
        featuresets_training.append([get_features_training(text_path,name),name])
    classifier = nltk.NaiveBayesClassifier.train(featuresets_training)
    
    validation_total = 0
    validation_correct = 0
    print ("GETTING TEST FILES...")
    count_test_files = 0
    for text_path in glob.glob(glob_text):
    #for text_path in glob.glob('aclImdb/test_redacted/*/*.txt.redacted'):
        if not ("redacted" in text_path):
            text_folder_path = text_path[0:text_path.rfind('/')+1]
            redactor.main([text_path], text_folder_path, True, False, False, False, False, None,[])
            text_path = text_path + ".redacted"
        count_test_files = count_test_files + 1
        #print("text_path = " + text_path)
        entity_set_validation = get_entity_validation(text_path)
        if not ("urls_" in text_path):
            print("valid path....")
            entity_set_test = get_entity_test(text_path)
            for entity in entity_set_test:
                validation_total = validation_total + 1
                #print(entity)
                result = classifier.classify(get_features_test(entity[0], entity[1]))
                final_result = result
                print("PREDICTION: " + result)
                #print("VALIDATION:")
                #print(entity_set_validation)
                if result in entity_set_validation:
                    validation_correct = validation_correct + 1
                    print("Prediction " + result + " is CORRECT!!!!")
                else:
                    print("Prediction " + result + " is WRONG!!!!")
        if count_test_files > 100:
            print("checked enough test files... moving on.")
            break
    print("===============VALIDATION STATS=====================")
    print("total checked = " + str(validation_total))
    print("number correct = " + str(validation_correct))
    return validation_total, validation_correct, final_result

def get_features_training(text_path,name):
    with io.open(text_path, 'r', encoding='utf-8') as fyl:
        text = fyl.read()
    sentiment = 0 #sentiment 1 corresponds to unsup folder
    if "pos" in text_path:
        sentiment = 2
    elif "neg" in text_path:
        sentiment = 1
    most_common_word = ""
    word_list = text.split()
    #word_list = [word for word in word_list if word not in stopwords.words('english')]
    word_dict = dict((word,1) for word in word_list)
    for word in word_list:
        word_dict[word] = word_dict[word] + 1
    v=list(word_dict.values())
    k=list(word_dict.keys())
    most_common_word = k[v.index(max(v))]
    num_of_spaces = 0
    for character in name:
        if character == " ":
            num_of_spaces = num_of_spaces + 1
    return {'textlength' : int(len(text)/10), 'sentiment' : sentiment, 'namelength' : len(name),'most_common_word' : most_common_word, 'num_of_spaces' : num_of_spaces}

def get_features_test(text_path,name):
    with io.open(text_path, 'r', encoding='utf-8') as fyl:
        text = fyl.read()
    sentiment = 0 #sentiment 1 corresponds to unsup folder
    if "pos" in text_path:
        sentiment = 2
    elif "neg" in text_path:
        sentiment = 1
    most_common_word = ""
    word_list = text.split()
    #word_list = [word for word in word_list if word not in stopwords.words('english')]
    word_dict = dict((word,1) for word in word_list)
    for word in word_list:
        word_dict[word] = word_dict[word] + 1
    v=list(word_dict.values())
    k=list(word_dict.keys())
    most_common_word = k[v.index(max(v))]
    num_of_spaces = 0
    for character in name:
        if character == " ":
            num_of_spaces = num_of_spaces + 1
    return {'textlength' : int(len(text)/10), 'sentiment' : sentiment, 'namelength' : len(name),'most_common_word' : most_common_word, 'num_of_spaces' : num_of_spaces}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str,required=True,help="Files to be unredacted.")
    parser.add_argument("--training", type=int,help="Number of files to use in training")
    args = parser.parse_args()
    if args.input:
        doextraction(args.input,args.training)
