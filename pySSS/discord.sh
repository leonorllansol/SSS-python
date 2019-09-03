#change to match lucene directory and version
LUCENE_DIR=/home/hawke/Work/SSS-python/lucene-7.7.1
LUCENE_VERSION=7.7.1
#change to match db4o directory
DB4O_DIR=/home/hawke/Work/SSS-python/

export CLASSPATH=${LUCENE_DIR}/core/lucene-core-${LUCENE_VERSION}.jar:$CLASSPATH
export CLASSPATH=${LUCENE_DIR}/demo/lucene-demo-${LUCENE_VERSION}.jar:$CLASSPATH
export CLASSPATH=${DB4O_DIR}/db4o-8.0.249.16098-core-java5.jar:$CLASSPATH
export CLASSPATH=${LUCENE_DIR}/queryparser/lucene-queryparser-${LUCENE_VERSION}.jar:$CLASSPATH
export CLASSPATH=${LUCENE_DIR}/analysis/common/lucene-analyzers-common-${LUCENE_VERSION}.jar:$CLASSPATH

javac lucene_resources/SimpleQA.java
javac -d . lucene_resources/SimpleQA.java
javac lucene_resources/SubtitleCorpusReader.java
javac -d . lucene_resources/SubtitleCorpusReader.java
javac lucene_resources/CorpusReader.java
javac -d . lucene_resources/CorpusReader.java
javac LuceneWrapper.java

python MultiagentBotEng.py
