import conversation
import configParser
from dialog.SimpleQA import SimpleQA
from texttools.normalizers import normalizerFactory
from texttools.normalizers.normalizer import Normalizer
from resources.externalAgents import AgentFactory
from xml.dom import minidom
import subprocess
import operator



class AgentManager:
    def __init__(self):
        self.conversation = conversation.Conversation()
        self.externalAgentsPath = configParser.getExternalAgentsPath()
        self.externalAgents = self.initializeAgents()
        self.normalizers = normalizerFactory.createNormalizers(configParser.getNormalizers())



    def initializeAgents(self):
        return AgentFactory.createExternalAgents(self.externalAgentsPath)


    def generateAgentsAnswers(self,userInput):

        candidates = self.generateLuceneCandidates(userInput)
        agentAnswers = {}

        for agent in self.externalAgents:
            try:
                answer = agent.getBestCandidate(userInput,candidates)
                agentAnswers[agent.__class__.__name__] = answer
            except IndexError:
                agentAnswers[agent.__class__.__name__] = configParser.getNoAnswerMessage()
        return agentAnswers



    def generateLuceneCandidates(self,query):
        query_normalized = Normalizer().applyNormalizations(query, self.normalizers)
        list_args = ["java", "LuceneWrapper", "-2", configParser.getCorpusPath(), query_normalized, configParser.getLanguage(), configParser.getIndexPath(), configParser.getHitsPerQuery(), configParser.getDbPath()]
        sp1 = subprocess.Popen(list_args,shell=False)
        exitCode = sp1.wait()

        luceneResults = open('luceneresults.txt', 'r')

        lines = luceneResults.readlines()
        strippedLines = []
        for line in lines:
            strippedLines.append(line.strip('\n'))

        luceneResults.close()

        candidates = getCandidatesFromLuceneResults(query, strippedLines)
        return candidates



    def decideBestAnswer(self,userInput,defaultAgentsAnswers):


        candidates = self.generateLuceneCandidates(userInput)
        agentAnswers, answerFrequency = self.getAgentsAnswer(userInput,candidates)

        self.integrateDefaultAgentsAnswers(defaultAgentsAnswers,agentAnswers,answerFrequency)   #this call directly modifies the dictionaries

        finalAnswer = max(answerFrequency.items(),key=operator.itemgetter(1))[0]

        for agent in agentAnswers.keys():
            print('Answer from agent ' + agent + ': \n' + agentAnswers[agent] + '\n')

        return finalAnswer

    

    def integrateDefaultAgentsAnswers(self,defaultAgentsAnswers,agentAnswers,answerFrequency):
        for i in range(len(defaultAgentsAnswers)):
            
            answer = defaultAgentsAnswers[i][0]
            agentAnswers['Agent' + str(i)] = answer
            answerFrequency[answer] = answerFrequency.get(answer,0) + 1




def getCandidatesFromLuceneResults(query, lines):
    candidates = []
    for i in range(0, len(lines), 6):
        previousQA = lines[i]
        question = lines[i+1]
        answer = lines[i+2]
        normalizedQuestion = lines[i+3]
        normalizedAnswer = lines[i+4]
        diff = lines[i+5]
        qa = SimpleQA(previousQA, question, normalizedQuestion, answer, normalizedAnswer, diff)
        candidates.append(qa)
    return candidates
    




