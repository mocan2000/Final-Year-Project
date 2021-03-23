import sys
import re 
import nltk
import string
from nltk.classify import *
from nltk.corpus import stopwords
import nltk.classify.util
import pickle
import random
from nltk.stem import WordNetLemmatizer
import codecs
from nltk import word_tokenize

def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)


def preprocess(tweet):
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','AT_USER',tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')
    tweet = word_tokenize(tweet)
    tweet = [word.lower() for word in tweet if word.isalpha()]
    return tweet

def getStopWordList(FileName):
#read the stopwords file and build a list
    stopWords = []
    #stopWords.append('TWITTER_USER')
    stopWords.append('URL')
 
    fp = open('StopWords.txt', 'r', encoding='utf-8')
    line = fp.readline()
    while line:
        word = line.strip()
        stopWords.append(word)
        line = fp.readline()
    fp.close()
    return stopWords


st = open('StopWords.txt', 'r', encoding='utf-8')
stopWords = getStopWordList('StopWords.txt')

# Remove stopwords and lemmatize words and normalize
def normalize(tweet):
    tweet = [word for word in tweet if word not in stopWords]
    tweet =[replaceTwoOrMore(word) for word in tweet]
    lemmatizer = WordNetLemmatizer()
    lemmWords = [lemmatizer.lemmatize(word) for word in tweet]
    return lemmWords

#tokenising the tweets
def format_sentence(tweet):
    return({word: True for word in tweet})

posTweet = []
with codecs.open('pos_tweets.json', "r",encoding='utf-8', errors='ignore') as f:
    for tweet in f:
        processedTweet = preprocess(tweet)
        featureVector = normalize(processedTweet)
        posTweet.append([format_sentence(featureVector), 'Non-violation'])
 
negTweet = []
with codecs.open('neg_tweets.json', "r",encoding='utf-8', errors='ignore') as f:
    for tweet in f:
        processedTweet = preprocess(tweet)
        featureVector = normalize(processedTweet)
        negTweet.append([format_sentence(featureVector), 'Violation'])

 
# splitting labelled data into the training and test data
training =posTweet[:int((.8)*len(posTweet))] + negTweet[:int((.8)*len(negTweet))]
test =posTweet[int((.8)*len(posTweet)):] + negTweet[int((.8)*len(negTweet)):]

#training = nltk.classify.apply_features(extractFeatures, tweets)
classifier = nltk.NaiveBayesClassifier.train(training)

#Storing the trained classifier in a pickle file
##f = open('trained_classifier.pickle', 'wb')
##pickle.dump(classifier, f)
##f.close()

# Ten fold validationtesting 
numFolds = 10
subsetSize = int (len(training)/numFolds)
for i in range(numFolds):
    testing_this_round = training[i*subsetSize:][:subsetSize]
    training_this_round = training[:i*subsetSize] + training[(i+1)*subsetSize:]
    foldClassifier = nltk.NaiveBayesClassifier.train(training_this_round)
    foldAccuracy = nltk.classify.accuracy(classifier, testing_this_round)
    totalTest = foldAccuracy * 100 
    print('\n Ten-fold validation of the NaiveBayes classifier: %4.2f' % totalTest)
    
print()
print()   
#showing the  most informative features
classifier.show_most_informative_features(10)


##Calculating the Accuracy of the Test Set
accuracyTestSet = nltk.classify.accuracy(classifier, test) 

# #Printing the accuracy for the test set  
totalTest = accuracyTestSet * 100 
print ('\nNaive Bayes Accuracy with the Test Set: %4.2f' % totalTest) 

print()
print() 
# testing of the NaiveBayes classifier

example1 = "bragged of sexual assault, sold the us to…"
processedTweet = preprocess(example1)
print("Tweet :"+ example1)
print("Classification test Result below")
print(classifier.classify(format_sentence(processedTweet)))

print()
print() 

example2 = "republicans that vote strongly disapprove of daca amnesty."
processedTweet = preprocess(example2)
print("Tweet :"+ example2)
print("Classification test Result below")
print(classifier.classify(format_sentence(processedTweet)))

print()
print() 

example3 = "Happiness is good!" 
processedTweet = preprocess(example3)
print("Tweet :"+ example3)
print("Classification test Result below")
print(classifier.classify(format_sentence(processedTweet)))


