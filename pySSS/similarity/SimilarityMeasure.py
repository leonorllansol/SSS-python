import nltk

class SimilarityMeasure:
    def __init__(self, weight):
        self.weight = weight

    def getWeight(self):
        return self.weight

class Jaccard(SimilarityMeasure):
    def distance(self, str1, str2):
        return nltk.jaccard_distance(set(str1), set(str2))

    def finalScore(self, dic):
        c = min(dic, key=dic.get)
        return c.getAnswer(), dic[c]

class Dice(SimilarityMeasure):
    def distance(self, str1, str2):
        set_1 = set(str1)
        set_2 = set(str2)
        overlap = len(set_1 & set_2)
        return 2 * overlap / (len(set_1) + len(set_2))

    def finalScore(self, dic):
        c = max(dic, key=dic.get)
        return c.getAnswer(), dic[c]

class EditDistance(SimilarityMeasure):
    def distance(self, str1, str2):
        return nltk.edit_distance(str1, str2)

    def finalScore(self, dic):
        c = min(dic, key=dic.get)
        return c.getAnswer(), dic[c]
