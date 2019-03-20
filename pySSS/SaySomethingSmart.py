from answers import HighestWeightedScoreSelection, MultipleAnswerSelection
import logging, sys
import configParser, subprocess
from DecisionMaker import DecisionMaker
from AgentManager import AgentManager

def dialogue(): #mode dialogue


    defaultAgentsMode = configParser.getDefaultAgentsMode()


    #--Lucene init--
    list_args = ["java", "LuceneWrapper", "0", configParser.getCorpusPath(), "", configParser.getLanguage(), configParser.getIndexPath(), configParser.getHitsPerQuery(), configParser.getDbPath()]
    sp1 = subprocess.Popen(list_args,shell=False)

    exitCode = sp1.wait()

    if(defaultAgentsMode == 'multi'):
        multiAgentAnswerMode()
    else:
        classicDialogueMode()
        


def classicDialogueMode():

    highestWeightedScoreSelection = HighestWeightedScoreSelection()

    while True:
        query = ""

        while (query == ""):
            query = input("Say something:\n")

        if query == "exit":
            break;

        logging.basicConfig(filename='log.txt', filemode='w', format='%(message)s', level=logging.INFO)
        logging.info("Query: " + query)


        answer = highestWeightedScoreSelection.provideAnswer(query)


        print("Question:", query)
        print("Answer:", answer)




def multiAgentAnswerMode():

    multipleAnswerSelection = MultipleAnswerSelection()
    agentManager = AgentManager()
    decisionMaker = DecisionMaker(configParser.getDecisionMethod())

    while True:
        query = ""

        while (query == ""):
            query = input("Say something:\n")

        if query == "exit":
            break;

        logging.basicConfig(filename='log.txt', filemode='w', format='%(message)s', level=logging.INFO)
        logging.info("Query: " + query)


        defaultAgentsAnswers = multipleAnswerSelection.provideAnswer(query)

        externalAgentsAnswers = agentManager.generateAgentsAnswers(query)
        
        #both defaultAgentsAnswers and externalAgentsAnswers are dictionaries in the format {'agent1': 'answer1', 'agent2': 'answer2'}

        answer = decisionMaker.decideBestAnswer(defaultAgentsAnswers,externalAgentsAnswers)


        print("Question:", query)
        print("Final Answer:", answer)







if __name__ == "__main__":
    dialogue()


#TODO mode evaluation
#TODO mode learning
