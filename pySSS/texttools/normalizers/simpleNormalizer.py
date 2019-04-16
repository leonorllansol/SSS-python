from .normalizer import Normalizer
import configParser

class SimpleNormalizer(Normalizer):
    #remove puncts , upper case to lower case
    def normalize(self, text):
        normalized = text.lower()

        path = configParser.getNormalizersPath()
        f = open(path, 'r')
        puncts = f.readlines()
        puncts[-1] = puncts[-1].strip()
        puncts = puncts[0].split(" ")
        
        for sym in puncts:
            normalized = normalized.replace(sym, '')
        return normalized
