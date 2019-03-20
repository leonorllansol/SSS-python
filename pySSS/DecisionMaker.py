import operator
import configParser

class DecisionMaker:
    def __init__(self,decisionMethod):
        self.decisionMethod = decisionMethod

    
    def decideBestAnswer(self,defaultAgentsAnswers,externalAgentsAnswers):
        
        if(self.decisionMethod == "SimpleMajority"):

            answerFrequency = {}

            mergedAgentAnswers = {**defaultAgentsAnswers, **externalAgentsAnswers}

            try:
                for agent in mergedAgentAnswers.keys():
                    answer = mergedAgentAnswers[agent]
                    answerFrequency[answer] = answerFrequency.get(answer,0) + 1
                    print('Answer from agent ' + agent + ': \n' + mergedAgentAnswers[agent] + '\n')            


                finalAnswer = max(answerFrequency.items(),key=operator.itemgetter(1))[0]

                return finalAnswer
            
            except ValueError:
                return configParser.getNoAnswerMessage()