from .normalizer import Normalizer
from ptstemmer import Stemmer
from ptstemmer.support import PTStemmerUtilities
from ptstemmer.implementations.OrengoStemmer import OrengoStemmer


class PortugueseStemmer(Normalizer):
    def __init__(self):
        stemmer = OrengoStemmer()
        stemmer.enableCaching(1000)
        #Optional
        stemmer.ignore(PTStemmerUtilities.fileToSet("./resources/namedEntities/namedEntities.txt"))

    def normalize(self, text):
        separator = " "
        return separator.join(stemmer.getPhraseStems(text))
