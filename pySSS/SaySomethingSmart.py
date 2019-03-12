from answers import HighestWeightedScoreSelection
import logging, sys
import configParser, subprocess

def dialogue(): #mode dialogue
    #trying not to create every classes every time a question is asked
    highestWeightedScoreSelection = HighestWeightedScoreSelection()
    #--Lucene init--
    list_args = ["java", "LuceneWrapper", "0", configParser.getCorpusPath(), "", configParser.getLanguage(), configParser.getIndexPath(), configParser.getHitsPerQuery(), configParser.getDbPath()]
    sp1 = subprocess.Popen(list_args,shell=False)

    exitCode = sp1.wait()
    #--------------
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
