from .FaqsAgent.FaqsAgent import FaqsAgent
from .MixAgent.MixAgent import MixAgent
from .SimplestAgent.SimplestAgent import SimplestAgent
from xml.dom import minidom
from xml.dom.minidom import Node
import os
import re



def agentHandler(configs):
    mainClass = configs['mainClass']

    if(mainClass == 'FaqsAgent'):
        return FaqsAgent(configs)
    
    elif(mainClass == 'MixAgent'):
        return MixAgent(configs)







def createExternalAgents(externalAgentsPath):
    externalAgents = [] 

    configFiles = getConfigFiles(externalAgentsPath)


    for config in configFiles:

        configs = {}
        configDoc = minidom.parse(config)
        
        for elem in configDoc.getElementsByTagName('config'):
            for x in elem.childNodes:
                if(x.nodeType == Node.ELEMENT_NODE):
                    configs[x.tagName] = x.firstChild.data
        
        agent = agentHandler(configs)
        externalAgents.append(agent)
    
    return externalAgents



def getConfigFiles(dirName):
    directories = os.listdir(dirName)
    configFiles = []
    for d in directories:
        fullpath = os.path.join(dirName, d)
        if os.path.isdir(fullpath):
            configFiles = configFiles + getConfigFiles(fullpath)
        elif fullpath.endswith('config.xml'):
            configFiles.append(fullpath)
    return configFiles