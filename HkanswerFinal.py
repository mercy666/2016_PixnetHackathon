# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 13:02:04 2016

@author: user
"""

import operator
import itertools
import jieba
import logging
import gensim
import multiprocessing
import json
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence,Text8Corpus
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
from keras.models import load_model
import numpy as np
import re
jieba.set_dictionary('dict.txt.big.txt')#繁中字庫
modelnn=load_model('my_model2.h5')
model = gensim.models.Word2Vec.load("w2v_v3.1.model")#載入w2v model
f=open('hackathon_1000.tsv') #範例
count=0
questions=[]
anwser=[]
for line in f:
    #json_data=json.loads(line)
    qlist=line.split('	')
    #sentence=json_data['question']#題目
    #quiz_no = int(m.group(1))
    question = qlist[1]
    options = {}
    answer=qlist[2]
    c=3
    for idx in ['a','b','c','d','e']:
        options[idx] = qlist[c].decode('utf8')
        c=c+1
    question=question.decode('utf8')
    sentence=question.replace(u'\n',u'')#濾掉雜訊
    sentence=sentence.replace(u' ',u'')
    sentence=sentence.replace(u'_',u'')
    sentence=sentence.replace(u'︽⊙＿⊙︽',u' _ ')
    #print sentence
    #print ' '.join(options[x] for x in options)
    words = jieba.cut(sentence, cut_all=False)#斷詞
    words = list(words)
    wd=' '.join([t for t in words if t in model.vocab or t==u'_'])
        
    w_d=wd.split(' ')
    wd=' '.join([t for t in w_d if t!=' '])
    print wd
    w_d=wd.split(' ')
    
    indices = [i for i, x in enumerate(w_d) if x == '_']
    w=[]
    for g in indices:
        w=[' ',' ',' ',' ',' ',' ',' ']
        word_count=0
        w[3]=w_d[g]
        for x in range(1,4):
            if g+x <len(w_d)-1:
                w[3+x]=w_d[g+x]
            if g-x >0:
                w[3-x]=w_d[g-x]
        ans={}
        for x in options:#5個選項
            c1=options[x]
            choices = jieba.cut(c1, cut_all=False)
            choices = list(choices)
            optionlist=[]
            for choice in choices:
                if choice in model.vocab:
                    optionlist.append(choice)
            if len(optionlist)!=0 :
                d700=[]
                for y in w:
                    if y==' ':
                        for y in range(0,100):
                            d700.append(0)
                    elif y==u'_':
                        d700.extend(model[optionlist[0]])
                    else:
                        d700.extend(model[y])
                proba = modelnn.predict_proba(np.array([d700]),batch_size=32)
                print proba[0][1]
                if x not in ans: 
                    ans[x]=proba[0][1]
                else:
                    if proba[0][1]>ans[x]:
                        ans[x]=proba[0][1]
                        
            else:
                ans[x]=0
    #print ans
    a=max(ans.iteritems(), key=operator.itemgetter(1))[0]
    if answer==a:
        count=count+1
        print 'yes'
    else :
        print 'error-------------------------'
        print len(indices)
print count
     
        
        
        
        
        
        