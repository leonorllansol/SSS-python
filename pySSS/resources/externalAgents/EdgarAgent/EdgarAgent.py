import re


class EdgarAgent:
    def __init__(self,configs):
        self.agentName = self.__class__.__name__
        self.corpusPath = configs['corpusPath']
        self.dbPath = configs['dbPath']
        self.indexPath = configs['indexPath']
        self.threshold = float(configs['threshold'])


    def requestAnswer(self,userInput,candidates):
        
        userInputWords = self.getWordSet(userInput)
        bestPair = candidates[0]
        for c in candidates:
            questionWords = self.getWordSet(c.getNormalizedQuestion())
            score = len(userInputWords.intersection(questionWords)) / len(userInputWords.union(questionWords))
            c.addScore(self.agentName,score)

            if(c.getScoreByEvaluator(self.agentName) > bestPair.getScoreByEvaluator(self.agentName)):
                bestPair = c
        
        if(bestPair.getScoreByEvaluator(self.agentName) > self.threshold):
            return bestPair.getAnswer()
        else:
            return 'Não sei responder a isso'



    def getWordSet(self,input):
        #tokenizedInput = re.sub(r'\W+',' ',input).lower()
        #wordSet = set(tokenizedInput.split())
        wordSet = set(input.split())
        return wordSet


