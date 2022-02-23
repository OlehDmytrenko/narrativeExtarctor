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
import importPackages
packages = ['io', 'stanza', 'stop_words', 'fasttext', 'nltk']
importPackages.setup_packeges(packages)

import os
import io
import stanza
from stop_words import safe_get_stop_words
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

def nlp_processing(text, nlpModel, stopWords):
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

def load_stop_words(defaultLangs):
    for lang in defaultLangs:
        if lang not in stopWords.keys():
            if os.path.isfile(lang+'.txt'):
                localStopWords = (io.open(lang+'.txt', 'r', encoding="utf-8").read()).split()
            else:
                localStopWords = []
            try:
                stopWords[lang] = set(safe_get_stop_words(lang) + localStopWords)
                print (str(lang) + ' stop words was loaded successfully!')
            except:
                return "Error! Stop words can not be loaded!"      
    return stopWords

def download_model(defaultLangs):
    for lang in defaultLangs:
        if lang not in nlpModels.keys():
            try:
                stanza.download(lang)
                print (str(lang) + ' stanza model was downloaded successfully!')
                
            except:
                return "Error! Language model can not be dowloaded!" 
            try:
                nlpModels[lang] = stanza.Pipeline(lang, processors='tokenize,pos,lemma') 
                print (str(lang) + ' stanza model was loaded successfully!')
            except:
                return "Error! Language model can not be loaded!"       
    return nlpModels

def append_lang(lang):
    try:
        defaultLangs.append(lang)
        with io.open("defaultLangs.csv", "a", encoding="utf-8") as file:
            file.write(lang+'\n')
            file.close()
    except:
        print ('Unexpected Error while adding new languade to default list!')
    return

def lang_detect(message):
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
        append_lang(lang)
        download_model(defaultLangs)
        load_stop_words(defaultLangs)
    return lang

def load_default_stop_words(defaultLangs):
    #checking if list is empty
    if defaultLangs:
        for lang in defaultLangs:
            if os.path.isfile(lang+'.txt'):
                localStopWords = (io.open(lang+'.txt', 'r', encoding="utf-8").read()).split()
            else:
                localStopWords = []
            try:
                stopWords[lang] = set(safe_get_stop_words(lang) + localStopWords)
                print (str(lang) + ' stop words was loaded successfully!')
            except:
                return "Error! Stop words can not be loaded!"
    else:
        print('The <defaultLangs> list is empty!')
        print ('Please, enter below at least one language ! For example, "en" or any other availible at https://fasttext.cc/docs/en/language-identification.html')
        lang = input()
        append_lang(lang)
        load_stop_words(defaultLangs)
    return stopWords

def load_default_models(defaultLangs):
    #checking if list is empty
    if defaultLangs:
        for lang in defaultLangs:
            try:
                nlpModels[lang] = stanza.Pipeline(lang, processors='tokenize,pos,lemma') 
                print (str(lang) + ' stanza model was loaded successfully!')
            except:
                return "Error! Language model is can not be loaded!"
    else:
        print('The <defaultLangs> list is empty!')
        print ('Please, enter below at least one language ! For example, "en" or any other availible at https://fasttext.cc/docs/en/language-identification.html')
        lang = input()
        append_lang(lang)
        download_model(defaultLangs)
    return nlpModels

def load_default_languages():
    try:
        defaultLangs = (io.open("defaultLangs.csv", 'r', encoding="utf-8").read()).split()
    except:
        defaultLangs = ['uk', 'ru', 'en', 'he', 'zh']
    return defaultLangs

if __name__ == "__main__":
    defaultLangs = load_default_languages()   
    nlpModels = dict()
    stopWords = dict()
    nlpModels = load_default_models(defaultLangs)
    stopWords = load_default_stop_words(defaultLangs)
    
    #text = input()
    text = """
    The US warned that there would be severe sanctions if Russia’s military entered Ukrainian territory. The exact details, however, were left intentionally vague.
    The Americans said they did not want to tip their hand. Now Russia has forced their hand. And after White House officials seemed uncertain about how to label Russia’s move, US President Joe Biden was clear. This was the beginning of an invasion and it will be punished as such.
    The sanctions will have a bite - although the US left out some of the most drastic moves, such as cutting Russia out of the Swift banking transaction system or limiting its access to vital microchip technologies.
    Perhaps the biggest news came earlier in the day with the German decision to suspend certification of the Nord Stream 2 pipeline, a move that can at least partially be attributed to US diplomatic efforts.
    Last month, Biden said that if Russia made a “minor incursion” into Ukraine, the US and its allies may struggle to come up with an appropriate response. For the moment, it appears the West is sticking together.
    Biden once again ruled out any US military response, so the diplomatic cards have been the only ones the US can play. In the end, he wasn’t able to stop Russian tanks from rolling in - but the crisis still has room to escalate. And Biden said he still has more punishment the US and its allies can dole out.
    Now, it's Putin’s move.
    ***
    США вводять санкції проти суверенного боргу Росії, а також блокувальні санкції проти російського державного інвестиційного банку VEB та воєнного банку "Промсвязьбанк". Про це у своєму зверненні оголосив американський президент Джо Байден.
    "Хто в ім'я Господа Бога, на думку Путіна, дає йому право оголошувати нові так звані "країни" на території, яка належить сусідам? Це кричуще порушення міжнародного права і вимагає рішучої відповіді міжнародної спільноти", - наголосив Байден, заявивши про санкції у відповідь на визнання Росією самопроголошених "ЛНР та ДНР", що відбулось у понеділок.
    За словами Байдена, відтепер Росія більше не зможе запозичувати гроші на західних ринках і торгувати своїми державними облігаціями. Однак це тільки перший пакет санкцій.
    Американський президент також анонсував санкції проти російських еліт. "Вони також беруть участь в корупційній політиці та мусять страждати", - сказав Байден.
    Рада Федерації дозволила Путіну використовувати російську армію за кордоном
    "Сильно вдарять по Росії". ЄС ввів санкції проти 351 депутата Держдуми
    Росія евакуює своїх дипломатів з України
    За словами Байдена, США також продовжить працювати з Німеччиною над тим, щоб "Північний потік-2" не працював. Напередодні канцлер Німеччини Олаф Шольц доручив призупинити процес сертифікації газопроводу, заявивши, що Росія в своїх діях "зайшла надто далеко".
    Під час свого виступу в Білому домі Байден засудив рішення Росії визнати самопроголошені "ДНР" та ЛНР", а також розкритикував вчорашню промову Путіна, зазначивши, що російський президент хоче переписати історію.
    Байден також прокоментував рішення Ради Федерації, яка у вівторок ввечері дозволила Путіну використовувати російську армії за кордоном.
    "Це робиться для того, щоб виправдати наступні військові дії", - сказав Байден. Він зазначив, що виправдання наступним вторгненням не буде, все ще переконаний в тому, що Росія може почати повномасштабне вторгнення в Україну.
    "Ніщо в його ремарках не свідчило про наявність готовності до діалогу", - додав Байден, пригадуючи вчорашню промову Путіна.
    Однак зазначив, що США та союзники досі готові рухатись дипломатичним шляхом, якщо Росія ставиться до дипломатії серйозно.
    Напередодні ЄС також ввів санкції проти 351 депутата Держдуми, які проголосували минулого тижня за звернення до російського президента Володимира Путіна з пропозицією визнати "ДНР" та "ЛНР", а також проти 27 фізичних та юридичних осіб, які теж "грають роль у підриві чи загрозі територіальної цілісності України, суверенітету та незалежності".
    А Велика Британія оголосила санкції проти п'яти російських банків: "Россия", "ИС Банк", "Генеральний банк", "Промсвязьбанк" і "Черноморский банк".
    За словами Байдена, США продовжать "ескалацію санкцій", якщо Росія продовжить загострювати ситуацію в Україні.
    "Гарячкове марення". Аналітики BBC про виступ Путіна
    Путін доручив відправити російські війська в "ДНР" та "ЛНР"
    ***
    Final approval of the Nord Stream 2 gas pipeline has been put on hold because of Russia's actions in Ukraine, Germany has said.
    The pipeline between Russia and Germany was completed last September but is not yet operating.
    What sanctions are being imposed on Russia?
    What is Nord Stream 2?
    Nord Stream 2 is a 1,200km pipeline under the Baltic Sea, which will take gas from the Russian coast near St Petersburg to Lubmin in Germany.
    It cost €10bn (£8.4bn) and was completed last September. The Russian state-owned energy giant Gazprom put up half of the cost and western energy firms such as Shell and ENGIE of France are paying the rest.
    Nord Stream 2 runs parallel to an existing gas pipeline, Nord Stream, which has been working since 2011.
    Together, these two pipelines could deliver 110bn cubic metres of gas to Europe every year. That is over a quarter of all the gas that European Union countries use annually.
    How has the Ukraine crisis affected Nord Stream 2's future?
    The pipeline does not yet have an operating licence - and Germany has now put this on hold.
    It took the step after Russia formally recognised two breakaway regions in eastern Ukraine, and sent troops there.
    "In light of the most recent developments we must reassess the situation in particular regarding Nord Stream 2," Chancellor Olaf Scholz said.
    US President Joe Biden had previously vowed to shut down Nord Stream 2 if Moscow invades Ukraine, saying "I promise you we will be able to do it".
    Who is against Nord Stream 2?
    The US and UK, along with Russia's neighbours Poland and Ukraine, strongly oppose Nord Stream 2.
    They fear that if were to start operating, it would give Russia even more of a stranglehold over gas supplies to Europe.
    Ukrainian president Volodymyr Zelensky has called Nord Stream 2 "a dangerous political weapon".
    UK Prime Minister Boris Johnson said Europe needs to "snip the drip feed into our bloodstream from Nord Stream".
    In 2006, Russia shut off gas supplies going through Ukraine because of a financial quarrel between the two countries. It caused acute energy shortages during winter in central and eastern Europe.
    There are fears Russia might stop gas supplies in the future for political reasons.
    The US has tried to block Nord Stream 2 before, by imposing sanctions on companies involved in the project. However, it has only targeted Russian firms and not German ones, for fear of damaging diplomatic relations with Berlin.
    Who wants Nord Stream 2?
    Russia is keen to boost supplies of gas to Europe from its vast fields in the west of the country.
    It wants an undersea pipeline to Europe, rather than relying on its land-based pipelines which go through Poland and Ukraine. These pipeline networks are aging and inefficient. Besides this, Poland and Ukraine charge high transit fees.
    Before the Ukraine crisis, Mr Scholz's predecessor Angela Merkel did a lot to try and push through Nord Stream 2.
    Germany already imports 35% of the gas it needs from Russia and she thought Nord Stream 2 would be a way of getting much more Russian gas delivered directly to Germany.
    Many countries fear Russia could hold back gas supplies from Europe for political reasons
    When could Nord Stream 2 start running at the earliest?
    Even before Germany's latest action, the project still faced a big legal hurdle and was unlikely to be delivering any gas before the summer of 2022.
    Germany's regulator had already refused to give it an operating licence because Russian firm Gazprom owns both a 50% stake in the Nord Stream 2 pipeline and all of the gas that would go through it.
    Germany says that gives Russia too much control over supplies and it wants the ownership of the pipeline to be passed to another company.
    ***
    Die Amerikaner erklären geplante Gespräche mit der russischen Regierung vorerst für hinfällig. Erst sagte Außenminister Blinken das Treffen mit seinem Amtskollegen Lawrow ab. Kurz darauf teilte das Weiße Haus mit, derzeit sei kein persönliches Treffen zwischen Biden und Putin geplant.
    Anzeige
    Angesichts der jüngsten Eskalation Moskaus in der Ukraine-Krise plant das Weiße Haus vorerst kein persönliches Treffen von US-Präsident Joe Biden und Russlands Präsident Wladimir Putin. „Derzeit ist das sicher nicht geplant“, sagte Bidens Sprecherin Jen Psaki am Dienstagabend (Ortszeit) in Washington.
    Biden sei grundsätzlich offen für Diplomatie und Gespräche auf höchster Ebene. Aber aktuell, da Putin die Invasion eines souveränen Landes vorantreibe, sei nicht der richtige Zeitpunkt dafür.
    In den vergangenen Tagen war ein persönliches Treffen von Biden und Putin im Gespräch gewesen. Die Initiative für einen solchen Gipfel ging vom französischen Präsidenten Emmanuel Macron aus, der am Sonntag zweimal Putin und einmal mit Biden telefoniert hatte. Biden hatte nach Angaben des Weißen Hauses „im Prinzip“ einem Treffen zugestimmt, auch der Kreml hatte sich offen dafür gezeigt.
    Blinken sagt Lawrow schriftlich ab
    Wegen der jüngsten Entscheidungen Putins in der Ukraine-Krise hatte am Dienstag jedoch auch US-Außenminister Antony Blinken ein für diesen Donnerstag in Genf geplantes Treffen mit seinem russischen Amtskollegen Sergej Lawrow abgesagt.
    US-Präsident Joe Biden und Russlands Präsident Wladimir Putin bei ihrem Treffen im Juni 2021 in Genf
    Quelle: REUTERS
    Blinken sagte, mit Blick auf das Vorgehen Moskaus habe es keinen Sinn, an dem ursprünglich für diese Woche in Genf angesetzten Gespräch mit seinem Kollegen Lawrow festzuhalten. Die US-Regierung sei grundsätzlich weiter zu diplomatischen Gesprächen bereit. Doch die russische Regierung müsse zeigen, dass es ihr ernst sei. „Die vergangenen 24 Stunden haben das Gegenteil gezeigt.“
    Lesen Sie auch
    Psaki betonte: „Wir werden die Tür zur Diplomatie nie ganz schließen.“ Das habe auch Blinken nicht getan. Nötig sei aber eine Kursänderung Moskaus. Es habe nie konkrete Pläne oder einen Zeitplan für ein weiteres Treffen der beiden Präsidenten gegeben. All dies hätte bei dem Treffen von Blinken und Lawrow am Donnerstag besprochen werden sollen. Und dazu komme es nun nicht.
    Anzeige
    Blinken habe Lawrow ein Schreiben gesendet, in dem er ihm die Absage mitteile, sagte Blinken nach einer Zusammenkunft mit dem ukrainischen Außenminister Dmytro Kuleba in Washington.
    Lesen Sie auch
    Putin hatte am Montag die Unabhängigkeit der Separatistenregionen Donezk und Luhansk in der Ostukraine anerkannt. Der Kremlchef ordnete eine Entsendung russischer Soldaten an. Er plant damit zum zweiten Mal nach 2014 einen Einmarsch in die Ukraine. Der Westen wirft ihm vor, damit gegen das Völkerrecht zu verstoßen.
    """
    messages = text.split('***')
    
    for message in messages:
        message = message.replace("\n"," ") #delete all \n from input message
        print (message)
        lang = lang_detect(message)
        print (lang)
        
        Words, Bigrams, Threegrams  = nlp_processing(message, nlpModels[lang], stopWords[lang])
        
        most_freq_key_terms(Words, Bigrams, Threegrams)

        