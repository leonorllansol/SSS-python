import re
from texttools import stopwords


class EdgarAgent:
    def __init__(self,configs):
        self.agentName = self.__class__.__name__
        self.corpusPath = configs['corpusPath']
        self.indexPath = configs['indexPath']
        self.threshold = float(configs['threshold'])
        self.stopwordsPath = configs['stopwords']


    def requestAnswer(self,userInput,candidates):
        
        userInputWords = self.getWordSet(userInput)
        userInputWords_WoStopwords = self.getStringListWithoutStopWords(userInputWords)
        
        if(len(candidates) > 0):
            bestPair = candidates[0]

            for c in candidates:
            
                questionWords = self.getWordSet(c.getNormalizedQuestion())

                questionWords_WoStopwords = self.getStringListWithoutStopWords(questionWords)

                #score = len(userInputWords.intersection(questionWords)) / len(userInputWords.union(questionWords))
                score = len(userInputWords_WoStopwords.intersection(questionWords_WoStopwords)) / len(userInputWords_WoStopwords.union(questionWords_WoStopwords))
                c.addScore(self.agentName,score)
                #print(questionWords_WoStopwords, score)

                if(c.getScoreByEvaluator(self.agentName) > bestPair.getScoreByEvaluator(self.agentName)):
                    bestPair = c
        else:
            return 'Não sei responder a isso'

        if(bestPair.getScoreByEvaluator(self.agentName) > self.threshold):
            return bestPair.getAnswer()
        else:
            return 'Não sei responder a isso'



    def getWordSet(self,input):
        tokenizedInput = re.sub(r'\W+',' ',input).lower()
        wordSet = set(tokenizedInput.split())
        #wordSet = set(input.split())
        return wordSet


    def getStringListWithoutStopWords(self,tokenizedQuestion):
        stopWords = self.getStopWords()
        stringList = []
        for word in tokenizedQuestion:
            if not word in stopWords:
                stringList.append(word)
        return set(stringList)

    def getStopWords(self):
        path = self.stopwordsPath
        f = open(path, 'r', encoding='latin-1')
        stopwords = []
        lines = f.readlines()[16:]
        for line in lines:
            stopwords.append(line.split()[0])
        return stopwords
