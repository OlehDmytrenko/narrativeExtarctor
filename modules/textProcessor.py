# -*- coding: utf-8 -*-
"""
Created on Wed Feb  11:45:30 2022

@author: Олег Дмитренко

"""
import fasttext

def built_words(sent, Words, stopWords):
    WordsTags = []
    for word in sent.words:
        i = word.lemma
        j = word.upos
        if j=='PROPN':
            j = 'NOUN'
        WordsTags.append((i,j))
        if (i not in stopWords) and (j == 'NOUN'): 
            Words.append(i)
    return WordsTags, Words

def built_bigrams(WordsTags, Bigrams, stopWords):
    for i in range(1, len(WordsTags)):
        w1 = WordsTags[i-1][0] 
        w2 = WordsTags[i][0]
        t1 = WordsTags[i-1][1]
        t2 = WordsTags[i][1]
        if (t1 == 'ADJ') and (t2 == 'NOUN') and (w1 not in stopWords) and (w2 not in stopWords):
            Bigrams.append(w1+'_'+w2)
    return Bigrams

def built_threegrams(WordsTags, Threegrams, stopWords):
    for i in range(2, len(WordsTags)):
        w1 = WordsTags[i-2][0]
        w2 = WordsTags[i-1][0]
        w3 = WordsTags[i][0]
        t1 = WordsTags[i-2][1]
        t2 = WordsTags[i-1][1]
        t3 = WordsTags[i][1]
        if (t1 == 'NOUN') and ((t2 == 'CCONJ') or (t2 == 'ADP')) and (t3 == 'NOUN') and (w1 not in stopWords) and (w3 not in stopWords):
            Threegrams.append(w1+'_'+w2+'_'+w3)
        elif (t1 == 'ADJ') and (t2 == 'ADJ') and (t3 == 'NOUN') and (w1 not in stopWords) and (w2 not in stopWords) and (w3 not in stopWords):
            Threegrams.append(w1+'_'+w2+'_'+w3)
    return Threegrams

def nl_processing(text, nlpModel, stopWords):
    Words = []
    Bigrams = []
    Threegrams = []
    doc = nlpModel(text)
    sents = doc.sentences
    for sent in sents:
        WordsTags, Words = built_words(sent, Words, stopWords)
        if len(WordsTags)>2:
            Bigrams = built_bigrams(WordsTags, Bigrams, stopWords)
        if len(WordsTags)>3:
            Threegrams = built_threegrams(WordsTags, Threegrams, stopWords)
    return Words, Bigrams, Threegrams

def lang_detect(message, defaultLangs):
    lidModel = fasttext.load_model('lid.176.ftz')
    if message.isspace():
        return "Error! Empty input space! Language of empty input space can not be defined!"
    else:
        try:
            # get first item of the prediction tuple, then split by "__label__" and return only language code
            lang = lidModel.predict(message)[0][0].split("__label__")[1]
        except:
            return "en"
    if lang not in defaultLangs:
        defaultLoader.append_lang(lang, defaultLangs)
        defaultLoader.download_model(defaultLangs)
        defaultLoader.load_stop_words(defaultLangs)
    return lang
