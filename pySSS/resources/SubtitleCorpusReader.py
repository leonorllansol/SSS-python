from os import walk
from dialog import SimpleQA
from org.apache.lucene.document import Document, TextField, Field

import transaction

def read(writer, dbroot, corpusDir):  #missing arg: normalizers
    files = []

    #extract filenames from corpus directory
    for (dirpath, dirnames, filenames) in walk(corpusDir):
        files.extend(filenames)
        break

    i = 0

    for filename in files:
        print("Creating lucene indexes and database for", filename, "...")
        filepath = corpusDir+'/'+filename
        file = open(filepath, 'r')

        lineNum = 0
        previousDialogId = 0
        internalId = -1

        line = file.readline()

        while (line):
            lineNum += 1

            if not line.strip():        #skip empty lines
                line = file.readline()
                continue;

            temp = line
            assert temp.startswith("SubId")
            subId = getSubstringAfterHyphen(temp)

            temp = file.readline()
            lineNum += 1
            assert temp.startswith("DialogId")
            dialogId = int(getSubstringAfterHyphen(temp))

            temp = file.readline()
            lineNum += 1
            assert temp.startswith("Diff")
            diff = float(getSubstringAfterHyphen(temp))

            temp = file.readline()
            lineNum += 1
            assert temp.startswith("I")
            question = getSubstringAfterHyphen(temp)

            temp = file.readline()
            lineNum += 1
            assert temp.startswith("R")
            answer = getSubstringAfterHyphen(temp)

            answer = answer.strip()

            normalizedAnswer = normalize(answer)
            normalizedQuestion = normalize(question)

            #apply normalization to answer and question
            if dialogId == previousDialogId + 1:
                simpleQA = SimpleQA.SimpleQA(internalId, question, normalizedQuestion, answer, normalizedAnswer, diff)
            else:
                simpleQA = SimpleQA.SimpleQA(-1, question, normalizedQuestion, answer, normalizedAnswer, diff)

            dbroot['simpleQAs'][lineNum] = simpleQA    #db.store(simpleQA);

            del simpleQA
            previousDialogId = dialogId

            addDoc(writer, question, str(lineNum)) #using lineNum as id

            line = file.readline()

        #print("final:", lineNum)
        i += 1

        print()

        if i % 200 == 0:
            transaction.commit()

    transaction.commit()
        #for sqa in dbroot['simpleQAs'].values():
        #    print(sqa.getDiff())

def getSubstringAfterHyphen(temp):
    return temp[temp.index('-') + 2:]

def addDoc(writer, question, answer):
    doc = Document()
    doc.add(TextField('question', question, Field.Store.YES))
    doc.add(TextField('answer', answer, Field.Store.YES))
    writer.addDocument(doc)

def normalize(query):
    query_normalized = query.lower()
    puncts = ['"','.','?','!',',', '\n']
    for sym in puncts:
        query_normalized = query_normalized.replace(sym, '')
    return query_normalized
