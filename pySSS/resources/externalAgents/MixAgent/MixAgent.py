

class MixAgent:
    def __init__(self,configs,indexval=''):
        self.useLucene = configs['receiveLuceneCandidates']          #string 'true' ou 'false'; n é convertido para bool
        self.agentName = self.__class__.__name__
        self.questionSimValue = float(configs['questionSimValue'])
        self.answerSimValue = float(configs['answerSimValue'])



    def getBestCandidate(self,userInput,candidates):
        userInputWords = self.getWordSet(userInput)
        bestPair = candidates[0]

        for c in candidates:
            questionWords = self.getWordSet(c.getNormalizedQuestion())
            answerWords = self.getWordSet(c.getNormalizedAnswer())

            questionScore = len(userInputWords.intersection(questionWords)) / len(userInputWords.union(questionWords))
            answerScore = len(userInputWords.intersection(answerWords)) / len(userInputWords.union(answerWords))

            finalScore = self.getFinalScore(questionScore,answerScore)
            c.addScore(self.agentName,finalScore)

            if(c.getScoreByEvaluator(self.agentName) > bestPair.getScoreByEvaluator(self.agentName)):
                bestPair = c
        
        return bestPair.getAnswer()



    def getWordSet(self,input):
        #tokenizedInput = re.sub(r'\W+',' ',input).lower()
        #wordSet = set(tokenizedInput.split())
        wordSet = set(input.split())
        return wordSet

    def getFinalScore(self,questionScore,answerScore):
        return questionScore * self.questionSimValue + answerScore * self.answerSimValue
