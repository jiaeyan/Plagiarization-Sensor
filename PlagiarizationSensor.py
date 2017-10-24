# -*- coding: utf-8 -*-
'''
Created on July 10, 2017
@author: jiajieyan
'''

from multiprocessing import Pool
from Counter import Counter
from Incrementor import Incrementor

# This module deals with N-grams collection and displays all longest possible ngrams 
# that appear in more than 1 file. 

class PlagiarizationSensor:
    '''This class executes the multiprocessing module and calls the functions to aggregate and increment.
         -input_path: the path to data source
         -baselen, toplen, padlen: the same as Counter class
    '''
    def __init__(self, data, baselen, toplen):
        self.id_t, self.id_w, padlen = self.get_padlen(data)
        self.counter = Counter(baselen, toplen, padlen)
        self.incrementor = Incrementor(baselen, toplen, padlen)
        
    def get_padlen(self, data):
        '''Get the max between len(data) and longest text to decide how many digits needed to pad doc info string.'''
        print 'Calculating padlen...'
        padlen = len(str(max([len(data), max([len(words) for words in data.itervalues()])])))
        id_t = {str(ID).zfill(padlen):t for ID, t in enumerate(data, 1)}
        id_w = {ID:data[id_t[ID]] for ID in id_t}        
        data.clear()
        return id_t, id_w, padlen
    
    ''' Executes multiprocessing. Map the "count" function of Counter class to ID:words pairs. 
          -num_workers: how many processes user wants to use
          -chunksize: how many pairs the user wants to pass to each process a time. For large number
                      of pairs, choosing a big chunksize improves speed (e.g., for 10000 pairs 100 is the best)
    '''                  
    def multi_map(self, num_workers, chunksize):
        print 'Mapping data and counting basegrams...'
        p = Pool(processes = num_workers)
        result = p.imap(self.counter, self.id_w.iteritems(), chunksize) # returns an iterator "res"
        p.close()
        p.join()
        return (subdict for subdict in result if subdict) # some subdict may be empty    
    
    ''' Generate a CSV file for all lengths ngrams.'''
    def generateCSV(self, ngrams, out_f):
        print 'Generating the result file...'
        step = self.counter.l * 2
        with open(out_f, 'w') as f:
            f.write('Length,Ngram,Callhits,CallIDs\n')
            for length, subgrams in ngrams.iteritems():
                for ngram, id_end in subgrams.iteritems():
                    if id_end == '': continue
                    ids = [self.id_t[id_end[i : i + self.counter.l]] for i in xrange(0, len(id_end), step)]
                    f.write('{0},{1},{2},{3}\n'.format(length, ngram, len(set(ids)), '  '.join(ids)))
    
    ''' A start function to begin everything.'''                
    def collect(self, out_f, num_workers, chunksize):
        map_res = self.multi_map(num_workers, chunksize)
        basegrams = self.counter.aggregate(map_res)
        result = self.incrementor.increment(basegrams, self.id_w)
        self.generateCSV(result, out_f)
        print 'Done!'

    def __call__(self, out_f, **mp_args):
        self.collect(out_f, **mp_args)
