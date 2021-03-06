Say Something Smart (SSS) is a dialogue engine based on a large corpus of movie subtitles (Subtle). SSS receives a user
request and retrieves an answer from a set of candidates that are retrieved from the corpus using Lucene. The selection of the best answer among those candidates is made according to a set of weighted criteria (heuristics), whose weights are previously defined. These criteria use similarity measures to measure the distance between, for example, the user query and a query from one of the Lucene candidates. These similarity measures also have weights that are defined on the file config.xml.
This is a Python implementation of SSS, which was originally implemented in Java. 

# Setup

## Resources

Add your resources to the folder `resources`, found inside the `SSS` folder (see the **Configurations** section below to learn how to include your corpus).

## Requirements

**Python version 3** is required, and so is **nltk**. Nltk can be installed by executing the following command:
```
pip3 install nltk
```
Download Apache Lucene's latest version, and the db4o jar available in https://github.com/leonorllansol/SSS-python/blob/master/db4o-8.0.249.16098-core-java5.jar. 
## Compilation and building
Running the script setup.sh will setup your java environment and compile the java files concerning Lucene. Run it using: 
```
. setup.sh
```

## How to run

```
python3 SaySomethingSmart.py
```

The program can be terminated by typing `exit`.
# Configurations

## Notes about folder structure

When indexing a corpus using Lucene, SSS will look through all the files in the specified corpus folder. Thus, in the event you
need to alternate between different languages, you should keep the corpora for each language in separate folders.
You should have a different folder per language for both the database file (```db.db4o```) and the index files. This folder should be named according to the language selected in the ```config.xml``` file (```english``` or ```portuguese```).

## config.xml
In this file, several settings should be configured before running SSS:

### Language

- `<language>`: `english` or `portuguese`.

### Lucene
- `<dbPath>`: Path (relative to `SSS` folder) to the corpus database file (`db.db4o`) for the selected language. E.g.
```  <dbPath>/resources/luceneDB/portuguese/this.db.db4o</dbPath>```
- `<indexPath>`: Path (relative to `SSS` folder) where the corpus indices are stored. Should end with a folder with the same name as the language selected. E.g.
```<indexPath>resources/luceneIndexes/portuguese</indexPath>```
- `<hitsPerQuery>`: Number of candidates retrieved by Lucene.

### Resources

- `<corpusPath>`: Path (relative to `SSS` folder) to the corpus that should be indexed.
- `<stopwords>`: Path (relative to `SSS` folder) for the list of stopwords for the selected language.

### Normalizers

 - `<normalizers>`: Names of the normalizers to be used (depending on the selected language), separated by commas. They should match the names in the `NormalizerFactory`. Note on the **Portuguese Stemmer Normalizer**: before using this normalizer, run `nltk.download()`, choosing the option *Download all*.
 - `<normalizersPath>`: Path (relative to `SSS` folder) to the file with punctuation to use in the `SimpleNormalizer`.
 
### Similarity

- `<similarityMeasure>`: The similarity measure to be used in some of the criteria, identified by its `name` (should match one of the names in the `SimilarityMeasureFactory`). Each similarityMeasure has a `weight` (an integer value between 0 and 100). There can be more than one similarity measure, and their weights must sum to 100.

### Criteria

- `<criterion>`: Each criterion that will be used to select the best answer, identified by its `name` (should match the name in the `QaScorerFactory`). Each criterion has a `weight` (an integer value between 0 and 100). The sum of the criterion weights should be equal to 100. The `SimpleConversationContext` criterion is also characterized by the `nPreviousInteractions` to consider.

### No answer found messages

- `<noAnswerFoundPT>` and `<noAnswerFoundEN>`: Message to be presented when no answer is retrieved.

# Advanced

## Adding a new similarity measure
- add it to `config.xml` in the form: `<similarityMeasure name="Jaccard" weight="50"/>`
- add class representing the new similarity measure to `SSS/similarity/SimilarityMeasure.py`
- add *if statement* regarding the creation of new similarity measure to `SSS/similarity/SimilarityMeasureFactory.py`

## Adding a new criterion to select best answer (evaluator)
- add it to config.xml in the form: `<criterion name="AnswerFrequency" weight="50"/>`
- add class representing the new criterion to `SSS/dialog/evaluators/QaScorer.py`
- add *if statement* regarding the creation of new similarity measure to `SSS/dialog/evaluators/QaScorerFactory.py`

## Adding a new normalizer
- add it to `config.xml` in the `normalizers` tag
- add class representing the new normalizer to `SSS/texttools/normalizers/normalizer.py`
- add *if statement* regarding the creation of new normalizer to `SSS/texttools/normalizers/normalizerFactory.py`
