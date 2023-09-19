"""
.. include:: ../../README.md
"""
import nltk

from .nrclex import NRCLex

for library in ['tokenizers/punkt', 'corpora/wordnet.zip']:
    try:
        nltk.data.find(library)
    except LookupError:
        print(f'Could not find {library}, downloading')
        print('---')
        nltk.download(library.split('/')[-1].replace('.zip', ''))

__version__ = '5.0'
__license__ = 'MIT'
__author__ = 'metalcorebear'

__all__ = [
    "NRCLex"
]
