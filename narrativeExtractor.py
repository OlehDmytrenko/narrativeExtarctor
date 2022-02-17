# -*- coding: utf-8 -*-
"""
Created on Wed May  5 10:32:58 2021
Edited on Mon Oct  4 20:43:55 2021
Edited on Mon Feb  7 05:45:53 2022
Edited on Wed Feb  16 15:23:25 2022

@author: Олег Дмитренко

"""
import io
import stanza
from stop_words import get_stop_words
import fasttext
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

def built_words(sent, Words, SW):
    WordsTags = []
    sentTermsTags = []
    for word in sent.words:
        i = word.lemma
        j = word.upos
        if j=='PROPN':
            j = 'NOUN'
        WordsTags.append((i,j))
        if (i not in SW) and (j == 'NOUN'): 
            sentTermsTags.append((i,j)) #without stop words
            Words.append(i)
    return WordsTags, sentTermsTags, Words

def built_bigrams(WordsTags, sentTermsTags, Bigrams, my_stop_words):
    bigramstags = []
    for i in range(1, len(WordsTags)):
        w1 = WordsTags[i-1][0]
        w2 = WordsTags[i][0]
        t1 = WordsTags[i-1][1]
        t2 = WordsTags[i][1]
        if (t1 == 'ADJ') and (t2 == 'NOUN') and (w1 not in my_stop_words) and (w2 not in my_stop_words):
            sentTermsTags.insert([index for index, value in enumerate(sentTermsTags) if value == (w2,t2)][-1], (w1+'_'+w2, t1+'_'+t2))
            bigramstags.append((w1+'_'+w2, t1+'_'+t2))
            Bigrams.append(w1+'_'+w2)
    return sentTermsTags, bigramstags, Bigrams

def built_threegrams(WordsTags, sentTermsTags, Threegrams, my_stop_words):
    threeramstags = []
    for i in range(2, len(WordsTags)):
        w1 = WordsTags[i-2][0]
        w2 = WordsTags[i-1][0]
        w3 = WordsTags[i][0]
        t1 = WordsTags[i-2][1]
        t2 = WordsTags[i-1][1]
        t3 = WordsTags[i][1]
        if (t1 == 'NOUN') and ((t2 == 'CCONJ') or (t2 == 'ADP')) and (t3 == 'NOUN') and (w1 not in my_stop_words) and (w3 not in my_stop_words):
            sentTermsTags.insert([index for index, value in enumerate(sentTermsTags) if value == (w1,t1)][-1], (w1+'_'+w2+'_'+w3, t1+'_'+t2+'_'+t3))
            threeramstags.append((w1+'_'+w2+'_'+w3, t1+'_'+t2+'_'+t3))
            Threegrams.append(w1+'_'+w2+'_'+w3)
        elif (t1 == 'ADJ') and (t2 == 'ADJ') and (t3 == 'NOUN') and (w1 not in my_stop_words) and (w2 not in my_stop_words) and (w3 not in my_stop_words):
            sentTermsTags.insert([index for index, value in enumerate(sentTermsTags) if value == (w2+'_'+w3,t2+'_'+t3)][-1], (w1+'_'+w2+'_'+w3, t1+'_'+t2+'_'+t3))
            threeramstags.append((w1+'_'+w2+'_'+w3, t1+'_'+t2+'_'+t3))
            Threegrams.append(w1+'_'+w2+'_'+w3)
    return sentTermsTags, threeramstags, Threegrams

def nlp_processing(text):
    sentsTermsTags = [] #list of targed sentenses (list of lists of targed words)
    allTermsTags = [] #list of all targed words without division into sentences (only NOUN)    
    Words = []
    Bigrams = []
    Threegrams = []
    doc = nlp(text)
    sents = doc.sentences
    for sent in sents:
        WordsTags, sentTermsTags, Words = built_words(sent, Words, SW)
        if len(WordsTags)>2:
            sentTermsTags, bigramstaggs, Bigrams = built_bigrams(WordsTags, sentTermsTags, Bigrams, SW)
        if len(WordsTags)>3:
            sentTermsTags, threeramstaggs, Threegrams = built_threegrams(WordsTags, sentTermsTags, Threegrams, SW)
        allTermsTags = allTermsTags + [wt for wt in sentTermsTags] 
        sentsTermsTags.append(sentTermsTags)
    return Words, Bigrams, Threegrams

def nlp_stopword(lang):
    if (lang == "ukr") or (lang == "uk"):
        nlp = nlp_ukr
        SW = set(get_stop_words('ukrainian')+(io.open('SW_ukr.txt', 'r', encoding="utf-8").read()).split())
    elif (lang == "rus") or (lang == "ru"):
        nlp = nlp_rus
        SW = set(get_stop_words('russian')+(io.open('SW_eng.txt', 'r', encoding="utf-8").read()).split())
    elif (lang == "eng") or (lang == "en"):
        nlp = nlp_eng
        SW = set(get_stop_words('english')+(io.open('SW_eng.txt', 'r', encoding="utf-8").read()).split())
    elif (lang == "heb") or (lang == "he"):
        nlp = nlp_heb
        SW = (io.open('SW_heb.txt', 'r', encoding="utf-8").read()).split()
    elif (lang == "chn") or (lang == "zh-cn") or (lang == "zh-tw"):
        nlp = nlp_chn
        SW = (io.open('SW_chn.txt', 'r', encoding="utf-8").read()).split()
    return nlp, SW

def lang_detect(message):
    lid_model = fasttext.load_model('lid.176.ftz')
    message = message.replace("\n"," ")
    if message.isspace():
        return ""
    else:
        try:
            # get first item of the prediction tuple, then split by "__label__" and return only language code
            lang = lid_model.predict(message)[0][0].split("__label__")[1]
        except:
            return "en"
    return lang

def load_models():
    nlp_ukr = stanza.Pipeline(lang="uk", processors='tokenize,pos,lemma')
    nlp_rus = stanza.Pipeline(lang="ru", processors='tokenize,pos,lemma')
    nlp_eng = stanza.Pipeline(lang="en", processors='tokenize,pos,lemma')
    nlp_heb = stanza.Pipeline(lang="he", pprocessors='tokenize,pos,lemma')
    nlp_chn = stanza.Pipeline(lang="lzh", processors='tokenize,pos,lemma')
    return nlp_ukr, nlp_rus, nlp_eng, nlp_heb, nlp_chn

if __name__ == "__main__":
    nlp_ukr, nlp_rus, nlp_eng, nlp_heb, nlp_chn = load_models()
    
    text = input()
    messages = text.split('***')
    
    for message in messages:
        print (message)
        lang = lang_detect(message)
        nlp, SW = nlp_stopword(lang)
        
        Words, Bigrams, Threegrams  = nlp_processing(message)
        
        most_freq_key_terms(Words, Bigrams, Threegrams)

        