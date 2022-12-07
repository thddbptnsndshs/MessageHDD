from collections import Counter
import pandas as pd
from tqdm import tqdm

class MessageHDD():
    
    def __init__(self, mode='mean', max_len=75, processor=None):
        '''
        args:
            mode -- 'mean' or 'sum', mode of grouping word hdds to get the metric for the whole text
            max_len -- int, actually the limit for the sample size so that the calculation did not break down
            processor -- function that turns str text into list of str tokens
        '''
        self.mode = mode
        self.max_len = max_len
        self.corpus = None
        self.processor = processor
        
    def hdd(self, text, frequency_dict, ntokens_corpus):
        
        def choose(n, k): #calculate binomial
            """
            A fast way to calculate binomial coefficients by Andrew Dalke (contrib).
            """
            if 0 <= k <= n:
                ntok = 1
                ktok = 1
                for t in range(1, min(k, n - k) + 1): #this was changed to "range" from "xrange" for py3
                    ntok *= n
                    ktok *= t
                    n -= 1
                return ntok // ktok
            else:
                return 0

        def hyper(successes, sample_size, population_size, freq): #calculate hypergeometric distribution
            #probability a word will occur at least once in a sample of a particular size
            try:
                prob_1 = 1.0 - (float((choose(freq, successes) * choose((population_size - freq),(sample_size - successes)))) / float(choose(population_size, sample_size)))
                prob_1 = prob_1 * (1/sample_size)
            except ZeroDivisionError:
                prob_1 = 0
            return prob_1
        
        prob_sum = 0.0
        ntokens = len(text)
        types_list = list(set(text))

        for items in types_list:
            prob = hyper(0, min(ntokens, self.max_len), ntokens_corpus, frequency_dict[items]) #random sample is message length
            prob_sum += prob
        if self.mode == 'sum':
            return prob_sum 
        elif self.mode == 'mean':
            try:
                return prob_sum / ntokens
            except:
                return None
            
        elif self.mode == 'root':
            try:
                return prob_sum / ntokens**0.5
            except:
                return None
  
    def fit(self, texts):
        '''
        function that prepares a corpus for the metric calculation
        
        args:
            texts -- list of lists of str or list of str, each list of str or each str corresponds to one text
        returns nothing
        '''
        if len(texts) == 0:
            raise RuntimeError('emply texts list')
            
        if self.processor and type(texts[0]) == str:
            self.texts = pd.Series(texts).apply(self.processor).tolist()
        elif not self.processor and type(texts[0]) == list:
            self.texts = texts
        else:
            raise RuntimeError(f'''text dtype: {type(texts[0])}  
                                   processor {'given' if self.processor else 'not given'}
                                   mismatch; provide a processor function or change dtype''')
            
        if self.corpus:
            self.corpus = self.corpus + sum(self.texts, [])
        else:
            self.corpus = sum(self.texts, [])
            
        self.corpus_frequency_dict = Counter(self.corpus)
        self.ntokens_corpus = len(self.corpus)
        
    def process_corpus(self):
        '''
        calculate the metric for all the texts in the corpus
        '''
        hdds = []

        for text in tqdm(self.texts):
            hdds.append(self.hdd(text, self.corpus_frequency_dict, self.ntokens_corpus))

        return hdds
        
    def calculate(self, text, process_corpus=True):
        '''
        calculates the metric on the provided text
        
        args:
            text -- list of str or str, text to pe processed
        returns:
            the MessageHDD metric for the passed text
        '''
        
        if self.processor and type(text) == str:
            text = self.processor(text)
        elif not self.processor and type(text) == list:
            pass
        else:
            raise RuntimeError(f'''text dtype: {type(texts[0])}  
                                   processor {'given' if self.processor else 'not given'}
                                   mismatch; provide a processor function or change dtype''')

        return self.hdd(text, self.corpus_frequency_dict, self.ntokens_corpus)