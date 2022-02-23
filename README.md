# Програмний модуль narrativeExtractor | Вступ

**Програмний модуль narrativeExtractor – "Програмний модуль виокремлення ключових термінів (слів і словосполучень) з тематичних текстових потоків"**, який написаний мовою програмування `Python`, призначений для попередньої обробки природомовних текстових даних поданих (за замовчуванням доступні українська, російська, англійська, іврит, китайська та німецька мовні моделі), що включає токенізацію тексту та видалення стоп-слів, і подальше виокремлення ключових слів і словосполучень з тематичних текстових потоків за допомогою застосування більш широкої обробки природної мови, що базується на розбитті на частини мови – [Part-of-speech tagging](https://stanfordnlp.github.io/stanza/pos.html), та кінцевого статистичного зважування термінів за частотою їх появи у тексті.


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

- `Docker` [v20.10](https://docs.docker.com/engine/release-notes/#version-2010)
- `Kubernetes` [v1.22.4](https://github.com/kubernetes/kubernetes/releases/tag/v1.22.4)
- `python 3.8.0` or newer [v3.8.0](https://www.python.org/downloads/release/python-380/)
- `importlib` [v1.0.4](https://pypi.org/project/importlib/1.0.4/)
- `Stanza` [v.1.3.0](https://pypi.org/project/stanza/1.3.0/)
- `Stop-words` [v.2018.7.23](https://pypi.org/project/stop-words/2018.7.23/)
- `fastText` [v9.0.2](https://github.com/facebookresearch/fastText)
- `nltk` [v3.7](https://pypi.org/project/nltk/3.7/)
- [lid.176.ftz](https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.ftz)
- `uk`, `ru`, `en`, `he`, `zh` та `de` [models](https://stanfordnlp.github.io/stanza/available_models.html) для відповідно української, російської, англійської, івриту та китайської мови, які можна інсталювати за бажанням вручну (не вимагається!), виконавши наступний програмний код:
```python
import stanza

stanza.download("uk")
stanza.download("ru")
stanza.download("en")
stanza.download("zh")
stanza.download("he")
stanza.download("de")
```

<a name="function"></a>
<h2>Функціональне призначення</h2>

Програмний модуль **"narrativeExtractor"** для попередньої обробки природомовних текстових даних поданих (за замовчуванням доступні українська, російська, англійська, іврит, китайська та німецька мовні моделі), що включає токенізацію тексту та видалення стоп-слів, і подальше виокремлення ключових слів і словосполучень з тематичних текстових потоків за допомогою застосування більш широкої обробки природної мови, що базується на розбитті на частини мови – [Part-of-speech tagging](https://stanfordnlp.github.io/stanza/pos.html), та кінцевого статистичного зважування термінів за частотою їх появи у тексті.

<a name="structure"></a>
<h2>Опис логічної структури</h2>

Програмний модуль складається з частин:
- `main.py` — головного скрипта, що викликає наступні підмодулі:
	- `packagesImporter.py` — підмодуль, що відповідає за перевірку та завантаження необхідних програмних бібліотек, модулів та підмодулів, і складається з наступних функцій:
		- `setup_packeges` — функції установки та завантаження необхідних для коректного функціонування програмного модуля **"narrativeExtractor"** бібліотек та пакетів
	- `defaultLoader.py` — підмодуль, що призначений для завантаження мовних моделей, які визначені у списку мов за замовуванням, і містить наступні функції:
		- `load_default_languages` — функцію завантаження списку мов, визначених за замовчуванням, із файла `defaultLangs.csv` (у разі відсутності файлу список за замовчуваннм буде визначений як `'uk', 'ru', 'en', 'he', 'zh', 'de'`)
		- `load_default_models` — функцію завантаження мовних моделей бібліотеки `Stanza` для списку мов, що визначені за замовчуванням
		- `download_model` — функцію завантаження нових мовних моделей
		- `load_default_stop_words` — функцію завантаження стоп-слів для списку мов, визначених за замовчуванням
		- `load_stop_words` — функцію завантаження стоп-слів для нової мови
		- `append_lang` — функцію додавання нової мови у список мов за замовчуванням
	- `textProcessor.py` — підмодуль, що відповідає за комп'ютеризовану обробку вхідного природомовного тексту, і містить наступні функції:
		- `lang_detect` — функцію визначення мови вхідного тексту
		- `nl_processing` — функцію комп'ютеризованої обробки вхідного тексту відповідною мовною моделлю з використанням [Pipeline](https://stanfordnlp.github.io/stanza/pipeline.html) конвеєра бібліотеки `Stanza` та більш широкої обробки природної мови, що базується на розбитті на частини мови – [Part-of-speech tagging](https://stanfordnlp.github.io/stanza/pos.html), для побудови слів, біграм та триграм
		- `built_words` — функцію виокремлення ключових слів
		- `built_bigrams` — функцію побудови та виокремлення біграм за визначеними шаблонами
		- `built_threegrams` — функцію побудови та виокремлення триграм за визначеними шаблонами
	- `termsRanker.py` — підмодуль, що здійснює статистичне зважування термінів (слів, біграм і триграм) за частотою їх появи у тексті, і містить наступні функції:
		- `most_freq_key_terms` — функцію визначення найбільш частотних слів, біграм і триграм та виокремлення `top`-списку цих термінів (за замовчуванням `top = 12` — топ 12 слів, топ 12 біграм та топ 12 триграм)
		- `built_words` — функцію визначення найбільш частотних термінів та формування повного списку цих термінів

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

Програмний модуль **"narrativeExtractor"** зчитує вхідний потік текстових даних за допомогою функції `Pipeline` бібліотеки `Stanza` та здійснює послідовну обробку отриманого на вхід природомовного тексту, виокремлює ключові слова, біграми та триграми, здійснює їх статистичне зважування за частотою появи у тексті, й наприкінці здійснює вивід найбільш частотних термінів у вигляді списку слів, біграм та триграм.


a name="hardware"></a>
<h2>Використовувані технічні засоби</h2>

Програмний модуль експлуатується на сервері (або у хмарі серверів) під управлінням операційної системи типу `Linux` (64-х разрядна). В основі управління всіх сервісів є система оркестрації `Kubernetes`, де всі контейнери працюють з використанням `Docker`.


<a name="run"></a>
<h2>Виклик та завантаження</h2>

Для серверів, які працюють під керівництвом операційних систем сімейства `Windows OS`, виклик програмної системи **"narrativeExtractor"** здійснюється шляхом запуску скрипта `ім'я скрипта.py` з використанням команди `python`. Потрібно відкрити командний рядок – термінал `cmd` та написати `python ім'я скрипта.py`. Важливо, щоб скрипт знаходився або в директорії, з якої запущено командний рядок, або в каталозі, прописаному у змінній середовища `PATH`. 
Тож завантаження програмної системи забезпечується введенням в командному рядку повного імені завантажувальної програми без додаткових параметрів:
```cmd
python main.py
```

Для серверів, які працюють під керівництвом `Unix`-подібних операційних систем (наприклад, `Linux`) також можна скористатися цим способом, але на початку скрипта `Python` у першому рядку має бути вказаний повний шлях до інтерпретатора:
``` cmd
#!/usr/bin/python3
```
або
``` cmd
#!/usr/bin/env python3
```
Після цього необхідно дозволити запуск файлу (зробити його виконуваним).
``` cmd
chmod u+x main.py
```
Тепер просто запустити скрипт, ввівши в термінал його ім'я, перед яким додати «./»:
``` cmd
./main.py
```

В результаті запуску скрипта `main.py` здійснюється зчитування вхідного потоку текстових даних за допомогою функції `Pipeline` бібліотеки `Stanza` та послідовна обробка отриманого на вхід природомовного тексту, виокремлення ключових слів, біграм та триграм, здійснюється їх статистичне зважування за частотою появи у тексті, й наприкінці здійснюється вивід у консоль найбільш частотних термінів у вигляді списку слів, біграм та триграм. 

За замовчуванням, дані, отримані в результаті застосування програмної системи, виводяться в консолі `cmd`. Також вивід може перенаправлятися із консолі у файл, який зберігаюється у дирикторії `results` у вигляді `.txt` файла. Для цього використовується оператор `>`.
Повна команда виглядає так:
```cmd
python main.py > output.txt
```
Тут `output.txt` – це текстовий файл, у який записується результат виконання скрипта.

Операція може використовуватися як в операційній системі `Windows OS`, так і в `Unix`-подібних системах.
Якщо файла, в який повинен вивестися результат, не існує – система створить його автоматично.
При використанні оператора `>` вміст файлу, в який відображаються дані, повністю перезаписується. Якщо наявні дані потрібно зберегти, а нові дописати до існуючих, то використовується оператор `>>`:
```cmd
python main.py >> output.txt
``` 

© 2022 [Oleh Dmytrenko](https://github.com/OlehDmytrenko)


