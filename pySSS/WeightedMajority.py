from AgentManager import AgentManager
import configParser
from WM_BestCandidate import WM_BestCandidate
from WM_BestScoring import WM_BestScoring
import math
from texttools.normalizers import normalizerFactory
from texttools.normalizers.normalizer import Normalizer
from texttools.ReferenceCorpusParser import ReferenceCorpusParser
import operator

class WeightedMajority:

    def __init__(self):
        self.references = self.parseReferenceCorpus()
        self.agentManager = AgentManager()
        self.agents = self.agentManager.externalAgents
        self.strategy = self.pickStrategy()
        self.normalizers = normalizerFactory.createNormalizers(configParser.getNormalizers())


    def learnWeights(self):

        weights = {}
        rewards = {}

        for agent in self.agents:
            weights[agent.agentName] = 1/len(self.agents)
            rewards[agent.agentName] = 0

        t = 1

        for ref in self.references:

            print("------------ ITERATION " + str(t) + " ------------")
            print("Reference Trigger: " + ref.trigger)
            print("Reference Answer: " + ref.answer)


            
            nquery = Normalizer().applyNormalizations(ref.trigger, self.normalizers)
            
            candidates = self.agentManager.generateLuceneCandidates(nquery,"")
            
            if(len(candidates) == 0):
                continue

            answers = self.agentManager.generateAgentsAnswersFixedCandidates(nquery, candidates)

            votedAnswer = self.mostVotedSelection(weights, answers)
            print(votedAnswer)

            totalWeight = 0

            for agent in self.agents:
                rewards[agent.agentName] += self.strategy.computeReward(candidates, ref.answer, agent.agentName)
                weights[agent.agentName] += self.strategy.updateWeight(rewards[agent.agentName])
                totalWeight += weights[agent.agentName]
            
            #distinct for loops because totalWeight is still being updated in the first loop
            for agent in self.agents:
                weights[agent.agentName] = (weights[agent.agentName] * 100) / totalWeight
            
            finalWeights = weights

            print(finalWeights)
            
            t += 1
   


    
    def mostVotedSelection(self, weights, answers):
        
        mostVoted = {}

        #we're assuming that all answers are represented by SimpleQA objects
        for agent in weights.keys():

            #must deal with the case that the agent doesn't have a set weight attribute, aka the default case: external structure being stored and passed?
            weightedVote = weights[agent]

            #assuming that the agentName attribute always exists for any agent

            bestCandidate = answers[agent]
            if(type(bestCandidate) is list):
                bestCandidate = bestCandidate[0]
            bestAnswer = bestCandidate.getAnswer()
            bestScore = bestCandidate.getScoreByEvaluator(agent)
            if(bestAnswer in mostVoted.keys()):
                weightedVote += mostVoted[bestAnswer]
            
            mostVoted[bestAnswer] = weightedVote
        
        return max(mostVoted.items(), key=operator.itemgetter(1))[0]


    def pickStrategy(self):

        zeta = math.sqrt((configParser.getEtaFactor() * math.log(len(self.agents))) / configParser.getInputSize())
        decimalPlaces = configParser.getDecimalPlaces()

        if(configParser.getLearningStrategy() == "BestCandidate"):
            return WM_BestCandidate(decimalPlaces, zeta)

        elif(configParser.getLearningStrategy() == "BestCandidate"):
            return WM_BestScoring(decimalPlaces, zeta)


    def parseReferenceCorpus(self):
        interactionsPath = configParser.getInteractionsPath()
        linesPath = configParser.getLinesPath()
        inputSize = configParser.getInputSize()

        rcp = ReferenceCorpusParser(interactionsPath,linesPath,inputSize)

        return rcp.parse()