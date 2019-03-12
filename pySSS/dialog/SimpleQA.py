import subprocess
import configParser

class SimpleQA:
    def __init__(self, previousQA, question, normalizedQuestion, answer, normalizedAnswer, diff):
        self.previousQA = previousQA    #is a number
        self.question = question
        self.answer = answer
        self.normalizedAnswer = normalizedAnswer
        self.normalizedQuestion = normalizedQuestion
        self.diff = diff
        self.scores = {}

    def getDiff(self):
        return self.diff

    def getPreviousQA(self):
        if int(self.previousQA) != -1:
            #getSimpleQA from LuceneWrapper
            list_args = ["java", "LuceneWrapper", self.previousQA, configParser.getCorpusPath(), "", configParser.getLanguage(), configParser.getIndexPath(), configParser.getHitsPerQuery(), configParser.getDbPath()]
            sp1 = subprocess.Popen(list_args,shell=False)
            exitCode = sp1.wait()

            newSimpleQa = open('simpleQa.txt', 'r')

            lines = newSimpleQa.readlines()
            strippedLines = []
            for line in lines:
                strippedLines.append(line.strip('\n'))

            newQa = SimpleQA(strippedLines[0], strippedLines[1], strippedLines[2], strippedLines[3], strippedLines[4], strippedLines[5])
            return newQa
        else:
            return -1 #no previousQA

    def getQuestion(self):
        return self.question

    def getAnswer(self):
        return self.answer

    def getNormalizedQuestion(self):
        return self.normalizedQuestion

    def getNormalizedAnswer(self):
        return self.normalizedAnswer

    def addScore(self, evaluator, score):
        self.scores[evaluator] = score

    def getScores(self):
        return self.scores

    def getScoreByEvaluator(self, evaluator):
        return self.scores[evaluator]

    def textual(self):
        return "previousQA: " + str(self.previousQA) + "; question: " + self.question +\
                "; answer: " + self.answer + "; normalizedAnswer: " + self.normalizedAnswer +\
                "; normalizedQuestion: " + self.normalizedQuestion + "; diff: " + str(self.diff)
