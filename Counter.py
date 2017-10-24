# -*- coding: utf-8 -*-
'''
Created on July 10, 2017
@author: jiajieyan
'''
from collections import defaultdict

class Counter:
    
    def __init__(self, baselen, toplen, padlen):
        ''' This class provides all counting methods.    
          -n: the length of the base ngrams
          -m: the top length that user wants to increment to
          -l: the string length the user wants to wrap the file IDs and end positions of ngrams
        '''
        self.n = baselen
        self.m = toplen
        self.l = padlen

    def pad(self, ID, end):
        ''' Pad ID number and end-position into string by given padlen.
    
        Each ngram has ID and end-position pairs, which are wrapped into a single string
        with a given padlen. E.g., ID 540 and position 12 will be padded into "0054000012" 
        with padlen 5. If that ngram appears in another file, like ID 673 and position 319, 
        this pair will be appended to former one: "00540000120067300319".This data form is 
        memory saving and easy to retrieve.
        '''
        return ID + str(end).zfill(self.l)
       
    def count(self, ID, words):
        ''' Count baselen ngrams from one file.'''
        subdict = defaultdict(str)
        for i in xrange(len(words) - self.n + 1):
            ngram = ' '.join(words[i : i + self.n])
            subdict[ngram] += self.pad(ID, i + self.n - 1)                                  
        return subdict
    
    def aggregate(self, dictlist):
        ''' Aggregate sub-basegrams from all processes into one.'''
        print 'Aggregating basegrams...'
        ngrams = defaultdict(str)
        for subdict in dictlist:
            for ngram, id_end in subdict.iteritems():
                ngrams[ngram] += id_end            
        return ngrams
                                   
    def __call__(self, args):
        '''This function is called by Counter() instance.'''
        return self.count(*args)
