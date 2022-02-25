# -*- coding: utf-8 -*-
"""
Created on Wed May  5 10:32:58 2021
Edited on Mon Oct  4 20:43:55 2021
Edited on Mon Feb  7 05:45:53 2022
Edited on Wed Feb  16 15:23:25 2022
Edited on Thu Feb  22 06:07:42 2022
Edited on Wed Feb  23 05:23:30 2022

@author: Олег Дмитренко

"""

from modules import defaultLoader, textProcessor, termsRanker
import sys

if __name__ == "__main__":
    #txtFileDir = '/Users/dmytrenko.o/Documents/GitHub/process_xml/datasets/20210126.txt'
    txtFileDir = sys.argv[1]
    defaultLangs = defaultLoader.load_default_languages()
    exceptedLangs = defaultLoader.load_except_languages()
    nlpModels = defaultLoader.load_default_models(defaultLangs)
    stopWords = defaultLoader.load_default_stop_words(defaultLangs)
    
    with open(txtFileDir, "r", encoding="utf-8") as file:
        messages = (file.read()).split('***')
        for message in messages:
            if message:
                message = message.replace("\n"," ") #delete all \n from input message
                print (message)               
            
                lang = textProcessor.lang_detect(message, defaultLangs, nlpModels, stopWords)
                if (lang in exceptedLangs):
                   continue 
                Words, Bigrams, Threegrams  = textProcessor.nl_processing(message, nlpModels[lang], stopWords[lang])    
                termsRanker.most_freq_key_terms(Words, Bigrams, Threegrams)
