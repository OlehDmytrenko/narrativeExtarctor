# -*- coding: utf-8 -*-
"""
Created on Wed May  5 10:32:58 2021
Edited on Mon Oct  4 20:43:55 2021
Edited on Mon Feb  7 05:45:53 2022
Edited on Wed Feb  16 15:23:25 2022

@author: Олег Дмитренко

"""
import io
import langdetect
from stop_words import get_stop_words
import stanza
from nltk import FreqDist

def keyTerms(Words, Bigrams, Threegrams):
    keyWords = ''
    fdist = FreqDist(word.lower() for word in Words)
    for (word, freq) in fdist.most_common(12):
        keyWords = keyWords + word  + ', ' 
    print (keyWords[:-2])
    
    keyBigrams = ''
    fdist = FreqDist(bigram.lower() for bigram in Bigrams)
    for (bigram, freq) in fdist.most_common(12):
        keyBigrams = keyBigrams + bigram  + ', ' 
    print (keyBigrams[:-2])
    
    keyThreegrams = ''
    fdist = FreqDist(threegram.lower() for threegram in Threegrams)
    for (threegram, freq) in fdist.most_common(12):
        keyThreegrams = keyThreegrams + threegram  + ', ' 
    print (keyThreegrams[:-2])
    
    print ('***')
    return

def built_words(sent, Words, SW):
    WordsTags = [] #
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

def NLP_StopWord(lang):
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

def langDetect(message):
    lang = langdetect.detect(message)
    if ((lang == 'uk') or (lang == 'ru') or (lang == 'en') or (lang == 'he') or (lang == "zh-cn") or (lang == "zh-tw")):
        return lang
    else: 
        return 'en'

def load_models():
    nlp_ukr = stanza.Pipeline(lang="uk", processors='tokenize,pos,lemma')
    nlp_rus = stanza.Pipeline(lang="ru", processors='tokenize,pos,lemma')
    nlp_eng = stanza.Pipeline(lang="en", processors='tokenize,pos,lemma')
    nlp_heb = stanza.Pipeline(lang="he", pprocessors='tokenize,pos,lemma')
    nlp_chn = stanza.Pipeline(lang="lzh", processors='tokenize,pos,lemma')
    return nlp_ukr, nlp_rus, nlp_eng, nlp_heb, nlp_chn

if __name__ == "__main__":
    nlp_ukr, nlp_rus, nlp_eng, nlp_heb, nlp_chn = load_models()
    
    #text = input()
    text = """[CITATION][C] Understanding criminal law
J Dressler, FR Strong, ME Moritz - 1987 - M. Bender
***
[PDF][PDF] Criminal sentences: Law without order
ME Frankel - 1973 - insidepdf.info
The trouble with sentencing is that it s lawless - The New York Times Criminal Sentences: Law 
Without Order. Front Cover. ME Frankel The Culture of Control: Crime and Social Order in Contemporary 
Society · David Garland Criminal sentences law without order, : Marvin E Frankel . Columbia …
***
[CITATION][C] Handbook on criminal law
WR LaFave, AW Scott - 1972 - West Publishing Company
***
[BOOK][B] The sanctity of life and the criminal law
GL Williams, WC Warren - 1958 - epubarea.info
THE SANCTITY OF LIFE and the Criminal Law by Glanville Williams . Full text. Full text is available 
as a scanned copy of the original print version. Get a printable copy (PDF file) of the complete 
article (365K), or click on a page The Sanctity of Life and the Criminal Law Buy the The Sanctity …
***
[BOOK][B] Textbook of criminal law
GL Williams, DJ Baker - 1983 - sinbooksret.com
Sweet & Maxwells Textbook of Criminal Law by Glanville . - Flipkart Download citation Glanville 
Williams T. Glanville Williams Textbook of Criminal Law is an exposition and evaluation of the 
criminal law. Now updated and ?Glanville Williams Textbook of Criminal Law: Dennis Baker …
***
[BOOK][B] Criminal law defenses
PH Robinson, J Grall, M Moskovitz - 1984 - ncjrs.gov
The volumes discuss the proof and disproof of criminal law defenses and the alternative consequences of a successful defense. They set out an overall conceptual framework within which all criminal law defenses can be considered and describe practical implications of …
***
[CITATION][C] A History of English Criminal Law and Its Administration from 1750: The Emergence of Penal Policy
L Radzinowicz - 1948 - Stevens & sons
***
[CITATION][C] Criminal law: The general part
GL Williams - 1953 - Stevens
***
[BOOK][B] International criminal law: cases and commentary
A Cassese, G Acquaviva, M Fan, A Whiting - 2011 - books.google.com
International Criminal Law: Cases and Commentary presents a concise and comprehensive explanation of the development of major areas in substantive international criminal law, through a selection of key illustrative cases from domestic and international jurisdictions"""
    messages = text.split('***')
    
    for message in messages:
        print (message)
        lang = langDetect(message)
        nlp, SW = NLP_StopWord(lang)
        
        Words, Bigrams, Threegrams  = nlp_processing(message)
        
        keyTerms(Words, Bigrams, Threegrams)

        