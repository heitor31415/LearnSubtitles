import os

import pytest
from typing import Any, Callable, Dict, List

import LearnSubtitles as ls


def prepare(language: str) -> List:
    """ Create LearnSubtitles objects for every subtitle in folder 'language' """
    test_dir = "testfiles/" + language
    subs = [
        ls.LearnSubtitles(os.path.abspath(os.path.join(test_dir, x)), language)
        for x in os.listdir(test_dir)
    ]

    return subs


languages = ["de", "en", "pt"]  # supported languages


def test_LearnSubtitles_parsing():
    for language in languages:
        subs = prepare(language)
        for sub in subs:
            assert len(sub.text) != 0


def test_LearnSubtitles_bad_file():
    with pytest.raises(FileNotFoundError):
        ls.LearnSubtitles(os.path.abspath("testfiles/fail/fail.srt"), "en")
    with pytest.raises(ls.LearnSubtitlesError):
        ls.LearnSubtitles(os.path.abspath("testfiles/fail/bad_file.srt"), "en")


def test_LearnSubtitles_level():
    levels = ["A1", "A2", "B1"]
    subs = [
        ls.LearnSubtitles(
            "testfiles/de/Nicos Weg – " + level + " – Ganzer Film - German.srt", "de"
        )
        for level in levels
    ]
    assert subs[0].film_level > subs[1].film_level
    assert subs[1].film_level > subs[2].film_level
