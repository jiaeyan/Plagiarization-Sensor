# -*- coding: utf-8 -*-
'''
Created on July 10, 2017
@author: svenyan
'''
from collections import defaultdict

class Incrementor():
    
    def __init__(self, l, n, m):
        self.l = l
        self.n = n
        self.m = m
    
    def increment(self, ngrams, id_w):
        '''Increment the length of ngrams.
        
        Target the basegrams that have >1 filehits, then grow them forward and backward to make
        them longest possible.
        Note: even after incrementing, the result is not clean. It still contains ngrams that
        have empty info or 1 filehits. These ngrams are filtered out when generating the CSV file.      
        '''
        step = self.l * 2
        result = { i:defaultdict(str) for i in xrange(self.n, self.m + 1)}
        print 'Growing basegrams forward...'
        self.grow_right(ngrams, result, id_w, self.n, step)
        print 'Growing basegrams backward...'
        self.grow_left(result, id_w, step)
        return result
    
    def grow_right(self, ngrams, result, id_w, length, step):
        '''Grow the ngrams to the right. Reduce all short ones to the long one.
        
        If current middle length ngram has >1 file hits, add one word at the last of that ngram
        and collect all possible higher length grams grown from that ngram and go on checking; 
        otherwise, roll back to its parent lower length gram and record it.
        '''
        while ngrams:
            ngram, id_end = ngrams.popitem()
            if id_end[:self.l] != id_end[-step:-self.l]:             # if current medium length gram >1 file hits, grow it
                if length == self.m: result[length][ngram] = id_end  # if reaches to toplen, record everything now have, since they are all qualified
                else:
                    hgrams = self.build_hgrams(ngram, id_end, result, id_w, length, step)
                    self.grow_right(hgrams, result, id_w, length + 1, step)              
            elif length == self.n: continue                          # basegrams cannot roll back
            else:
                lgram = ngram[:ngram.rfind(' ')]                     # if =1 file hits, roll back to lower length and record,
                for i in xrange(0, len(id_end), step):               # because that lgram must be qualified
                    ID = id_end[i : i + self.l] 
                    end = int(id_end[i + self.l : i + step])
                    result[length - 1][lgram] += self.pad(ID, end - 1) 
    
    def build_hgrams(self, ngram, id_end, result, id_w, length, step):
        '''Build a high length grams dict grown from one medium length.'''
        hgrams = defaultdict(str)
        for i in xrange(0, len(id_end), step):
            step_info = id_end[i:i+step]
            ID = step_info[:self.l]
            h_end = int(step_info[self.l:]) + 1
            try:                                     # h_end may be out of index
                hgram = ngram + ' ' + id_w[ID][h_end]
                hgrams[hgram] += self.pad(ID, h_end)
            except: result[length][ngram] += step_info
        return hgrams
                    
    def grow_left(self, ngrams, id_w, step):
        '''Grow the ngrams to the left. Reduce all short ones to the long one.
        
        Add one word at the head of current length gram to make it grow, check if that higher
        length ngram exits in the result from right-growth, if yes, check if the position info
        is the same; if yes too, then remove this piece of info from current ngram. 
        '''
        for i in xrange(self.n, self.m):
            for ngram, id_end in ngrams[i].iteritems():
                neo_info = ''             
                for j in xrange(0, len(id_end), step):
                    step_info = id_end[j : j + step]
                    ID = step_info[:self.l]
                    h_start = int(step_info[self.l:]) - i
                    try:                                        # h_start may be out of index
                        hgram = id_w[ID][h_start] + ' ' + ngram
                        if step_info not in ngrams[i + 1][hgram]:
                            neo_info += step_info
                    except: neo_info += step_info
                ngrams[i][ngram] = neo_info