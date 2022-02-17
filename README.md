# Програмний модуль narrativeExtractor | Вступ

**Програмний модуль narrativeExtractor – "Програмний модуль виокремлення ключових термінів (слів і словосполучень) з тематичних текстових потоків"**, який написаний мовою програмування `Python`, призначений для попередньої обробки природомовних текстових даних поданих українською, російською, англійською, івритом та китайською мовою, що включає токенізацію тексту та видалення стоп-слів, і подальше виокремлення ключових слів і словосполучень з тематичних текстових потоків за допомогою застосування більш широкої обробки природної мови, що базується на розбитті на частини мови – Part-of-speech tagging, та кінцевого статистичного зважування термінів за допомогою глобальної частоти терміну — GTF (Global Term Frequency) з урахуванням тегів, отриманих після Part-of-speech tagging.


### Зміст
- [Позначення та найменування програмного модуля](#name)
- [Програмне забезпечення, необхідне для функціонування програмного модуля](#software)
- [Функціональне призначення](#function)
- [Опис логічної структури](#structure)
- [Використовувані технічні засоби](#hardware)
- [Виклик та завантаження](#run)

<a name="name"></a>
<h2>Позначення та найменування програмного модуля</h2>

Програмний модуль має позначення **"narrativeExtractor"**.

Повне найменування програмного модуля – **"Програмний модуль виокремлення ключових термінів (слів і словосполучень) з тематичних текстових потоків"**.

<a name="software"></a>
<h2>Програмне забезпечення, необхідне для функціонування програмного модуля</h2>

Для функціонування програмного модуля, написаного мовою програмування `Python`, необхідне наступне програмне забезпечення, пакети та моделі:

- `python 3.8.0` or newer [v3.8.0](https://www.python.org/downloads/release/python-380/)
- `Stanza` [v.1.3.0](https://pypi.org/project/stanza/1.3.0/)
- `Stop-words` [v.2018.7.23](https://pypi.org/project/stop-words/2018.7.23/)
- `fastText` [v9.0.2](fhttps://github.com/facebookresearch/fastText)
- `nltk` [v3.7](https://pypi.org/project/nltk/3.7/)
- [lid.176.ftz](https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.ftz)
- `uk`, `ru`, `en`, `he` та `lzh` [models](https://stanfordnlp.github.io/stanza/available_models.html), які необхідно інсталювати виконавши нступний програмний код;
```python
import stanza

stanza.download("uk")
stanza.download("ru")
stanza.download("en")
stanza.download("lzh")
stanza.download("he")
```

<a name="function"></a>
<h2>Функціональне призначення</h2>

Програмний модуль **"narrativeExtractor"** для попередньої обробки природомовних текстових даних поданих українською, російською, англійською, івритом та китайською мовою, що включає токенізацію тексту та видалення стоп-слів, і подальше виокремлення ключових слів і словосполучень з тематичних текстових потоків за допомогою застосування більш широкої обробки природної мови, що базується на розбитті на частини мови – Part-of-speech tagging, та кінцевого статистичного зважування термінів за допомогою глобальної частоти терміну — [GTF (Global Term Frequency)](http://odmytrenko.tilda.ws/2018paper6) з урахуванням тегів, отриманих після Part-of-speech tagging.

<a name="structure"></a>
<h2>Опис логічної структури</h2>

Програмний модуль складається з частин:
- `load_models` — функції завантаження мовних моделей бібліотеки `Stanza` для української, російської, англійської, івриту та китайської мови з використанням [Pipeline](https://stanfordnlp.github.io/stanza/pipeline.html) конвеєра бібліотеки `Stanza`
- Зчитування за допомогою `input()` вхідних тематичних текстових даних поданих у форматі:
```txt
<вхідний текст 1>
***
<вхідний текст 2>
***
.
.
.
***
<вхідний текст n>
```
- `split` — функції розбиття вхідного потоку текстових повідомлень на окремі повідомлення
- `lang_detect` — функції визначення мітки мови вхідних текстових даних
- `nlp_stopword` — функції завантаження необхідної моделі та списку стоп-слів для відповідної попередньо визначеної мітки мови: української, російської, англійської, івриту та китайської
- Попередньої комп'ютеризованої обробки віхідних тематичних текстових потоків за допомогою функцій бібліотеки `Stanza`
- `most_freq_key_terms` — функції визначення найбільш частотних термінів (за замовчуванням `top = 12` — топ 12 слів, топ 12 біграм та топ 12 триграм) за допомогою глобальної частоти терміну `GTF`
- Виводу даних за допомогою команди `print` у вихідний потік у форматі: 
```txt
<вхідний текст 1>
слово, слово2, ..., слово12
біграма1, біграма2, ..., біграма12
триграма1, триграма2, ..., трирама12
***
<вхідний текст 2>
слово1, слово2, ..., слово12
біграма1, біграма2, ..., біграма12
триграма1, триграма2, ..., трирама12
***
.
.
.
***
<вхідний текст n>
слово1, слово2, ..., слово12
біграма1, біграма2, ..., біграма12
триграма1, триграма2, ..., трирама12
***
```


Програмний модуль **"narrativeExtractor"** зчитує вхідний потік текстових даних та за допомогою функції `Pipeline` бібліотеки `Stanza` здійснює послідовну обробку отриманого на вхід природомовного тексту, виокремлює ключові слова, біграми та триграми та здійснює їх статистичне зважування за допомогою глобальної частоти терміну `GTF` й вивід найбільш частотних у вигляді трьох списків: список слів, список біграм та список триграм.
