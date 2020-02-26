import os
import re
from typing import Any, Callable, Dict, List, Tuple, TypeVar, Iterable, Iterator, Union

import srt
import wordfreq as wf
import spacy
from spacy.cli.download import download as spacy_download
from spacy.language import Language as SpacyModelType


def remove_duplicated_and_uppercase_words(word_list):
    """Removes duplicated and uppercase words from a list """
    my_list_temp = []
    for word in word_list:
        if word.isupper():
            word = word.lower()
        if (word.lower() not in my_list_temp) or (word not in my_list_temp):
            my_list_temp.append(word)
    return my_list_temp


def clean_line(raw_line):
    """Removes tags, eventual line breaks and special characters """

    p1 = re.compile(r"<.*?>")  # removes tags
    new_line = p1.sub("", raw_line)
    new_line = re.sub("\n", " ", new_line)  # removes \n
    new_line = re.sub(r"[^\wäöüßÄÖÜ ?!.,]", " ", new_line)  # removes special characters
    new_line = re.sub(r"\s{2,}", " ", new_line)  # removes multiple spaces
    return new_line


def clean_text(raw_text):
    """Removes multiple spaces from text """
    return re.sub(r"\s{2,}", " ", raw_text)


class LearnSubtitles:
    def __init__(self, subtitle_path: str, language: str, nlp: SpacyModelType) -> None:
        """
        Base class for LearnSubtitles.
        :type subtitle_path: str : path for the srt file
        :param language: language of the subtitle.
        :param text: Subtitle text (not tokenized).
        :important_words: tokenized text, without stopwords
        :param study

        """
        self.subtitle_path = subtitle_path
        self.language = language
        self.nlp = nlp
        self.text = ""
        self.tokens = ""
        self.important_words = ""
        self.study_dict = {}
        self.film_level = 0

        # Open subtitle file and pre-process it
        try:
            with open(subtitle_path) as raw_subtitle:
                subs = list(srt.parse(raw_subtitle))  # extract texts with srt
                for i in range(len(subs)):
                    self.text += clean_line(subs[i].content) + " "
                self.text = clean_text(self.text)

        except FileNotFoundError:
            print(f"File not found at {subtitle_path}")
        except srt.SRTParseError:
            print("The srt file has parsing problems. Trying to fix the File.")
            with open(subtitle_path, "r") as f:
                lines = f.readlines()
                maintain = False
                with open("reworked_subtitle.srt", "w") as new_f:
                    for line in lines:
                        if re.match("^.?1(\n)?$", line) != None or maintain:
                            if not maintain:
                                new_f.write("1\n")
                            else:
                                new_f.write(line)
                            maintain = True
            try:
                with open("reworked_subtitle.srt") as raw_subtitle:
                    subs = list(srt.parse(raw_subtitle))  # extract texts with srt
                    for i in range(len(subs)):
                        self.text = self.text + clean_line(subs[i].content) + " "
                    self.text = clean_text(self.text)
            except FileNotFoundError:
                print(f"File not found at {subtitle_path}")
            except srt.SRTParseError:
                print("The srt file has parsing problems.")

        self.__tokenize_and_process()
        self.__create_study_dicts()

    def __repr__(self):
        print(self.text)

    def __tokenize_and_process(self):
        """Tokenize text and extract most important words"""
        self.tokens = self.nlp(self.text)
        # separate words that may be useful
        important_words_raw = [
            token.lemma_
            for token in self.tokens
            if not token.is_stop
            and len(token) > 2
            and not token.is_punct
            and not token.like_num
            and token.pos_ != "PROPN"
        ]

        self.important_words = remove_duplicated_and_uppercase_words(
            important_words_raw
        )

    def __create_study_dicts(self):
        for word in self.important_words:
            word_freq = wf.zipf_frequency(word, self.language)
            self.film_level += word_freq

            if word_freq >= 5:
                self.study_dict[word] = 1
            elif word_freq >= 3.5:
                self.study_dict[word] = 2
            else:
                self.study_dict[word] = 3
        self.film_level /= len(self.study_dict)

    @property
    def easy_words(self, level=1):  # level = 1 easy/ 2 intermediate/3 advanced
        return [word for word in self.study_dict if self.study_dict[word] == level]

    @property
    def intermediate_words(self, level=2):
        return [word for word in self.study_dict if self.study_dict[word] == level]

    @property
    def advanced_words(self, level=3):
        return [word for word in self.study_dict if self.study_dict[word] == level]


def main():

    language = "en"

    spacy_default_models = {
        "en": "en_core_web_md",
        "de": "de_core_news_md",
        "pt": "pt_core_news_sm",
    }
    spacy_model_name = spacy_default_models[language]

    try:
        spacy_model = spacy.load(spacy_model_name, disable=["ner"])
    except OSError:
        print(
            f"Spacy models '{spacy_model_name}' not found.  Downloading and installing."
        )
        spacy_download(spacy_model_name)
        spacy_model = spacy.load(spacy_model_name, disable=["ner"])

    test_dir = "testfiles/" + language
    subs = [
        LearnSubtitles(
            os.path.abspath(os.path.join(test_dir, x)), language, spacy_model
        )
        for x in os.listdir(test_dir)
    ]

    for sub in subs:
        print(sub.subtitle_path, sub.film_level)
        print(sub.easy_words)
        print(sub.intermediate_words)
        print(sub.advanced_words)
        print(sub.text)


if __name__ == "__main__":
    main()
