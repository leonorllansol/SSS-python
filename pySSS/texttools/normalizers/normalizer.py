class Normalizer:
    def applyNormalizations(self, text, normalizers):
        normalized = text
        for normalizer in normalizers:
            normalized = normalizer.normalize(normalized)
        return normalized


'''class EnglishLemmatizer(Normalizer):
    def __init__(self):
        self.textAnalyzer = TextAnalyzer()'''
