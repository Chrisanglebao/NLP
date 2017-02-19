
import sys
import nltk
import math
import time
from collections import Counter

START_SYMBOL = '*'
STOP_SYMBOL = 'STOP'
RARE_SYMBOL = '_RARE_'
RARE_WORD_MAX_FREQ = 5
LOG_PROB_OF_ZERO = -1000


# TODO: IMPLEMENT THIS FUNCTION
# Receives a list of tagged sentences and processes each sentence to generate a list of words and a list of tags.
# Each sentence is a string of space separated "WORD/TAG" tokens, with a newline character in the end.
# Remember to include start and stop symbols in yout returned lists, as defined by the constants START_SYMBOL and STOP_SYMBOL.
# brown_words (the list of words) should be a list where every element is a list of the tags of a particular sentence.
# brown_tags (the list of tags) should be a list where every element is a list of the tags of a particular sentence.
def split_wordtags(brown_train):
    brown_words = []
    brown_tags = []
    for sen in brown_train:
#        sen = START_SYMBOL + ' ' + sen + ' ' + STOP_STMBOL
        brown_words += [START_SYMBOL, START_SYMBOL]
        brown_tags += [START_SYMBOL, START_SYMBOL]
        for word in sen.split():
            if word.count('/')==1:
                brown_words += [word[:word.index('/')]]
                brown_tags += [word[(word.index('/')+1):]]
            elif word.count('/')==2:
                i = word.index('/')
                brown_words += [word[:word.index('/', i+1)]]
                brown_tags += [word[(word.index('/', i+1)+1):]]
        brown_words += [STOP_SYMBOL]
        brown_tags += [STOP_SYMBOL]
    return brown_words, brown_tags


# TODO: IMPLEMENT THIS FUNCTION
# This function takes tags from the training data and calculates tag trigram probabilities.
# It returns a python dictionary where the keys are tuples that represent the tag trigram, and the values are the log probability$
def calc_trigrams(brown_tags):
    q_values = {}
    trigram_tuples = list(nltk.trigrams(brown_tags))
    trigram_tuples_temp = list(nltk.bigrams(brown_tags))
    count_1={}
    count_2={}
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


    for item in count_1:
        q_values[item] = math.log(float(count_1[item])/float(count_2[(item[0], item[1],)]), 2)

    return q_values


# This function takes output from calc_trigrams() and outputs it in the proper format
def q2_output(q_values, filename):
    outfile = open(filename, "w")
    trigrams = q_values.keys()
    trigrams.sort()
    for trigram in trigrams:
        output = " ".join(['TRIGRAM', trigram[0], trigram[1], trigram[2], str(q_values[trigram])])
        outfile.write(output + '\n')
    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# Takes the words from the training data and returns a set of all of the words that occur more than 5 times (use RARE_WORD_MAX_FR$
# brown_words is a python list where every element is a python list of the words of a particular sentence.
# Note: words that appear exactly 5 times should be considered rare!
def calc_known(brown_words):
    known_words = set([])
    #This count function is cited from Ashif from Stackoverflow
    count_word =Counter(brown_words)
    for word in brown_words:
        if count_word[word] > 5:
            known_words.add(word)
    return known_words



# TODO: IMPLEMENT THIS FUNCTION
# Takes the words from the training data and a set of words that should not be replaced for '_RARE_'
# Returns the equivalent to brown_words but replacing the unknown words by '_RARE_' (use RARE_SYMBOL constant)
def replace_rare(brown_words, known_words):
    brown_words_rare = []
    for word in brown_words:
        if word not in known_words:
            brown_words_rare += [RARE_SYMBOL]
        else:
            brown_words_rare += [word]
    return brown_words_rare

# This function takes the ouput from replace_rare and outputs it to a file
def q3_output(rare, filename):
    outfile = open(filename, 'w')
    for sentence in rare:
        outfile.write(' '.join(sentence[2:-1]) + '\n')
    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# Calculates emission probabilities and creates a set of all possible tags
# The first return value is a python dictionary where each key is a tuple in which the first element is a word
# and the second is a tag, and the value is the log probability of the emission of the word given the tag
# The second return value is a set of all possible tags for this data set
def calc_emission(brown_words_rare, brown_tags):
    e_values = {}
    taglist = set([])
    total_list = []
    count = {}
    count_1 = {}
    for i in range(len(brown_words_rare)):

        total_list += [(brown_words_rare[i], brown_tags[i])]
    for item in set(brown_tags):
        if item not in count:
            count[item] = brown_tags.count(item)
            taglist.add(item)
        else:
            count[item] = brown_tags.count(item)+count[item]
    for item in set(total_list):
        if item not in count_1:
            count_1[item] = total_list.count(item)
        else:
            count_1[item] = total_list.count(item)+count_1[item]
    for i in range(len(total_list)):
        e_values[(brown_words_rare[i],brown_tags[i])]=math.log(float(count_1[total_list[i]])/float(count[brown_tags[i]]),2)

    print e_values['*', '*']
    print e_values['Place', 'VERB']
    print e_values['prime', 'ADJ']
    print e_values['STOP', 'STOP']
    print e_values['_RARE_', 'VERB']
    return e_values, taglist



# This function takes the output from calc_emissions() and outputs it
def q4_output(e_values, filename):
    outfile = open(filename, "w")
    emissions = e_values.keys()
    emissions.sort()
    for item in emissions:
        output = " ".join([item[0], item[1], str(e_values[item])])
        outfile.write(output + '\n')
    outfile.close()



def main():
    # start timer
    time.clock()

    # open Brown training data
    infile = open(DATA_PATH + "Brown_tagged_train.txt", "r")
    brown_train = infile.readlines()
    infile.close()

    # split words and tags, and add start and stop symbols (question 1)
    brown_words, brown_tags = split_wordtags(brown_train)

    # calculate tag trigram probabilities (question 2)
    q_values = calc_trigrams(brown_tags)

    # question 2 output
    q2_output(q_values, OUTPUT_PATH + 'B2.txt')

    # calculate list of words with count > 5 (question 3)
    known_words = calc_known(brown_words)

    # get a version of brown_words with rare words replace with '_RARE_' (question 3)
    brown_words_rare = replace_rare(brown_words, known_words)

    # question 3 output
    q3_output(brown_words_rare, OUTPUT_PATH + "B3.txt")

    # calculate emission probabilities (question 4)
    e_values, taglist = calc_emission(brown_words_rare, brown_tags)

    # question 4 output
    q4_output(e_values, OUTPUT_PATH + "B4.txt")

    # delete unneceessary data
    del brown_train
    del brown_words_rare

    # open Brown development data (question 5)
    infile = open(DATA_PATH + "Brown_dev.txt", "r")
    brown_dev = infile.readlines()
    infile.close()

    # format Brown development data here
    brown_dev_words = []
    for sentence in brown_dev:
        brown_dev_words.append(sentence.split(" ")[:-1])

    # do viterbi on brown_dev_words (question 5)
    viterbi_tagged = viterbi(brown_dev_words, taglist, known_words, q_values, e_values)

    # question 5 output
    q5_output(viterbi_tagged, OUTPUT_PATH + 'B5.txt')

    # do nltk tagging here
    nltk_tagged = nltk_tagger(brown_words, brown_tags, brown_dev_words)

    # question 6 output
    q6_output(nltk_tagged, OUTPUT_PATH + 'B6.txt')

    # print total time to run Part B
    print "Part B time: " + str(time.clock()) + ' sec'

if __name__ == "__main__": main()











