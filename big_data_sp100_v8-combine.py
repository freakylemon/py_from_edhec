# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 02:51:58 2019

@author: freakylemon
"""

import requests
from bs4 import BeautifulSoup

r = requests.get('http://cdn-hk.evilucifero.com/wiki/S%26P_100')

soup = BeautifulSoup(r.content, 'html.parser')


title = soup.find('title')


tables = soup.find_all('table')

print(tables[0].prettify())

apple_text_elements = soup.findAll(text='Apple Inc.')


apple_element = apple_text_elements[0]

table = apple_element.find_parent('tbody')


links = table.find_all('a')


links = [link.attrs['href'] for link in links]



import numpy as np
links_unique, link_counts = np.unique(links, 
                                      return_counts=True)

links_unique = ['http://cdn-hk.evilucifero.com' + link for link in links_unique]

#######################

index = [x[35:] for x in links_unique]

import re

import nltk

from sklearn.feature_extraction.text import CountVectorizer

import pandas as pd

def get_company_text_multiple(urls):
    text = []
    for url in urls:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        paragraphs = soup.find_all('p')
        paragraphs = [paragraph.text for paragraph in paragraphs]
        paragraphs = ' '.join(paragraphs) #after improve, add index here[:1/2/3]
        pattern = '\[[0-9]+\]'
        paragraphs = re.sub(pattern, '', paragraphs)
        stemmer = nltk.stem.SnowballStemmer('english')
        paragraphs = stemmer.stem(paragraphs)
        text.append(paragraphs)
    vectorizer = CountVectorizer(stop_words='english')
    counts = vectorizer.fit_transform(text)
    counts = pd.DataFrame(counts.toarray(), 
                          columns = vectorizer.get_feature_names()).transpose()
    return counts

counts = get_company_text_multiple(links_unique)
counts.columns = index

'''
7.3 USE ONLY FIRST SEVERAL PARAGRAPHS OF THE DESCRIPTION
'''


#def get_company_text_multiple(urls, paras):
#    text = []
#    for url in urls:
#        r = requests.get(url)
#        soup = BeautifulSoup(r.content, 'html.parser')
#        paragraphs = soup.find_all('p')
##        print(paragraphs)
#        paragraphs = [paragraph.text for paragraph in paragraphs]
#        paragraphs = ' '.join(paragraphs[:paras]) #after improve, add index here[:1/2/3]
#        pattern = '\[[0-9]+\]'
#        paragraphs = re.sub(pattern, '', paragraphs)
#        stemmer = nltk.stem.SnowballStemmer('english')
#        paragraphs = stemmer.stem(paragraphs)
#        text.append(paragraphs)
#    vectorizer = CountVectorizer(stop_words='english')
#    counts = vectorizer.fit_transform(text)
#    counts = pd.DataFrame(counts.toarray(), 
#                          columns = vectorizer.get_feature_names()).transpose()
#    return counts
#
#counts = get_company_text_multiple(links_unique, 3)
#counts.columns = index

'''
TO USE IT, PLEASE UNCOMMENT THE CODE ABOVE
'''



word_frequency = counts.copy()
word_frequency = word_frequency/ word_frequency.sum()


'''
7.1 CHANGE THE METHOD FOR TABLE 'word_frequency'
'''
#idf = pd.DataFrame([1 + np.log(100/ counts[counts>0].count(axis=1))]).transpose()
#idf.columns = ['idf']
#
#word_frequency = counts.copy()
#word_frequency = word_frequency/ word_frequency.sum()
#for i in word_frequency.columns:
#    word_frequency[i] = word_frequency[i]* idf['idf']

'''
TO USE IT, PLEASE UNCOMMENT THE CODE ABOVE
'''









#############################

def findDist(company1, company2):
    return sum((company1-company2)**2)**0.5


'''
7.2 CHANGE THE METHOD FOR PAIRWISE DISTANCE CALCULATION
'''

#def findDist(company1, company2):
#    return (sum(company1 * company2))/((sum(company1**2))**0.5 * (sum(company2**2))**0.5)

'''
TO USE IT, PLEASE UNCOMMENT THE CODE ABOVE
'''


from itertools import combinations
combinations = list(combinations(word_frequency.columns,2))

distance = pd.DataFrame(combinations)
distance.columns = ['Company 1', 'Company 2']

distance['Distance'] = distance.apply(lambda x: findDist(word_frequency[x['Company 1']], 
        word_frequency[x['Company 2']]), axis=1)

temp = distance.copy()
temp.columns = ['Company 2', 'Company 1', 'Distance']
distance = pd.concat([distance, temp])

###############################


def get_company_industries(urls):
    industries_data = []
    for url in urls:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        infobox = soup.find('table', 
                            {'class': 'infobox'})
        industries = [x.text.lower() for x in infobox.find('th',
                      text = 'Industry').parent()[1].find_all('a')]
        industries = pd.Series(1, index = industries)
        industries_data.append(industries)
    industries_data = pd.concat(industries_data, 
                                axis=1,
                                sort=False).fillna(0)
    return industries_data

industries = get_company_industries(links_unique)
industries = industries.transpose()
industries.index = index

# here for certain industry we may extract the corresponding companies
# and get intra-industry distances
# while the inter-industry distance can be obtained through the 
# industry-distance table

# with idea above, we can have, answer to 6.1
# 6.1, could be a line, with the distance intra, another line with distance inter

# so first to achieve the intra distances,,, there's financial services as example,



import seaborn as sns
import matplotlib.pyplot as plt


industry_pack = {}
intra_industry_distance = pd.DataFrame(columns=['Company 1', 'Company 2', 'Distance'])

intra_industry_industry_distance = {}

for indu in list(industries.columns):
    temp = [item for item in industries[industries[indu] == 1].index]
    from itertools import combinations
    combinations = list(combinations(temp,2))    
    industry_pack[indu] = pd.DataFrame(combinations, columns = ['Company 1', 
                 'Company 2'])
#    industry_pack[indu]['Distance']= 0
    industry_pack[indu] = pd.merge(industry_pack[indu], 
                 distance, 
                 on=['Company 1', 'Company 2'])
    temp = industry_pack[indu].copy()
    temp.columns = ['Company 2', 'Company 1', 'Distance']
    industry_pack[indu] = pd.concat([industry_pack[indu],temp],sort=False)
    intra_industry_distance = pd.concat([intra_industry_distance,industry_pack[indu]], 
                                        sort=False)
    print(indu, industry_pack[indu]['Distance'].mean())
    intra_industry_industry_distance[indu] = industry_pack[indu]['Distance'].mean()
# overall components pairwise distance is higher then average intra-industry distance
distance['Distance'].mean() - intra_industry_distance['Distance'].mean()

############################################################################

# to get intra industry distance, and compare it to the overall industry pairwise distance
intra_industry_industry_distance = pd.DataFrame.from_dict(intra_industry_industry_distance, 
                                                          orient='index')
intra_industry_industry_distance.columns = ['Distance']



from itertools import combinations
industry_distances = pd.DataFrame(list(combinations(industries.columns, 2)))
industry_distances.columns = ['Industry 1', 'Industry 2']

def find_industry_distance(key1, key2, distance):
    firms1 = industries[industries[key1]==1].index
    firms2 = industries[industries[key2]==1].index
    i1 = distance['Company 1'].isin(firms1) & distance['Company 2'].isin(firms2)
    i2 = distance['Company 1'].isin(firms2) & distance['Company 2'].isin(firms1)
    i = i1 | i2
    return distance.loc[i]['Distance'].mean()

industry_distances['Distance'] = industry_distances.apply(lambda x: find_industry_distance(x['Industry 1'], 
                  x['Industry 2'], 
                  distance),
        axis=1)
        
temp = industry_distances.copy()
temp.columns = ['Industry 2', 'Industry 1', 'Distance']
industry_distances = pd.concat([industry_distances, temp], sort=False)

# 6.2 
industry_distances['Distance'].mean()-intra_industry_industry_distance['Distance'].mean()



# below to examine, those industries that has the cloest distance to f.s.
top_ind = industry_distances[industry_distances['Industry 1'] == 'financial services'].sort_values(by='Distance').dropna()['Industry 2'].values[:10]
top_ind = ['financial services'] + list(top_ind)

pivot_data = industry_distances.pivot('Industry 1', 
                                      'Industry 2', 
                                      'Distance').reindex(index=top_ind,
                                                columns=top_ind)


plt.figure(figsize=(15,15))
sns.heatmap(pivot_data, cmap='RdYlBu_r', annot=True)
plt.show()