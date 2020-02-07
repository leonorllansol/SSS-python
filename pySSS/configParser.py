from xml.dom import minidom

# parse an xml file by name
mydoc = minidom.parse('config/config.xml')

def getSimilarityMeasure():
    similarityMeasures = mydoc.getElementsByTagName('similarityMeasure')
    elems = []
    weights = []
    for elem in similarityMeasures:
        elems.append(elem.attributes['name'].value)
        weights.append(elem.attributes['weight'].value)
    return elems, weights

def getEvaluators():
    criteria = mydoc.getElementsByTagName('criterion')
    elems = []
    for elem in criteria:
        if elem.attributes['weight'].value != '0':
            if elem.attributes['name'].value == 'SimpleConversationContext':
                elems.append((elem.attributes['name'].value, elem.attributes['weight'].value, elem.attributes['nPreviousInteractions'].value))
            else:
                elems.append((elem.attributes['name'].value, elem.attributes['weight'].value, '0'))
    return elems

def getNormalizers():
    normalizersStrings = mydoc.getElementsByTagName('normalizers')[0]
    return (normalizersStrings.firstChild.data).split(',')

def getDbPath():
    dbPath = mydoc.getElementsByTagName('dbPath')[0]
    return dbPath.firstChild.data

def getNoAnswerMessage():
    language = getLanguage()
    if language == 'english':
        noAnswerMessage = mydoc.getElementsByTagName('noAnswerFoundEN')[0]
    elif language == 'portuguese':
        noAnswerMessage = mydoc.getElementsByTagName('noAnswerFoundPT')[0]
    return noAnswerMessage.firstChild.data

def getHitsPerQuery():
    hitsPerQuery = mydoc.getElementsByTagName('hitsPerQuery')[0]
    return hitsPerQuery.firstChild.data

def usePreviouslyCreatedIndex():
    usePreviouslyCreatedIndex = mydoc.getElementsByTagName('usePreviouslyCreatedIndex')[0]
    if(usePreviouslyCreatedIndex.firstChild.data == 'true'):
        return True
    else:
        return False


def getNormalizersPath():
    normalizerPath = mydoc.getElementsByTagName('normalizersPath')[0]
    return normalizerPath.firstChild.data

def getExternalAgentsPath():
    externalAgentsPath = mydoc.getElementsByTagName('externalAgentsPath')[0]
    return externalAgentsPath.firstChild.data

def getLanguage():
    language = mydoc.getElementsByTagName('language')[0]
    return language.firstChild.data

def getIndexPath():
    indexPath = mydoc.getElementsByTagName('indexPath')[0]
    return indexPath.firstChild.data

def getCorpusPath():
    corpusPath = mydoc.getElementsByTagName('corpusPath')[0]
    return corpusPath.firstChild.data

def getStopWordsPath():
    stopWordsPath = mydoc.getElementsByTagName('stopwords')[0]
    return stopWordsPath.firstChild.data

def getDefaultAgentsMode():
    defaultAgentsMode = mydoc.getElementsByTagName('defaultAgentsMode')[0]
    return defaultAgentsMode.firstChild.data


def getDecisionMethod():
    decisionMethod = mydoc.getElementsByTagName('decisionMethod')[0]
    return decisionMethod.firstChild.data

def getSequentialQuestionTxtPath():
    questionTxtFile = mydoc.getElementsByTagName('questionTxtFile')[0]
    return questionTxtFile.firstChild.data

def getSequentialTargetTxtPath():
    sequentialTargetTxtFile = mydoc.getElementsByTagName('sequentialTargetTxtFile')[0]
    return sequentialTargetTxtFile.firstChild.data

def getAnswerAmount():
    answerAmount = mydoc.getElementsByTagName('answerAmount')[0]
    return int(answerAmount.firstChild.data)


def getInteractionsPath():
    interactionsPath = mydoc.getElementsByTagName('interactions')[0]
    return interactionsPath.firstChild.data

def getLinesPath():
    linesPath = mydoc.getElementsByTagName('lines')[0]
    return linesPath.firstChild.data

def getInputSize():
    inputSize = mydoc.getElementsByTagName('inputSize')[0]
    return int(inputSize.firstChild.data)

def getDecimalPlaces():
    decimalPlaces = mydoc.getElementsByTagName('decimalPlaces')[0]
    return int(decimalPlaces.firstChild.data)

def getEtaFactor():
    etaFactor = mydoc.getElementsByTagName('etaFactor')[0]
    return int(etaFactor.firstChild.data)

def getLearningStrategy():
    learningStrategy = mydoc.getElementsByTagName('strategy')[0]
    return learningStrategy.firstChild.data

def getWeightResults():
    weightResults = mydoc.getElementsByTagName('weightResults')[0]
    return eval(weightResults.firstChild.data)
    
def getInitialWeights():
    initialWeights = mydoc.getElementsByTagName('initialWeights')[0]
    return eval(initialWeights.firstChild.data)




def getPriorities():
    agents = mydoc.getElementsByTagName('agent')
    priorityDoc = {}
    for agent in agents:
        priorityDoc[agent.attributes['name'].value] = int(agent.attributes['priority'].value)
    return priorityDoc