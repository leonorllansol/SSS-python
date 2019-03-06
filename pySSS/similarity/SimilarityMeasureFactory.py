from .SimilarityMeasure import Jaccard, Dice, EditDistance

def createSimilarityMeasures(similarityMeasures):
    similarity_measures = []
    for i in range(0, len(similarityMeasures[0])):
        weight = similarityMeasures[1][i]
        if similarityMeasures[0][i] == "Jaccard":
            similarity_measures.append(Jaccard(weight))
        elif similarityMeasures[0][i] == "Dice":
            similarity_measures.append(Dice(weight))
        elif similarityMeasures[0][i] == "EditDistance":
            similarity_measures.append(EditDistance(weight))
    return similarity_measures
