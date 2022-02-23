# -*- coding: utf-8 -*-
"""
Created on Wed Feb  11:45:30 2022

@author: Олег Дмитренко

"""
from nltk import FreqDist

def most_freq(keyTerms, top):
    mostFreqKeyTerms = ''
    fdist = FreqDist(word.lower() for word in keyTerms)
    for (term, freq) in fdist.most_common(top):
        mostFreqKeyTerms = mostFreqKeyTerms + term  + ', ' 
    return mostFreqKeyTerms[:-2]

def most_freq_key_terms(Words, Bigrams, Threegrams, top = 12):
    print (most_freq(Words,top))
    print (most_freq(Bigrams, top))
    print (most_freq(Threegrams,top))
    print ('***')
    return
