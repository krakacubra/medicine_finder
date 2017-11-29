import pandas as pd
import re
from collections import Counter
import string
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords


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



drugs_coded = pd.read_csv("Drugs_coded.csv", sep=';', encoding='utf-8')
patients_data = pd.read_csv("AG_2010_2015_NewFormatDate.csv", sep=';', encoding='utf-8')
drugs_coded_dictionary = make_dictionary(drugs_coded)
pd.DataFrame(columns=['registration_number', 'data', 'med', 'code']).to_csv("result.csv", sep=';')
# for j in range(30):
for j in range(len(patients_data)):
    med = set()
    med_code = set()
    if patients_data['Рекомендации'][j] != '-':
        x = str(patients_data['Рекомендации'][j]).lower().split('\\n')
        for i in range(len(x)):
            med_syn = []
            if x[i] != '':
                for k in drugs_coded_dictionary.keys():
                    if re.search(drugs_coded_dictionary.get(k)[0], x[i]) is not None:
                        med_syn.append(k)
                med_syn.sort(reverse=True)
                for value in med_syn:
                    for element in med_syn:
                        if value != element and value.find(element) != -1:
                            med_syn.remove(element)
                for k in med_syn:
                    if drugs_coded_dictionary.get(k)[3] == 2:
                        med.add(drugs_coded_dictionary.get(k)[1])
                        med_code.add('{:.0f}'.format(drugs_coded_dictionary.get(k)[2]))
    pd.DataFrame(columns=[patients_data['Рег.№'][j], patients_data['Дата приема'][j], '|'.join(med),
                          '|'.join(med_code)]).to_csv('result.csv', sep=';', mode='a')
