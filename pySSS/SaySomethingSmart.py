from DefaultAnswers import HighestWeightedScoreSelection, MultipleAnswerSelection
import logging, sys, time
import configParser, subprocess
from DecisionMaker import DecisionMaker
from AgentManager import AgentManager
from WeightedMajority import WeightedMajority

def dialogue():

    """
    Main startup function for the SaySomethingSmart framework.
    - Verifies the desired workmode by checking the defaultAgentsMode parameter in the config.xml
    - If the defaultAgentsMode is "multi", calls the multiagent SSS framework; else, calls the "legacy" version of SSS with only its origin agents
    - Calls the LuceneWrapper class in order to index the given corpus
    """

    defaultAgentsMode = configParser.getDefaultAgentsMode()

    if(not configParser.usePreviouslyCreatedIndex()):
        list_args = ["java", "LuceneWrapper", "0", configParser.getCorpusPath(), "", configParser.getLanguage(), configParser.getIndexPath(), configParser.getHitsPerQuery(), configParser.getDbPath()]
        sp1 = subprocess.Popen(list_args,shell=False)
    
        exitCode = sp1.wait()


    if(defaultAgentsMode == 'multi'):
        multiAgentAnswerMode()
    elif(defaultAgentsMode == 'sequential'):
        sequentialConversationMode()
    elif(defaultAgentsMode == 'learning'):
        learningMode()
    else:
        classicDialogueMode()
        


def classicDialogueMode():

    """
    Classic mode for SSS: only calls the Evaluators inside SSS's source, doesn't take external agents into account

    - Initializes an AnswerSelection object (in this case, HighestWeightedScoreSelection)
    - Performs the "legacy" SSS routine: upon receiving a user query, it sends that query to the AnswerSelection object
    - The AnswerSelection object then returns an answer String, which is subsequently printed to the user
    """

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




def sequentialConversationMode():

    multipleAnswerSelection = MultipleAnswerSelection()
    agentManager = AgentManager()
    decisionMaker = DecisionMaker(configParser.getDecisionMethod())
    
    questionsPath = configParser.getSequentialQuestionTxtPath()
    targetPath = configParser.getSequentialTargetTxtPath()

    f = open(questionsPath,'r',encoding='utf8')
    questions = f.readlines()
    f.close()

    edgar_results = open(targetPath,'w',encoding='utf8')

    for query in questions:

        #defaultAgentsAnswers = multipleAnswerSelection.provideAnswer(query)
        defaultAgentsAnswers = {}
        externalAgentsAnswers = agentManager.generateAgentsAnswers(query)
        # Both defaultAgentsAnswers and externalAgentsAnswers are dictionaries in the format {'agent1': 'answer1', 'agent2': 'answer2'}
        

        # Calling the DecisionMaker after having all of the answers stored in the above dictionaries
        answer = decisionMaker.decideBestAnswer(defaultAgentsAnswers,externalAgentsAnswers)


        print("Question:", query)
        print("Final Answer:", answer)
        print()

        edgar_results.write("Q - " + query)
        edgar_results.write("A - " + answer + '\n\n')


    edgar_results.close()





def multiAgentAnswerMode():

    """
    Multiagent mode for SSS. It is composed by three main modules, each with its own role: MultipleAnswerSelection, AgentManager and DecisionMaker

    Initializes main modules:
    - MultipleAnswerSelection will give us the answers from the classic SSS's agents
    - AgentManager will generate our external agents and retrieve their answers
    - DecisionMaker will receive both the answers from MultipleAnswerSelection and AgentManager, and will decide the best answer to give to the user

    The final answer decided by DecisionMaker is then printed to the user
    """

    multipleAnswerSelection = MultipleAnswerSelection()
    agentManager = AgentManager()
    decisionMaker = DecisionMaker(configParser.getDecisionMethod())

    if("PrioritySystem" in configParser.getDecisionMethod()):
        print("Current priority agents (whose answers will be prioritized): ")
        for agentName in configParser.getPriorities().keys():
            print(agentName)
        print()

    # SSS workloop
    while True:
        query = ""

        while (query == ""):
            query = input("Say something:\n")
            print()

        if query == "exit":
            break;

        logging.basicConfig(filename='logs/log' + time.strftime('%d%m%Y_%H%M%S') + '.txt', filemode='w', format='%(message)s', level=logging.INFO)
        logging.info("Query: " + query)

        #defaultAgentsAnswers = multipleAnswerSelection.provideAnswer(query)
        defaultAgentsAnswers = {}

        externalAgentsAnswers = agentManager.generateAgentsAnswers(query)
        # Both defaultAgentsAnswers and externalAgentsAnswers are dictionaries in the format {'agent1': 'answer1', 'agent2': 'answer2'}
        

        # Calling the DecisionMaker after having all of the answers stored in the above dictionaries
        answer = decisionMaker.decideBestAnswer(defaultAgentsAnswers,externalAgentsAnswers)


        logging.info("Query: " + query)
        logging.info("Answer: " + answer)


        print()
        print("Question:", query)
        print("Final Answer:", answer)
        print()


def learningMode():
    wm = WeightedMajority()
    wm.learnWeights()




if __name__ == "__main__":
    dialogue()


#TODO mode evaluation
#TODO mode learning
