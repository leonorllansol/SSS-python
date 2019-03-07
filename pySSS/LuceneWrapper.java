import java.io.BufferedWriter;
import java.io.OutputStreamWriter;
import java.io.FileOutputStream;

import java.io.FileWriter;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.nio.file.Paths;

import com.db4o.Db4oEmbedded;
import com.db4o.ObjectContainer;
import com.db4o.config.EmbeddedConfiguration;

import org.apache.lucene.store.Directory;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.pt.PortugueseAnalyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.document.Document;
import org.apache.lucene.store.MMapDirectory;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;

import lucene_resources.CorpusReader;
import lucene_resources.SubtitleCorpusReader;
import lucene_resources.SimpleQA;


public class LuceneWrapper{
  private Analyzer analyzer;
  private Directory index;
  private IndexSearcher searcher;
  private int hitsPerQuery;
  public static ObjectContainer db;
  public static String DB4OFILENAME = "";

  public static void main(String[] args) throws IOException{
    int flag = Integer.parseInt(args[0]);

    if (flag == 0){   //called from answers.py
      String corpusPath = args[1];
      String query_normalized = args[2];
      String language = args[3];
      String pathOfIndex = args[4];
      String pathOfDb = args[6];

      DB4DB4OFILENAME = Paths.get("").toAbsolutePath().toString() + pathOfDb;

      LuceneWrapper lw = new LuceneWrapper();
      lw.hitsPerQuery = Integer.parseInt(args[5]);
      // Lucene algorithm init
      try {
          lw.initAnalyzer(language);
          lw.index = lw.createIndex(lw.analyzer, pathOfIndex, corpusPath);
      } catch (IOException e) {
          e.printStackTrace();
      }
      IndexReader reader = DirectoryReader.open(lw.index);
      lw.searcher = new IndexSearcher(reader);

      lw.db = Db4oEmbedded.openFile(DB4OFILENAME);

      lw.getCandidates(query_normalized);
    }

    else{  //called from getPreviousQA -- flag is qaId
      LuceneWrapper lw = new LuceneWrapper();
      lw.db = Db4oEmbedded.openFile(DB4OFILENAME);
      SimpleQA simpleQA = lw.getSimpleQA(flag);

      File fileDir = new File("simpleQa.txt");
      BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(fileDir), "UTF-8"));
      writer.write(String.valueOf(simpleQA.getPreviousQA()));
      writer.write("\n");
      writer.write(simpleQA.getQuestion());
      writer.write("\n");
      writer.write(simpleQA.getAnswer());
      writer.write("\n");
      writer.write(simpleQA.getNormalizedQuestion());
      writer.write("\n");
      writer.write(simpleQA.getNormalizedAnswer());
      writer.write("\n");
      writer.write(String.valueOf(simpleQA.getDiff()));
      writer.write("\n");
      writer.close();
    }



  }

  private void initAnalyzer(String language) {
      if (language.equalsIgnoreCase("portuguese")) {
          this.analyzer = new PortugueseAnalyzer();
      } else if (language.equalsIgnoreCase("english")) {
          this.analyzer = new StandardAnalyzer();
      }
  }

  public void getCandidates(String normalizedQuestion){
    try {
        List<Document> luceneDocs = search(normalizedQuestion, this.hitsPerQuery);
        loadLuceneResults(luceneDocs);

    } catch (IOException e) {
        e.printStackTrace();
    } catch (ParseException e) {
        e.printStackTrace();
    }
  }

  private void loadLuceneResults(List<Document> docList) throws IOException{
    File fileDir = new File("luceneresults.txt");
    BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(fileDir), "UTF-8"));
    for (Document d : docList) {
      String qaId = d.get("answer");
      SimpleQA simpleQA = getSimpleQA(Long.parseLong(qaId));
      writer.write(String.valueOf(simpleQA.getPreviousQA()));
      writer.write("\n");
      writer.write(simpleQA.getQuestion());
      writer.write("\n");
      writer.write(simpleQA.getAnswer());
      writer.write("\n");
      writer.write(simpleQA.getNormalizedQuestion());
      writer.write("\n");
      writer.write(simpleQA.getNormalizedAnswer());
      writer.write("\n");
      writer.write(String.valueOf(simpleQA.getDiff()));
      writer.write("\n");
    }
    writer.close();
  }

  public SimpleQA getSimpleQA(long qaId) {
      SimpleQA simpleQA = this.db.ext().getByID(qaId);
      this.db.activate(simpleQA, 1);
      return simpleQA;
  }

  public List<Document> search(String inputQuestion, int hitsPerPage) throws IOException, ParseException {
      TopScoreDocCollector collector = TopScoreDocCollector.create(hitsPerPage);
      Query q = new QueryParser("question", this.analyzer).parse(inputQuestion);
      this.searcher.search(q, collector);
      ScoreDoc[] hits = collector.topDocs().scoreDocs;
      ArrayList<Document> docList = new ArrayList<>();
      for (ScoreDoc scoreDoc : hits) {
          int docId = scoreDoc.doc;
          Document d = this.searcher.doc(docId);
          docList.add(d);
      }
      return docList;
  }

  public Directory createIndex(Analyzer analyzer, String indexDir, String corpusDir) throws IOException{
    File indexDirec = new File(indexDir);
    Directory index = MMapDirectory.open(indexDirec.toPath());
    IndexWriterConfig config = new IndexWriterConfig(analyzer);

    IndexWriter writer = new IndexWriter(index, config);
    writer.deleteAll(); //delete previous lucene files

    File dbFile = new File(DB4OFILENAME);
    dbFile.delete();

    EmbeddedConfiguration db4oConfig = Db4oEmbedded.newConfiguration();
    db4oConfig.file().blockSize(8);
    db4oConfig.file().lockDatabaseFile(false);
    ObjectContainer db = Db4oEmbedded.openFile(db4oConfig, DB4OFILENAME);

    File f = new File(corpusDir);
    File[] files = f.listFiles();
    CorpusReader corpusReader = new SubtitleCorpusReader();
    corpusReader.read(writer, db, files);
    //db4oConfig.file().readOnly(true);
    writer.close();
    db.close();
    return index;
  }
}
