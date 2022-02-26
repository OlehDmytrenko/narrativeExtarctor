# -*- coding: utf-8 -*-
"""
Created on Wed Feb 11:45:30 2022
Edited on Wed Fri 25 10:16:56 2022
Edited on Wed Sat 26 17:08:53 2022

@author: Олег Дмитренко

"""
from modules import defaultLoader
import os
import io
import stanza
from stop_words import safe_get_stop_words

def append_lang(lang, defaultLangs):
    try:
        defaultLangs.append(lang)
        with io.open("defaultLangs.csv", "a", encoding="utf-8") as file:
            file.write(lang+'\n')
            file.close()
    except:
        print ('Unexpected Error while adding new languade to default list!')
    return

def load_stop_words(defaultLangs, stopWords, lang):
    if os.path.isfile(lang+'.txt'):
        localStopWords = (io.open(lang+'.txt', 'r', encoding="utf-8").read()).split()
    else:
        localStopWords = []
    try:
        stopWords[lang] = set(safe_get_stop_words(lang) + localStopWords)
        #print (str(lang) + ' stop words was loaded successfully!')
    except:
        return "Error! Stop words can not be loaded!"      
    return stopWords

def load_default_stop_words(defaultLangs):
    stopWords = dict()
    #checking if list is empty
    if defaultLangs:
        for lang in defaultLangs:
            if os.path.isfile(lang+'.txt'):
                localStopWords = (io.open(lang+'.txt', 'r', encoding="utf-8").read()).split()
            else:
                localStopWords = []
            try:
                stopWords[lang] = set(safe_get_stop_words(lang) + localStopWords)
                #print (str(lang) + ' stop words was loaded successfully!')
            except:
                return "Error! Stop words can not be loaded!"
    else:
        print('The <defaultLangs> list is empty!')
        print ('Please, enter below at least one language ! For example, "en" or any other availible at https://fasttext.cc/docs/en/language-identification.html')
        lang = input()
        append_lang(lang)
        stopWords = load_stop_words(defaultLangs, stopWords)
    return stopWords

def download_model(defaultLangs, nlpModels, lang):
    try:
        stanza.download(lang)
        defaultLoader.append_lang(lang, defaultLangs)
        #print (str(lang) + ' stanza model was downloaded successfully!')    
    except:
        return 'en'
    try:
        nlpModels[lang] = stanza.Pipeline(lang, processors='tokenize,pos,lemma') 
        #print (str(lang) + ' stanza model was loaded successfully!')
    except:
        return None      
    return nlpModels

def load_default_models(defaultLangs):
    nlpModels = dict()
    #checking if list is empty
    if defaultLangs:
        for lang in defaultLangs:
            if lang not in nlpModels.keys():
                try:
                    stanza.download(lang)
                    #print (str(lang) + ' stanza model was downloaded successfully!')   
                except:
                    return "Error! "+str(lang)+" language model can not be dowloaded!" 
            try:
                nlpModels[lang] = stanza.Pipeline(lang, processors='tokenize,pos,lemma') 
                #print (str(lang) + ' stanza model was loaded successfully!')
            except:
                return "Error! "+str(lang)+" language model is can not be loaded!"           
    else:
        print('The <defaultLangs> list is empty!')
        print ('Please, enter below at least one language ! For example, "en" or any other availible at https://fasttext.cc/docs/en/language-identification.html')
        lang = input()
        append_lang(lang)
        nlpModels = download_model(defaultLangs, nlpModels)
    return nlpModels

def load_except_languages():
    try:
        exceptedLangs = (io.open("exceptedLangs.csv", 'r', encoding="utf-8").read()).split()
    except:
        exceptedLangs = ['kv', 'tl', 'bcl', 'xal', 'ba', 'ga']
    return exceptedLangs

def load_default_languages():
    try:
        defaultLangs = (io.open("defaultLangs.csv", 'r', encoding="utf-8").read()).split()
    except:
        defaultLangs = ['uk', 'ru', 'en', 'he', 'zh', 'de']
    return defaultLangs
