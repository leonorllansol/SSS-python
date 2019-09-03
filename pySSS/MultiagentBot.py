from DefaultAnswers import HighestWeightedScoreSelection, MultipleAnswerSelection
import logging, sys, time
import configParser, subprocess
from DecisionMaker import DecisionMaker
from AgentManager import AgentManager
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import Token
from discord import utils



defaultAgentsMode = configParser.getDefaultAgentsMode()

if(not configParser.usePreviouslyCreatedIndex()):
    list_args = ["java", "LuceneWrapper", "0", configParser.getCorpusPath(), "", configParser.getLanguage(), configParser.getIndexPath(), configParser.getHitsPerQuery(), configParser.getDbPath()]
    sp1 = subprocess.Popen(list_args,shell=False)

    exitCode = sp1.wait()
    
    
        
bot = Bot(command_prefix='~')

    


    
multipleAnswerSelection = MultipleAnswerSelection()
agentManager = AgentManager()
decisionMaker = DecisionMaker(configParser.getDecisionMethod())


@bot.event
async def on_message(message):
    if(not message.author.bot):
        query = message.content


        logging.basicConfig(filename='log_edgar_' + time.strftime('%d%m%Y_%H%M%S') + '.txt', filemode='w', format='%(message)s', level=logging.INFO)
        logging.info("Query: " + query)

        

        #defaultAgentsAnswers = multipleAnswerSelection.provideAnswer(query)
        defaultAgentsAnswers = {}

        externalAgentsAnswers = agentManager.generateAgentsAnswers(query)
        # Both defaultAgentsAnswers and externalAgentsAnswers are dictionaries in the format {'agent1': 'answer1', 'agent2': 'answer2'}
        

        # Calling the DecisionMaker after having all of the answers stored in the above dictionaries
        answer = decisionMaker.decideBestAnswer(defaultAgentsAnswers,externalAgentsAnswers)


        logging.info("\n")
        logging.info("Query: " + query)
        logging.info("Final Answer: " + answer)


        print("Question:", query)
        print("Final Answer:", answer)
        print()

        await message.channel.send(answer)
    
    elif(message.author.id == bot.user.id):
        await message.add_reaction('✅')
        await message.add_reaction('❌')
        await message.add_reaction('❔')

    await bot.process_commands(message)







bot.run(Token.token)