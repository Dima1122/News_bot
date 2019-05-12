# -*- coding: utf-8 -*-
"""
Created on Sat May 11 20:57:00 2019

@author: User
"""

import pandas as pd
import numpy as np
from gensim.models import KeyedVectors
from annoy import AnnoyIndex
import re 
import pymorphy2 
from functools import lru_cache

@lru_cache(maxsize=100000) # с кешом! 
def get_normal_form (i):
    morph = pymorphy2.MorphAnalyzer()
    return morph.normal_forms(i)[0] 

@lru_cache(maxsize=100000)
def normalize_text(x): 
    return ' '.join([get_normal_form(i) for i in re.findall('\w+', x)])


def mean_sentence(text, my_model):
    vec_sentence = np.zeros(300)
    i = 0
    for sentence in text:
        for word in sentence:
            try:
                vec_sentence += my_model[word]
                i +=1
            except KeyError:
                i +=1
                continue
    return vec_sentence/i

def get_news(text):
    text = normalize_text(text)
    text = [text.split()]    
    data = pd.read_pickle("small_data.pkl") 
    d1 = dict() 
    d2 = dict()
    i = 0
    for d in data:
        d1.update({i: d['text']})
        d2.update({i: d['tokens_wo_upper']})
        i+=1      
    del data 
    my_model = KeyedVectors.load(r'C:\Users\User\Documents\python_tasks\AtomML\hackaton\w2v\my_model')
    NUM_TREES = 15 
    VEC_SIZE_EMB = 300 
    
    counter = 0 
    index_title_emb = AnnoyIndex(VEC_SIZE_EMB) 
    vec_text = mean_sentence(text, my_model)
    for i in d2.keys():
        title_vec = mean_sentence(d2[i], my_model) 
    
        index_title_emb.add_item(counter, title_vec) # Кладем в анной  
        counter += 1 
    index_title_emb.build(NUM_TREES) 
    annoy_res = list(index_title_emb.get_nns_by_vector(vec_text, 1, include_distances=True)) 
    result = list()
    for i in annoy_res[0]:
        result.append(d1[i])
    result = '\n\n'.join(result)
    return result
    
    
    