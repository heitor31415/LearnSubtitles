#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import srt
import spacy
import wordfreq as wf

nlp = spacy.load('de_core_news_md', disable=["ner"])  # md or sm


def remove_duplicated_and_uppercase_words(word_list):
    """Removes duplicated and uppercase words from a list """
    if word_list:
        my_list_temp = []
        for word in word_list:
            if word.isupper():
                word = word.lower()
            if word.lower() not in my_list_temp:
                if word not in my_list_temp:
                    my_list_temp.append(word)
        return my_list_temp
    else:
        return []


def clean_line(raw_line):
    """Removes tags, eventual line breaks and special characters """

    allowed_characters = " .,?!0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZöäüÖÄÜß"

    p1 = re.compile(r'<.*?>')  # removes tags
    new_line = p1.sub('', raw_line)
    new_line = re.sub('\n', ' ', new_line)  # removes \n
    new_line = ''.join(c for c in new_line if c in allowed_characters)
    re.sub("\s\s+", " ", new_line)  # removes multiple spaces
    return new_line


def clean_text(raw_text):
    """Removes multiple spaces from text """
    re.sub("\s\s+", " ", raw_text)


class LearnSubtitles:
    def __init__(self, subtitle_path: str, language='de'):
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
        self.text = ''
        self.tokens = ''
        self.important_words = ''
        self.study_dict = {}

        # Open subtitle file and pre-process it
        try:
            with open(subtitle_path) as raw_subtitle:
                subs = list(srt.parse(raw_subtitle))  # extract texts with srt
                for i in range(len(subs)):
                    self.text += clean_line(subs[i].content) + ' '
                clean_text(self.text)

        except FileNotFoundError:
            print(f'File not found at {subtitle_path}')
        except srt.SRTParseError:
            print('The srt file has parsing problems. Trying to fix the File.')
            with open(subtitle_path, "r") as f:
                lines = f.readlines()
                maintain = False
                with open("reworked_subtitle.srt", "w") as new_f:
                    for line in lines:
                        if re.match("^.?1(\n)?$", line) != None or maintain:
                            if not maintain:
                                new_f.write('1\n')
                            else:
                                new_f.write(line)
                            maintain = True
            try:
                with open("reworked_subtitle.srt") as raw_subtitle:
                    subs = list(
                        srt.parse(raw_subtitle))  # extract texts with srt
                    for i in range(len(subs)):
                        self.text = self.text + clean_line(
                            subs[i].content) + ' '
                    clean_text(self.text)
            except FileNotFoundError:
                print(f'File not found at {subtitle_path}')
            except srt.SRTParseError:
                print(
                    'The srt file still has parsing problems. Try to fix it manually.')

        self.__tokenize_and_process()
        self.__create_study_dicts()

    def __repr__(self):
        print(self.text)

    def __tokenize_and_process(self):
        """Tokenize text and extract most important words"""
        self.tokens = nlp(self.text)
        # separate words that may be useful
        important_words_raw = [token.lemma_ for token in self.tokens if
                               not token.is_oov
                               and not token.is_stop
                               and not token.is_punct
                               and not token.like_num
                               and token.tag != 'NE'  # optional
                               and token.pos_ != 'PROPN']

        self.important_words = remove_duplicated_and_uppercase_words(
            important_words_raw)

    def __create_study_dicts(self):
        for word in self.important_words:
            word_freq = wf.zipf_frequency(word, self.language)
            if word_freq >= 5:
                self.study_dict[word] = 'easy'
            elif word_freq >= 3.5:
                self.study_dict[word] = 'intermediate'
            else:
                self.study_dict[word] = 'advanced'

    def print_dict(self, level='easy'):  # level = easy/intermediate/advanced
        return (
        [word for word in self.study_dict if self.study_dict[word] == level])


def main():
    sub_dir = "/home/heitor/p/LearnSubtitles/testfiles/"
    filename: str = 'Dark.S01E01.WEBRip.x264-STRiFE.German.srt'
    # filename: str = 'Im.Juli.srt'
    subtitle_path = sub_dir + filename
    dark = LearnSubtitles(subtitle_path)

    print(dark.print_dict(level='easy'))
    print('\n\n######INTERMEDIATE WORDS#######')
    print(dark.print_dict(level='intermediate'))
    print('\n\n######ADVANCED WORDS#######')
    print(dark.print_dict(level='advanced'))


if __name__ == '__main__':
    main()
