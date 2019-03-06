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

def getHitsPerQuery():
    hitsPerQuery = mydoc.getElementsByTagName('hitsPerQuery')[0]
    return hitsPerQuery.firstChild.data

def getNormalizersPath():
    normalizerPath = mydoc.getElementsByTagName('normalizersPath')[0]
    return normalizerPath.firstChild.data

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

def getReferencesFolder():
    folder = mydoc.getElementsByTagName('folder')[0]
    return folder.firstChild.data

def getReferencesInteractions():
    interactions = mydoc.getElementsByTagName('interactions')[0]
    return interactions.firstChild.data

def getReferencesLines():
    lines = mydoc.getElementsByTagName('lines')[0]
    return lines.firstChild.data

def getReferencesInputSize():
    inputSize = mydoc.getElementsByTagName('inputSize')[0]
    return inputSize.firstChild.data
