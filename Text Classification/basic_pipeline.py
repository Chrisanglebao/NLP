import sklearn.datasets

# If categories is left as None, all categories will be loaded
#categories = ['comp.graphics','comp.os.ms-windows.misc', 'comp.sys.ibm.pc.hardware', 'comp.sys.mac.hardware', 'comp.windows.x',	
#              'rec.autos', 'rec.motorcycles', 'rec.sport.baseball', 'rec.sport.hockey', 
#			  'sci.crypt', 'sci.electronics', 'sci.med', 'sci.space', 
#			  'misc.forsale', 'talk.politics.misc', 'talk.politics.guns', 'talk.politics.mideast', 'talk.religion.misc', 
#			  'alt.atheism', 'soc.religion.christian']
categories = ['alt.atheism', 'soc.religion.christian', 'comp.graphics', 'sci.med']


twenty_train = sklearn.datasets.load_files('./scikit-learn-master/doc/tutorial/text_analytics/data/twenty_newsgroups/20news-bydate-train', description=None, categories=categories, load_content=True, shuffle=True, encoding='latin1', decode_error='strict', random_state=34)

twenty_test = sklearn.datasets.load_files('./scikit-learn-master/doc/tutorial/text_analytics/data/twenty_newsgroups/20news-bydate-test', description=None, categories=categories, load_content=True, shuffle=True, encoding='latin1', decode_error='strict', random_state=0)


# Let's get some statistics on the data sets

# All class labels
print twenty_train.target_names

# How many data instances
print len(twenty_train.data)
# or
print len(twenty_train.filenames)

print len(twenty_test.data)

# How does a file look like (first 5 lines)

print("\n".join(twenty_train.data[0].split("\n")[:5]))

print(twenty_train.target_names[twenty_train.target[0]])


#Get all words in the train dataset (build the vocabulary)
from sklearn.feature_extraction.text import CountVectorizer
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(twenty_train.data)

# What does it look like
print X_train_counts.shape


# Transform count features to "weights"
from sklearn.feature_extraction.text import TfidfTransformer
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

X_train_tfidf.shape

# Train a Naive Bayes classifier
from sklearn.naive_bayes import MultinomialNB
clfr = MultinomialNB().fit(X_train_tfidf, twenty_train.target)

# Do the same feature processing for test data
X_test_counts = count_vect.transform(twenty_test.data)
X_test_tfidf = tfidf_transformer.transform(X_test_counts)

#Predict the class label
predicted = clfr.predict(X_test_tfidf)

#Alternatively, do it all in one step as a pipeline

from sklearn.pipeline import Pipeline
NB_clfr = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clfr', MultinomialNB())])
NB_clfr = NB_clfr.fit(twenty_train.data, twenty_train.target)

predicted = NB_clfr.predict(twenty_test.data)

#Label for the first file
print('%s => %s' % (twenty_test.filenames[0], twenty_train.target_names[predicted[0]]))

#Label for all files
for x in range(0, len(twenty_test.data)):
  print('%s => %s' % (twenty_test.filenames[x], twenty_train.target_names[predicted[x]]))


# How well did we do?
import numpy as np
print np.mean(predicted == twenty_test.target)


# Now, let's train an SVM classifier
from sklearn.linear_model import SGDClassifier
SVM_clfr = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clfr', SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, n_iter=5, random_state=34))])

SVM_clfr = SVM_clfr.fit(twenty_train.data, twenty_train.target)
predicted = SVM_clfr.predict(twenty_test.data)

print np.mean(predicted == twenty_test.target) 

# Some mre detailed analysis of the results
from sklearn import metrics

print metrics.classification_report(twenty_test.target, predicted, target_names=twenty_test.target_names)
print metrics.confusion_matrix(twenty_test.target, predicted)


