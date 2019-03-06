from answers import HighestWeightedScoreSelection
import logging, sys

def dialogue(): #mode dialogue
    #trying not to create every classes every time a question is asked
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


if __name__ == "__main__":
    dialogue()


#TODO mode evaluation
#TODO mode learning
