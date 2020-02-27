# LearnSubtitles
Learn subtitles is a tool that allows you to prepare yourself
before watching your favorite Movie/Series in its original language.
## How does it work?
__LearnSubtitles__ parses and lemmatizes the .str subtitle file
(with [srt](https://github.com/cdown/srt "str GitHub Page")
and [spaCy](https://github.com/explosion/spaCy "spacy GitHub page")),
then look at each  word frequency using
[wordfreq](https://github.com/LuminosoInsight/wordfreq "wordfreq GitHub page").
__LearnSubtitles__ will divide these words in three categories: easy, intermediate
 and advanced.

## How to use it

Right now __LearnSubtitles__ is only available for subtitles in German, English and Portuguese. However, feel free to **implement** your own language. 

First make sure that you have installed all [Dependencies](#dependencies), then you can look up for the words in your film base on their difficulty. You can also check how difficult is the film with the metric film_level (the higher, the easier).

```python
import LearnSubtitles as ls

language = "de" # "pt" and "en" also available
my_sub = ls.LearnSubtitles("your/srt/file.srt", language)
print(my_sub.subtitle_path, my_sub.film_level)
print(*my_sub.easy_words, sep=", ")
print(*my_sub.intermediate_words, sep=", ")
print(*my_sub.advanced_words, sep=", ")
```

### Results:
#### Results for a German Short Film
[![German Short Film](http://img.youtube.com/vi/WBC2MukULcE/0.jpg)](http://www.youtube.com/watch?v=WBC2MukULcE "German Short Film")


**Easy words:**
lassen, paar, Woche, Junge, laufen, versuchen, Problem, schreiben, stehen, einfach, gehen, weiß, genau

**Intermediate words:**
Aufstehen, Frühstück, Außenseiter, Alternativ, Ruhe, Lehrer, Kapitel, geschehen, Handy, reparieren, Plan, Backup, beheben, Software, Tür, Aufschrift, Betreten, verbieten, beginnen, Nachricht, langweilig, übertreiben, Klick, Beziehung, zerstören, wusste, öfter, Albtraum, jederzeit

**Advanced words:**
Ungewöhnliches, einspielen, unbeobachtete, Spalt, mitzulesen, Frendschaften, bescheißen, Selbstdiagnose

#### Results for a German Short Film (but in English)
[![English Short Film](http://img.youtube.com/vi/IiavLUfbmgM/0.jpg)](http://www.youtube.com/watch?v=IiavLUfbmgM "English Short Film")

**Easy words:**
self, computer, people, leave, week, ago, happen, boy, give, phone, go, plan, try, problem, write, like, door, say, open, start, read, message, get, able, relationship, feel, know, far, exactly, want, time

**Intermediate words:**
breakfast, diagnosis, outsider, alternatively, nerd, prefer, teacher, chapter, unusual, cell, fix, accord, import, backup, software, entry, crack, boring, click, destroy, friendship, nightmare

**Advanced words:**
unobserved, overdo, crappy


#### Results for Clip in Brazilian Portuguese
[![Brazilian Portuguese Clip](http://img.youtube.com/vi/TQ5DUv_ZwRg/0.jpg)](http://www.youtube.com/watch?v=TQ5DUv_ZwRg "Brazilian Portuguese Clip")

**Easy words:**
mão, pensar, esperar, deixar, dia, encontrar, voltar, mostrar, saber, vir, perder, pra, aprender, entender, amor, olhar, levar, código, som, pedir, mundo, gente, paz, viver, seguir, falar, mim, ir, ficar, manhã, nenhum, difícil, comigo, passar, viagem, longo, fazer, claro, tentar, Seja, sentir

**Intermediate words:**
Menina, agir, mentir, confusão, direção, beber, catar, lata, olho, Desculpe, sincero, lógico, letra, rap, sólido, brigar, virar, der, meter, ensinar, curto, chorar, despedir, café, acordar, errar, ódio, rancor, precisar, independente, amar, negar, positivo, existir, cair, tratar, arrepender, envolver, querer, Noites, doer, justificar, sumir

**Advanced words:**
champanhe, vidar, sórdido, Psicografado, súbito, bobeira, pirar, bandeiro, certar, horar, abalar, papar, inventariar, clichê


## Dependencies

__LearnSubtitles__ used ``spaCy``, ``srt`` and ``wordfreq``, so you need to install them. You can install it easily:
```
pip install -r requirements.txt
```
spaCy Models will be automatically downloaded if needed
## TODO and Improvements
### TODO
- [x] Make other languages available
- [ ] Download subtitles automatically
- [ ] Swipe GUI (like tinder), so the user can easily filter the words he doesn't know

### Improvements
- [ ] Execution time (spaCy model taking long time)
- [ ] Filter language (Words from other languages may also pop up)
- [ ] Improve NLP model for subtitles
