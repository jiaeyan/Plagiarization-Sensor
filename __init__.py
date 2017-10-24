# -*- coding: utf-8 -*-
'''
Created on July 10, 2017
@author: jiajieyan
'''
from nltk.corpus import reuters
from LongestNgramsCollector import PlagiarizationSensor
import string

def read():
    '''A toy test with NLTK's Reuters corpus.'''
    print 'Reading source data...'
    t_w = {}
    ps = set([c for c in string.punctuation + ' '])
    for fid in reuters.fileids():
        txt = ' '.join([clean(word, ps) for word in reuters.words(fid) if word not in ps])
        t_w[fid] = txt.split()  
    return t_w 
          
def clean(word, ps):
    '''Clean up the texts.'''        
    for p in ps: word = word.replace(p, '')
    return word

if __name__ == '__main__':
    data = read()
    out_f = 'your/path/result.csv'
    collector = PlagiarizationSensor(data, baselen = 10, toplen = 50)
    collector(out_f, num_workers = 3, chunksize = 100)
