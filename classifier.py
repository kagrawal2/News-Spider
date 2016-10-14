from textblob.classifiers import NaiveBayesClassifier
import re
import csv
from nltk.corpus import stopwords

cachedStopWords = set(stopwords.words('english'))


with open('classifier.csv', 'r',  newline='', encoding = "cp1252") as f:
    reader = csv.reader(f, delimiter=',')
    titles = list(reader)

def cleanText(string):
    removeStop = " ".join((filter(lambda word: word.lower() not in cachedStopWords, string.split())))
    return re.sub(r'([^\s\w]|_)+', '', removeStop)

training_data = []

for title in titles[1:]:
    if title[0] != '':
        training_data.append((cleanText(title[0]), 'obj'))
    if title[1] != '':
        training_data.append((cleanText(title[1]), 'sub'))

# print(training_data)
cl = NaiveBayesClassifier(training_data)

test = cl.classify("cool features")   
x = cl.accuracy(training_data)
print(test)
print(x)
cl.show_informative_features(10)


