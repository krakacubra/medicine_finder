import pandas as pd
import string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import numpy as np
from nltk.stem.snowball import RussianStemmer
# from regular_findmed import make_dictionary
from pandas import read_csv
import re


def make_dictionary(drugs_coded):
    drugs_coded_dictionary = {}
    for i in range(len(drugs_coded['synonims'])):
        # dc = drugs_coded['synonims'][i].replace('-', '').split('|')
        dc = drugs_coded['synonims'][i].split('|')

        for j in range(len(dc)):
            drugs_coded_dictionary.update({dc[j]: [re.compile(r'\b' + dc[j] + r'\b'), drugs_coded['medicine'][i], drugs_coded['attendant_class'][i],
                                                         drugs_coded['group'][i]]})
        if dc.count(drugs_coded['medicine'][i]) == 0:
            drugs_coded_dictionary.update({drugs_coded['medicine'][i]: [re.compile(r'\b' + drugs_coded['medicine'][i] +
                                                                                   r'\b'), drugs_coded['medicine'][i],
                                                drugs_coded['attendant_class'][i], drugs_coded['group'][i]]})
    return drugs_coded_dictionary


print('open drugs coded file')
drugs_coded = pd.read_csv("Drugs_coded.csv", sep=';', encoding='utf-8')
print('open patients file')
patients_data = pd.read_csv("AG_2010_2015_NewFormatDate.csv", sep=';', encoding='utf-8')
print('making dictionary...')
drugs_coded_dictionary = make_dictionary(drugs_coded)
print('making dictionary ended')
# find_med = pd.read_csv("result (1).csv", sep=';', encoding='utf-8')
data = patients_data['Рекомендации']
stop_words = stopwords.words('russian')
datadata = []
stemmer = RussianStemmer()
print('начало обработки данных...')
# for i in range(10):

for i in range(len(data)):
# deleting drugs
    x = str(data[i]).lower().split('\\n')
    for j in range(len(x)):
        med_syn = []
        if x[j] != '' or x[j] != '-':
            for k in drugs_coded_dictionary.keys():
                if re.search(drugs_coded_dictionary.get(k)[0], x[j]) is not None:
                    med_syn.append(k)
            med_syn.sort(reverse=True)
            for value in med_syn:
                for element in med_syn:
                    if value != element and value.find(element) != -1:
                        med_syn.remove(element)
            for k in med_syn:
                x[j] = x[j].replace(k, '')
    d = "".join(x)
# making preprocesing
    d = "".join(l if l not in string.punctuation and not l.isdigit() else ' ' for l in d).lower()
    text = d.split(" ")
    text1 = [word for word in text if stop_words.count(word) == 0]
    for i in range(len(text1)):
        text1[i] = stemmer.stem(text1[i])
    datadata.append(' '.join(word for word in text1 if len(word) > 2))
print(datadata[:10])
print('конец обработки данных!')
# # тут все ок
print('считаем частоту слов в каждой рекомендации...')
cvectorizer = CountVectorizer(analyzer='word', stop_words=stop_words)
bag_of_words = cvectorizer.fit_transform(datadata)
sum_pd = np.sum(bag_of_words.toarray(), axis=0)
dictionary = dict(zip(cvectorizer.get_feature_names(),sum_pd))
sorted_dictionary = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
pd.DataFrame(sorted_dictionary).to_csv('words_frequency.csv', sep=';')
print('считаем веса слов в каждой рекомендации...')
tfidf_vectorizer = TfidfVectorizer()
weighted_words = tfidf_vectorizer.fit_transform(datadata)
a_weighted_words = weighted_words.toarray()
res = np.sum(a_weighted_words, axis=0)
count = np.count_nonzero(a_weighted_words, axis=0)
tfidf_dictionary = dict(zip(tfidf_vectorizer.get_feature_names(),[res[i]/count[i] for i in range(a_weighted_words.shape[1])]))
tfidf_sorted_dictionary = sorted(tfidf_dictionary.items(), key=lambda x: x[1], reverse=True)
print(type(tfidf_sorted_dictionary))
pd.DataFrame(tfidf_sorted_dictionary).to_csv('tfidf_words_weight.csv', sep=';')