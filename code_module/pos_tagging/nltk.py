
import math
import nltk
import time
from math import log
# Constants to be used by you when you fill the functions
START_SYMBOL = '*'
STOP_SYMBOL = 'STOP'
MINUS_INFINITY_SENTENCE_LOG_PROB = -1000

# TODO: IMPLEMENT THIS FUNCTION
# Calculates unigram, bigram, and trigram probabilities given a training corpus
# training_corpus: is a list of the sentences. Each sentence is a string with tokens separated by spaces, ending in a newline cha$
# This function outputs three python dictionaries, where the keys are tuples expressing the ngram and the value is the log probab$
def calc_probabilities(training_corpus):

    unigram_p = {}
    bigram_p = {}
    trigram_p = {}
    count = {}
    count_1 = {}
    count_0 = {}
    count_2 = {}
    total_list = []
    count_2 = {}
    total_list = []
    for sentence in training_corpus:

        story = START_SYMBOL + ' ' + sentence + ' ' + STOP_SYMBOL
        story_uni = START_SYMBOL + ' ' + sentence
        story_tri = START_SYMBOL + ' ' +  START_SYMBOL  + ' ' + sentence + ' ' + STOP_SYMBOL

        unigram_list = [(item) for item in story.split()]
        bigram_tuples = list(nltk.bigrams(story.split()))
        trigram_tuples_temp = list(nltk.bigrams(story_tri.split()))
        trigram_tuples = list(nltk.trigrams(story_tri.split()))
        total_list += story_uni.split()

        for item in set(unigram_list):
            if item not in count_0:
                count_0[item] = unigram_list.count(item)
            else:
                count_0[item] = unigram_list.count(item) + count_0[item]
        for item in set(bigram_tuples):
            if item not in count:
                count[item] =  bigram_tuples.count(item)
            else:
                count[item] = bigram_tuples.count(item) + count[item]
        for item in set(trigram_tuples):
            if item not in count_1:
                count_1[item] = trigram_tuples.count(item)
            else:
                count_1[item] = trigram_tuples.count(item)+count_1[item]
        for item in set(trigram_tuples_temp):
            if item not in count_2:
                count_2[item] =  trigram_tuples_temp.count(item)
            else:
                count_2[item] = trigram_tuples_temp.count(item) + count_2[item]
    for item in count_0:
        unigram_p[item] = log(float(count_0[item])/float(len(total_list)), 2)


    for item in count:
        numb =  float(count[item])/float(count_0[item[0]])
        bigram_p[item] = log(float(numb), 2)

    for item in count_1:
#        if item[0] + item[1] != '**':
#            print item
        trigram_p[item] = log(float(count_1[item])/float(count_2[(item[0], item[1],)]), 2)
    return unigram_p, bigram_p, trigram_p


# Each input is a python dictionary where keys are a tuple expressing the ngram, and the value is the log probability of that ngr$
def q1_output(unigrams, bigrams, trigrams, filename):
    # output probabilities
    outfile = open(filename, 'w')

    unigrams_keys = unigrams.keys()
    unigrams_keys.sort()
    for unigram in unigrams_keys:
        outfile.write('UNIGRAM ' + unigram[0] + ' ' + str(unigrams[unigram]) + '\n')

    bigrams_keys = bigrams.keys()
    bigrams_keys.sort()
    for bigram in bigrams_keys:
        outfile.write('BIGRAM ' + bigram[0] + ' ' + bigram[1]  + ' ' + str(bigrams[bigram]) + '\n')

    trigrams_keys = trigrams.keys()
    trigrams_keys.sort()
    for trigram in trigrams_keys:
        outfile.write('TRIGRAM ' + trigram[0] + ' ' + trigram[1] + ' ' + trigram[2] + ' ' + str(trigrams[trigram]) + '\n')

    outfile.close()



def score(ngram_p, n, corpus):

    if n == 1:
        scores = []
        for sen in corpus:
            score  = 0
            senten = (START_SYMBOL + ' ' + sen).split()
            for i in senten:
                if i in ngram_p:
                    score += ngram_p[i]
                else:
                    score = MINUS_INFINITY_SENTENCE_LOG_PROB
            scores += [score]

    if n == 2:
       scores = []
       for sen in corpus:
            senten = (START_SYMBOL + ' ' + sen + ' ' + STOP_SYMBOL).split()
            score = 0
            for i in range(len(senten)):
                if i<len(senten)-1 and (senten[i],senten[i+1]) in ngram_p:
                    score += ngram_p[(senten[i],senten[i+1])]
                elif i<len(senten)-1:
                    score = MINUS_INFINITY_SENTENCE_LOG_PROB
            scores += [score]


    if n == 3:
        scores = []
        for sen in corpus:
            senten = (START_SYMBOL + ' ' + START_SYMBOL + ' ' +  sen + ' ' + STOP_SYMBOL).split()
            score_3 = 0
            for i in range(len(senten)):
                if i < (len(senten)-2) and (senten[i], senten[i+1], senten[i+2]) in ngram_p:
                    score_3 += ngram_p[(senten[i], senten[i+1], senten[i+2])]
                elif i < len(senten)-2 and (senten[i], senten[i+1], senten[i+2]) not in ngram_p:
                    score_3 = MINUS_INFINITY_SENTENCE_LOG_PROB
            scores += [score_3]
    return scores

# Outputs a score to a file
# scores: list of scores
# filename: is the output file name
def score_output(scores, filename):
    outfile = open(filename, 'w')
    for score in scores:
        outfile.write(str(score) + '\n')
    outfile.close()

# Like score(), this function returns a python list of scores
def linearscore(unigrams, bigrams, trigrams, corpus):
    scores = []
    for sen in corpus:
        score = 0
        senten = (START_SYMBOL + ' ' + START_SYMBOL + ' ' +  sen + ' ' + STOP_SYMBOL).split()
        for i in range(len(senten)):
            if i < len(senten)-2 and (senten[i], senten[i+1], senten[i+2]) in trigrams:
                score += log((2**trigrams[(senten[i], senten[i+1], senten[i+2])] + 2**bigrams[(senten[i+1], senten[i+2])] + 2**un$

        scores += [score]
    return scores

DATA_PATH = 'data/'
OUTPUT_PATH = 'output/'

def main():
    # start timer
    time.clock()

    # get data
    infile = open(DATA_PATH + 'Brown_train.txt', 'r')
    corpus = infile.readlines()
    infile.close()

    # calculate ngram probabilities (question 1)
    unigrams, bigrams, trigrams = calc_probabilities(corpus)

    # question 1 output
    q1_output(unigrams, bigrams, trigrams, OUTPUT_PATH + 'A1.txt')

    # score sentences (question 2)
    uniscores = score(unigrams, 1, corpus)
    biscores = score(bigrams, 2, corpus)
    triscores = score(trigrams, 3, corpus)
    score_output(uniscores, OUTPUT_PATH + 'A2.uni.txt')
    score_output(biscores, OUTPUT_PATH + 'A2.bi.txt')
    score_output(triscores, OUTPUT_PATH + 'A2.tri.txt')

    # linear interpolation (question 3)
    linearscores = linearscore(unigrams, bigrams, trigrams, corpus)

    # question 3 output
    score_output(linearscores, OUTPUT_PATH + 'A3.txt')

    # open Sample1 and Sample2 (question 5)
    infile = open(DATA_PATH + 'Sample1.txt', 'r')
    sample1 = infile.readlines()
    infile.close()
    infile = open(DATA_PATH + 'Sample2.txt', 'r')
    sample2 = infile.readlines()
    infile.close()
    
    # score the samples
    sample1scores = linearscore(unigrams, bigrams, trigrams, sample1)
    sample2scores = linearscore(unigrams, bigrams, trigrams, sample2)

    # question 5 output
    score_output(sample1scores, OUTPUT_PATH + 'Sample1_scored.txt')
    score_output(sample2scores, OUTPUT_PATH + 'Sample2_scored.txt')

    # print total time to run Part A
    print "Part A time: " + str(time.clock()) + ' sec'

if __name__ == "__main__": main()



