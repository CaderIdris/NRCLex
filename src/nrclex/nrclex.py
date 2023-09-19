#!/usr/bin/env python
""" Measures emotional affect of a body of text.

Based on the National Research Council Canada (NRC) affect lexicon [^nrc] and
built on top of TextBlob [^blob].

As per the terms of use of the NRC Emotion Lexicon, if you use the lexicon or
any derivative from it, cite this paper:

Crowdsourcing a Word-Emotion Association Lexicon,
Saif Mohammad and Peter Turney,
Computational Intelligence,
29 (3), 436-465, 2013.

[^nrc]: http://saifmohammad.com/WebPages/NRC-Emotion-Lexicon.html
[^blob]: https://textblob.readthedocs.io/en/dev/
"""
from collections import Counter
from importlib.resources import as_file, files
from importlib.resources.abc import Traversable
import json
from pathlib import Path
from typing import get_args, Literal, Optional, TypeAlias, Union

from textblob import TextBlob





PreInstalledLexicons: TypeAlias = Literal[
    "NRCLex"
]

class NRCLex:
    """
    Compares provided text against an emotional affect lexicon

    Emotional affect lexicons must be saves as a json file and
    have the following format:

    ```json
        "word": [
            # List of associated emotions as strings
        ]
    ```

    Examples
    --------
    #### Pre-tokenized text
    >>> nrc_object = NRCLex(lexicon_file=...)
    >>> nrc_object.load_token_list(tokens)
    
    TODO: Finish examples
    """

    def __init__(
            self,
        lexicon_file: Union[PreInstalledLexicons, Path] = "NRCLex"
        ):
        """
        Parameters
        ----------
        lexicon_file : Path or {'NRCLex'}, default='NRCLex'
            Path to custom lexicon file or name of preinstalled lexicon

        Raises
        ------
        TypeError
            Raised if `lexicon_file` is not Path or name of preinstalled
            lexicon
        """
        preinstalled_files: dict[
            PreInstalledLexicons,
            Traversable
        ] = {
            "NRCLex": files('nrclex.data').joinpath('nrc_en.json')
        }
        self.lexicon: dict[str, list[str]] = dict()
        """
        Emotional lexicon to analyse text with
        """
        if isinstance(lexicon_file, Path):
            self.load_lexicon(lexicon_file)
        elif lexicon_file in get_args(PreInstalledLexicons):
            with as_file(preinstalled_files[lexicon_file]) as lexicon_file:
                self.load_lexicon(lexicon_file)
        else:
            raise TypeError('Expected path or preinstalled lexicon')
        self.words: list[str] = list()
        """
        Words to analyse with emotional `lexicon`
        """
        self.affect_list: list[str] = list()
        """
        Words in `words` with corresponding emotions in `lexicon`
        """
        self.affect_dict: dict[str, list[str]] = dict()
        """
        `lexicon` filtered to words in text
        """
        self.raw_emotion_scores: dict[str, int] = dict()
        """
        Counts of words in `text` that are in `lexicon`
        """
        self.affect_frequencies: dict[str, float] = dict()
        """
        Proportion words appear relative to other emotional words
        """

    def load_lexicon(self, path: Path):
        """
        Loads a json file representing emotional lexicon
        
        Parameters
        ----------
        path : Path
            Path to the json file representing emotional lexicon
        """
        with open(path, 'r') as json_file:
            self.lexicon = json.load(json_file)

    def build_word_affect(self):
        """
        """
        affect_list = list()
        affect_dict = dict()
        affect_frequencies = Counter()
        affect_percent = dict()

        lexicon_keys = self.lexicon.keys()
        for word in self.words:
            if word in lexicon_keys:
                affect_list.extend(self.lexicon[word])
                affect_dict.update({word: self.lexicon[word]})

        for word in affect_list:
            affect_frequencies[word] += 1

        sum_values = sum(affect_frequencies.values())
        affect_percent = {
            key: float(affect_frequencies[key]) / float(sum_values)
            for key in affect_frequencies.keys()
        }
        self.affect_list = affect_list
        self.affect_dict = affect_dict
        self.raw_emotion_scores = dict(affect_frequencies)
        self.affect_frequencies = affect_percent

    @property
    def top_emotions(self) -> list[tuple[str, float]]:
        """
        List of most common emotions
        """
        max_value = max(self.affect_frequencies.values())
        top_emotions: list[tuple[str, float]] = []
        for key in self.affect_frequencies.keys():
            if self.affect_frequencies[key] == max_value:
                top_emotions.append((key, max_value))
        return top_emotions

    def load_token_list(self, token_list: list[str]):
        '''
        Load pre-tokenized text.
        This is for when you want to use NRCLex with a text that you prefer
        to tokenize and/or lemmatize yourself.

        Parameters
        ----------
        token_list : list of str
            A list of pre-tokenized utf-8 strings.
        Returns
        -------
        None
        '''
        self.words = token_list
        self.build_word_affect()

    def load_raw_text(self, text):
        '''
        Load a string into the NRCLex object for
        tokenization and lemmatization with TextBlob.

        Parameters:
            text (str): a utf-8 string.
        Returns:
            No return
        '''
        blob: TextBlob = TextBlob(text)
        self.load_token_list(
            [w.lemma for w in blob.words]  # type: ignore
        )
        
