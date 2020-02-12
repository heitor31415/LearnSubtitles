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

Right now __LearnSubtitles__ is only available for subtitles in German
~~because I'm using it to watch dark without checking the dictionary~~

First make sure that you have installed all [Dependencies](#dependencies)

```python
import LearnSubtitles as ls

subtitle_path='/your/file/path/Dark.S01E01.German.srt'

Darks01e01= ls.LearnSubtitles(subtitle_path, 'de')
print(Darks01e01.print_dict(level='intermediate')) ## easy, advanced also available
```

#### Result
```
The srt file has parsing problems. Trying to fix the File.
['wissenschaftler', 'vertrauen', 'linear', 'verlaufen', 'ewig', 'Unterscheidung', 'Vergangenheit',  ...
'Erwacht', 'Augenblick', 'kehren', 'fangen', 'irgendwann', 'Irgendwo', 'warten']
[Finished in 33.4s]
```


## Dependencies

__LearnSubtitles__ used ``spaCy``, ``srt`` and ``wordfreq``, so you need to install them. You can install it easily:
```
pip install wordfreq
pip install -U srt

pip install -U spacy
python -m spacy download de_core_news_md
```
## TODO and Improvements
### TODO
* Make other languages available (en and pt will be available soon)
* Download subtitles automatically
* Swipe GUI (like tinder), so the user can easily filter the words he doesn't know

### Improvements
* Execution time (spaCy model taking long time)
* Filter language (Words from other languages may also pop up)
* Improve NLP model for subtitles
