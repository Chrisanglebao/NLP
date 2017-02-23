#This file use grid search pipeline

import csv
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import metrics
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.model_selection import StratifiedKFold
from sklearn.naive_bayes import MultinomialNB
from sklearn import neighbors
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import numpy as np
import pandas as pd
import mifs
from sklearn.neighbors import NearestNeighbors
from pprint import pprint
from time import time
import logging
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from nltk.stem import WordNetLemmatizer

print(__doc__)

def term_freq_cal():
    gastroenterology, neurology, orthopedic, radiology, urology = [], [], [], [], []
    stage1_data, label_data = [] , []
    f1, f2, f3, f4, f5 = [], [], [], [], []
    f11, f22, f33, f44, f55 = 0,0,0,0,0
    data_set = []
    topics = []

    input_term = open('stage2_data.txt', 'ru')
    inputr_term = csv.reader(input_term, delimiter='\n')
    for index, stage1 in enumerate(inputr_term):
        if len(stage1) != 0:
            stage1_data += stage1
        else:
            stage1_data += ['']
    input_term.close()

    input_lable = open('trainLabels.csv', 'ru')
    inputr_lable = csv.reader(input_lable, delimiter=',')
    for label in inputr_lable:
        temp_label = 0
        if label[1] == 'Gastroenterology':
            temp_label = 0
        if label[1] == 'Neurology':
            temp_label = 1
        if label[1] == 'Orthopedic':
            temp_label = 2
        if label[1] == 'Radiology':
            temp_label = 3
        if label[1] == 'Urology':
            temp_label = 4
        label_data += [temp_label]
    input_lable.close()


    pipeline = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', SVC())])

    parameters = {
    'vect__max_df': (0.55,),
    'vect__max_features': (2100,),
    'vect__ngram_range': ((1,2),),   
    'clf__kernel': ('linear',),
    'clf__C': (0.55, ),

    }

    grid_search = GridSearchCV(pipeline, parameters, cv=5, n_jobs=-1, verbose=1)

    print("Performing grid search...")
    print("pipeline:", [name for name, _ in pipeline.steps])
    print("parameters:")
    pprint(parameters)
    t0 = time()
    
    y_train = np.asarray(label_data[:826])

    grid_search.fit(stage1_data[:826], label_data[:826])

    print("done in %0.3fs" % (time() - t0))
    print()

    print("Best score: %0.3f" % grid_search.best_score_)
    print("Best parameters set:")
    best_parameters = grid_search.best_estimator_.get_params()
    for param_name in sorted(parameters.keys()):
        print("\t%s: %r" % (param_name, best_parameters[param_name]))


    pred = grid_search.predict(stage1_data[826:])


    for ii in pred:
        if ii == 0:
            print ('Gastroenterology')
        if ii == 1:
            print ('Neurology')
        if ii == 2:
            print ('Orthopedic')
        if ii == 3:
            print ('Radiology')
        if ii == 4:
            print ('Urology')


term_freq_cal()