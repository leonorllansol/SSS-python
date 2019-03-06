from .simpleNormalizer import SimpleNormalizer
from .portugueseStemmer import PortugueseStemmer

def createNormalizers(normalizersStrings):
    normalizers = []
    for norm in normalizersStrings:
        if norm == "RemoveDiacriticalMarks":
            normalizers.append(SimpleNormalizer())
        elif norm == "PortugueseStemmer":
            normalizers.append(PortugueseStemmer())
    return normalizers
