# Say Something Smart

## What is it?

Say Something Smart (SSS) is a dialogue engine based on a large corpus of movie subtitles (Subtle). 

This specific branch is focused on the implementation of a plug-and-play system composed by multiple distinct agents: each agent gives its own response to the received user input, and the best answer is reached through a formally estabilished consensus strategy.


## How does it work?

Upon receiving input from the user, SSS retrieves the most similar candidates (that is, entries of the Subtle corpus) through Lucene and sends both the user query and the Lucene candidates to all available agents. Subsequently, each agent gives its own answer to the query, and the best answer is delivered to the user.

This process is accomplished through the use of four modules: 
- The `LuceneWrapper` module, which indexes the Subtle corpus and allows the other SSS modules to retrieve the best candidates to a query.
- The `DefaultAnswers` module, which, given a user query, generates the answers of the default SSS agents to that query.
- The `AgentManager` module, which initializes all of the external agents and, upon receiving a user query, delivers the necessary information (query, Lucene candidates) to each external agent. It also stores the answers of each external agent.
- The `DecisionMaker` module, which receives the answers generated by the DefaultAnswers and AgentManager modules, and based on a voting strategy, decides the best answer to give to the user. It will also be the module that manages the weight each agent has on the final answer.



---
# Getting Started

### **Requirements:**
- [Python 3](https://www.python.org/downloads/)
- [Java Development Kit](https://www.oracle.com/technetwork/java/javase/downloads/index.html)
- [Lucene's binary release](https://lucene.apache.org/core/downloads.html)

Extract Lucene's binary release (preferentially to the same folder where pySSS is located) and install nltk through the command:

    pip3 install nltk

Open your `setup.sh` file (which should be located inside the pySSS folder) and edit the following variables:
- `LUCENE_DIR` corresponds to the directory where the binary release of Lucene was extracted.
- `LUCENE_VERSION` is the version of your Lucene release.
- `DB4O_DIR` is the directory where the file `db4o-8.0.249.16098-core-java5.jar` is located (it should correspond to the path pointing to this repository).

For example:

    LUCENE_DIR=/home/hawke/Work/SSS-python/lucene-7.7.1
    LUCENE_VERSION=7.7.1
    DB4O_DIR=/home/hawke/Work/SSS-python/

The rest of the script content should be kept intact, as not to break the building process.

Afterwards, run `setup.sh` through the following command (note that you should only have to run it in your first time building the project):

    . setup.sh

Finally, to try out running SSS, execute the command:

    python3 SaySomethingSmart.py

The program should prompt you to *"Say something:"*. Once it does, type your query (for example, *"Como te chamas?"*), and hit Enter. The answers from each agent should appear on the screen, along with SSS's final answer.

When you're done with interacting, type `exit` to terminate the program.

---
# How-To: Create New Agents

An external agent, in the context of SSS, is defined by two components: the configuration file, and the source code.

The configuration file serves as the "header" of the agent for SSS: it allows the agent to be detected and added to the pool of available agents, and it also allows the user to set configurable parameters without directly interacting with the source code. Each agent has its own configuration file.

The source code of the agent is composed by one or more source files, which have the goal of delivering an answer upon receiving a user query (and, optionally, a set of Lucene candidates).


## 1. Paths and Directories

Before you start building your new agent, you should know where it should be placed in order to be found by SSS.

For the context of building agents, the folder structure of SSS is as follows:

    pySSS
    └── resources
        └── externalAgents
            ├── AgentFactory.py
            ├── Agent1
            │   ├── config.xml
            │   └── Agent1.py
            └── Agent2
                ├── config.xml
                └── Agent2.py

When creating a new agent, the directory containing the source code and config file of the agent should be inside the `externalAgents` folder, and the configuration file of the agent **must** be named `config.xml`.

To start off, let's create a new folder inside `externalAgents` called `SimplestAgent`, which will be our `HelloWorld` for this tutorial.

## 2. Source Code

As mentioned before, an agent can have more than one source file, but it must have a **main** source file. The main file usually has the same name as the agent's folder, and it corresponds to the connection point between SSS and the agent.

That said, the following indications must be followed when creating a new agent:

- The agent's main file must be implemented as a `class`;
- The agent's class must implement the function `requestAnswer(self,userInput,candidates)`, which receives a `userInput` string and a `candidates` array, and must return an `answer` string.

To give a simple example, if we wanted to implement an agent that always delivered the same answer to the user regardless of the input or the candidates, we could create a file called `SimplestAgent.py` inside the `SimplestAgent` directory that contained the following code:

    class SimplestAgent:
        def requestAnswer(self,userInput,candidates):
           return "This is a very good answer!"
    

When SSS requests the answer of each agent, it does so by calling the function `agent.requestAnswer(userInput,candidates)`, and expects to receive a string corresponding to the agent's answer to the userInput in return.

- `userInput` is a string that contains a query made directly to SSS by the user (e.g.: "Como te chamas?").
- `candidates` is an array containing the generated Lucene candidates for the above user query in the format `[CandidateObject1, CandidateObject2, ... , CandidateObjectN]`. Candidate objects correspond to instances of the `SimpleQA` class, found in:

        pySSS
        └── dialog
            ├── BasicQA.py
            └── SimpleQA.py

Building agents that use the provided Lucene candidates is explored in a further section of this guide.


## 3. Configuration File

To create and interact with each individual agent, the `AgentManager` searches for all `config.xml` files inside the `externalAgents` directory and subdirectories. In order to be found by the `AgentManager`, each agent has a configuration file where its configurable parameters are defined.

When creating the `config.xml` file for your agent, you should follow the structure below:

    <config>
        <mainClass>agentName</mainClass>
        (other parameters to define)
        (...)
    </config>

All defined parameters must be encapsulated by the exterior tag `<config>`, and the `<mainClass>`must be defined with the same name as the main class of the agent.

For example, in the case of our `SimplestAgent` presented earlier, the `config.xml` would be located inside the `SimplestAgent` folder and contain something like this:

    <config>
        <mainClass>SimplestAgent</mainClass>
    </config>

When this configuration file is parsed by the `AgentManager`, a `configs` dictionary will be generated in the format `{'mainClass': 'SimplestAgent'}`, which can subsequently be passed to the agent class.

After having created this file, our new agent is ready to roll. When SSS is instantiated again, the `AgentFactory` class will detect our new `config.xml`. The `mainClass` parameter tells the `AgentFactory` which class it has to import (in this case, it tells the `AgentFactory` to import the `SimplestAgent` class) and it will automatically generate an instance of our new agent. 

From this point on, upon receiving a user query, the `AgentManager` will then send that query to the `SimplestAgent`, as well as to all other available agents.


## 4. Conclusion

So far, we have covered the basics of adding a new agent to our system. If you followed the steps for the creation of the `SimplestAgent`, upon running SaySomethingSmart again and making a query, you should notice that the agent is already interacting with the system.

    Answer from agent SimplestAgent: 
    This is a very good answer!

In the following sections, we will cover how to make use of the Lucene candidates and explore the implementation details of SSS's architecture further.




---
# How-To: Use Lucene Candidates In Our Agents

As mentioned earlier, all agents receive a set of candidates that can help them with the task of deciding an answer. 

Lucene is given a source corpus comprising of Question-Answer pairs to index and search: upon receiving input from the user, Lucene searches for the candidate pairs whose `question` is most similar to the given input. These candidates are then passed to each agent, where they can be used to help that agent reach an answer.

This is especially useful for agents that base themselves on lexical clues, as we will see in the following tutorial. In this next tutorial, we will create a simple agent that takes the Lucene candidates into account.


## 1. Initial Set-Up of the Agent

For starters, let's follow in the footsteps of what we learned in the previous tutorial about creating a new agent. I'm calling this one `MixAgent`, but feel free to name your agents however you like it.

As such, let's create a new folder inside `/externalAgents/`, as well as a new configuration file and the source file for our `MixAgent`:

    pySSS
    └── resources
        └── externalAgents
            └── MixAgent
                ├── config.xml
                └── MixAgent.py

There should also be an `AgentFactory.py` inside the `/externalAgents/` folder, as well as any other agent folders you have created. We'll leave them alone for this tutorial.

To get our agent up and running, we will also need to have the `mainClass` parameter defined inside our configuration file, which should look similar to this:

    <config>
        <mainClass>MixAgent</mainClass>
    </config>

We'll eventually come back to this configuration file, but it should rest for a bit while we build the main source code for our agent.

As we covered before, an agent's main file must be a python class, and it must implement a `requestAnswer` function in the format `requestAnswer(self,userInput,candidates)`. While the `userInput` is simply a `string` containing the input from the user, the `candidates` object is an array in the format `[CandidateObject1, CandidateObject2, ... , CandidateObjectN]`, with each of these objects being an instance of the `SimpleQA` class.

But what exactly is a `SimpleQA`?



## 2. The SimpleQA Class

To sum it up in a line, the `SimpleQA` class is a way of converting the text data inside a given corpus into a format that SSS can actually understand. We've mentioned multiple times that our corpora are composed by Question-Answer pairs, but let's actually take a look at an entry of the corpus:

    SubId - 1000
    DialogId - 1
    Diff - 1
    I - Qual o teu nome?
    R - Chamo-me Afonso Coentro Morcela

As it was originally built to specifically support SubTle, a corpus based on movie subtitles, the fields `SubId`, `DialogId` and `Diff` all refer to parameters specific to subtitles, with the first two parameters being identifiers to the movie and dialog section, and the last parameter being the time difference between the end of the first subtitle and the beginning of the second one.

The `I` stands for "Interaction", and it is the equivalent of our "Question", while `R` stands for "Response", and subsequently corresponds to our "Answer". That specific corpus entry would likely be selected as a candidate if we gave an input that contained the words "qual" and "nome" to SSS, as those would be recognized as similar to the "Question" field.

If we take a look at the `SimpleQA.py` class file, the following parameters are initialized on creation:

    def __init__(self, previousQA, question, normalizedQuestion, answer, normalizedAnswer, diff):
        self.previousQA = previousQA    #is a number
        self.question = question
        self.answer = answer
        self.normalizedAnswer = normalizedAnswer
        self.normalizedQuestion = normalizedQuestion
        self.diff = diff
        self.scores = {}

Let's go over each of these:

- `previousQA` is a pointer to the QA pair immediately before this one in the corpus;
- `diff` is, as covered before, the time difference between the two subtitles;
- `question` and `normalizedQuestion` are both forms of the "Question" field, with the last one having the configured `Normalizers` applied on it;
- The same applies to `answer` and `normalizedAnswer`, but for the "Answer" field;
- Finally, `scores` is a dictionary in the form {"AgentName": Score} where we can access the score given to a QA Pair by any of the agents that evaluated it.

Knowing where to look and which parameters to access is vital to obtain successful results for our agents, and we will use these same parameters in the next step of the tutorial to build our `MixAgent`.

## 3. Building the MixAgent

We have been discussing corpora, questions and answers, but we have not decided the most important aspect of our agent yet. What will it actually _do_ to find an answer?

In the beginning of this tutorial, we estabilished that we wanted to use the Lucene `candidates` provided by the `AgentManager`, and of course, we are trying to answer any `userQuery` that we receive.

The SimpleQA class tells us that we have access to two main parameters for the most likely candidates: the `question` and the `answer`. With that in mind, why not try to find a candidate whose `question` is very similar to the user query, but also shares some words with the `answer`?

That brings us to the issue of how similarity is measured. While there are methods such as counting words in common, we intend to adopt the Jaccard Similarity for the purpose of this tutorial. In this context, the Jaccard Similarity is calculated by taking two sets of words and dividing the intersection of those two sets by their union, as represented by the following line of code:

    len(setA.intersection(setB)) / len(setA.union(setB))

In this case, we'll be comparing both the `question` and the `answer` of each candidate with the `userInput` given by SSS, and as such, we can write the following to compute the _question similarity_ and the _answer similarity_:

    def requestAnswer(self,userInput,candidates):
        userInputWords = self.getWordSet(userInput)

        for c in candidates:
            questionWords = self.getWordSet(c.getNormalizedQuestion())
            answerWords = self.getWordSet(c.getNormalizedAnswer())

            questionScore = len(userInputWords.intersection(questionWords)) / len(userInputWords.union(questionWords))
            answerScore = len(userInputWords.intersection(answerWords)) / len(userInputWords.union(answerWords))
    
    def getWordSet(self,input):
        wordSet = set(input.split())
        return wordSet


The `getWordSet()` function is an auxiliary function built to transform each `string` into an array of words, and we obtain both the `questionScore` and the `answerScore` for each candidate by computing the Jaccard Similarity between the question/answer and the user query.

Now that we can obtain these scores, we'll need a way to keep track of the candidate with the best score in order to deliver it to the user, and that's where the `scores` dictionary from the `SimpleQA` class shines:



    def __init__(self,configs):
        self.agentName = self.__class__.__name__

    def requestAnswer(self,userInput,candidates):
        userInputWords = self.getWordSet(userInput)
        bestPair = candidates[0]

        for c in candidates:
            questionWords = self.getWordSet(c.getNormalizedQuestion())
            answerWords = self.getWordSet(c.getNormalizedAnswer())

            questionScore = len(userInputWords.intersection(questionWords)) / len(userInputWords.union(questionWords))
            answerScore = len(userInputWords.intersection(answerWords)) / len(userInputWords.union(answerWords))

            finalScore = questionScore + answerScore
            c.addScore(self.agentName,finalScore)

            if(c.getScoreByEvaluator(self.agentName) > bestPair.getScoreByEvaluator(self.agentName)):
                bestPair = c
        
        return bestPair.getAnswer()

    def getWordSet(self,input):
        wordSet = set(input.split())
        return wordSet

Through the `addScore()` method, we can keep track of the score given to each candidate, and we can easily compare scores given to different candidates through the `getScoreByEvaluator()` method. The final score is given to the candidate with the highest sum of `questionScore` and `answerScore`.

This raises another issue: what if we wanted to give a greater weight to `questionScore`? Answers that are too similar or identical to the original user query might not be appropriate responses, and these values might need manual tweaking, which is not recommended for values directly in the code.

Since we do not want to insert direct values in the code, we can take another approach and insert them in the configuration file instead:

    <config>
        <mainClass>MixAgent</mainClass>
        <questionSimValue>0.7</questionSimValue>
        <answerSimValue>0.3</answerSimValue>
    </config>

Then, all we need to do is to initialize these values in our code and to take them into account when delivering the final score:


    class MixAgent:
        def __init__(self,configs):
            self.agentName = self.__class__.__name__
            self.questionSimValue = float(configs['questionSimValue'])
            self.answerSimValue = float(configs['answerSimValue'])

        def requestAnswer(self,userInput,candidates):
            userInputWords = self.getWordSet(userInput)
            bestPair = candidates[0]

            for c in candidates:
                questionWords = self.getWordSet(c.getNormalizedQuestion())
                answerWords = self.getWordSet(c.getNormalizedAnswer())

                questionScore = len(userInputWords.intersection(questionWords)) / len(userInputWords.union(questionWords))
                answerScore = len(userInputWords.intersection(answerWords)) / len(userInputWords.union(answerWords))

                finalScore = self.getFinalScore(questionScore,answerScore)
                c.addScore(self.agentName,finalScore)

                if(c.getScoreByEvaluator(self.agentName) > bestPair.getScoreByEvaluator(self.agentName)):
                    bestPair = c

            return bestPair.getAnswer()

        def getWordSet(self,input):
            wordSet = set(input.split())
            return wordSet

        def getFinalScore(self,questionScore,answerScore):
            return questionScore * self.questionSimValue + answerScore * self.answerSimValue

From this point on, we can edit the weights through the `config.xml` without having to mess around with the code, and our `MixAgent` is now ready to go into action.

    Say something:
    Como te chamas?

    Answer from agent MixAgent: 
    Yuri.

    Answer from agent SimplestAgent: 
    This is a very good answer!

    Question: Como te chamas?
    Final Answer: Yuri.

In the next tutorial, we will explore the available decision methods, as well as how to build agents who use specific corpus, rather than being limited to the default.