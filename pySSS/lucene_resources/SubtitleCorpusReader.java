package lucene_resources;

import com.db4o.ObjectContainer;
import org.apache.lucene.index.IndexWriter;
//import SimpleQA;
//import sss.texttools.Cleaner;
//import sss.texttools.normalizer.Normalizer;

import java.io.*;
import java.text.NumberFormat;
import java.util.List;
import java.util.Arrays;

public class SubtitleCorpusReader extends CorpusReader {


    @Override
    public void read(IndexWriter writer, ObjectContainer db, File[] files) throws IOException {

//        Cleaner c = new Cleaner(); // Marco

        int i = 0;

        for (File file : files) {

            System.out.println("Creating lucene indexes and database for " + file.getName() + "...");
            BufferedReader reader = new BufferedReader(new FileReader(file.getCanonicalPath()));

            String line;

            String subId;
            String question;
            String answer;

            long internalId = -1;
            int previousDialogId = 0;
            long totalLines = count(file.getCanonicalPath());
            long step = totalLines / 1000;
            long lineNum = 0;

            // Marco
//            System.out.println(((double)(i*100) / files.length));

            while ((line = reader.readLine()) != null) {

                lineNum++;
                //if ((lineNum % step) == 0) {
                //    System.out.println(getPercentage(lineNum, totalLines));
                //}

                if (line.trim().length() == 0) {
                    continue;
                }

                String temp = line;
                assert (temp.startsWith("SubId"));
                subId = getSubstringAfterHyphen(temp);

                temp = reader.readLine(); lineNum++;
                assert (temp.startsWith("DialogId"));
                int dialogId = Integer.parseInt(getSubstringAfterHyphen(temp));

                temp = reader.readLine(); lineNum++;
                assert (temp.startsWith("Diff"));
                long diff = Long.parseLong(getSubstringAfterHyphen(temp));

                temp = reader.readLine(); lineNum++;
                assert (temp.startsWith("I"));
                question = getSubstringAfterHyphen(temp); //assumes the corpus does not have empty questions

                temp = reader.readLine(); lineNum++;
                assert (temp.startsWith("R"));
                answer = getSubstringAfterHyphen(temp); //assumes the corpus does not have empty answers

                answer = answer.trim();

                String normalizedAnswer = normalize(answer);
                String normalizedQuestion = normalize(question);
                // Marco
//                String normalizedAnswer = c.cleanAndNormalize(answer);
//                String normalizedQuestion = c.cleanAndNormalize(question);

                SimpleQA simpleQA;

                if (dialogId == previousDialogId + 1) {
                    simpleQA = new SimpleQA(internalId, question, answer, normalizedQuestion, normalizedAnswer, diff);
                } else {
                    simpleQA = new SimpleQA(-1, question, answer, normalizedQuestion, normalizedAnswer, diff);
                }

                db.store(simpleQA);
                internalId = db.ext().getID(simpleQA);
                simpleQA = null;
                previousDialogId = dialogId;
                addDoc(writer, normalizedQuestion, String.valueOf(internalId));
            }

            i++;
            System.out.println();

            // Marco
            if (i % 200 == 0) {
                db.commit();
            }
        }

        db.commit();
    }

    private String normalize(String query){
        String query_normalized = query.toLowerCase();
        List<String> puncts = Arrays.asList(".","?","!",",", "\n", "-");
        for (String sym : puncts){
            query_normalized = query_normalized.replace(sym, "");
        }
        return query_normalized;
    }


    private String getPercentage(long partial, long total) {
        NumberFormat defaultFormat = NumberFormat.getPercentInstance();
        defaultFormat.setMinimumFractionDigits(1);
        return defaultFormat.format(partial / (double) total);
    }

    private String getSubstringAfterHyphen(String temp) {
        return temp.substring(temp.indexOf('-') + 2, temp.length());
    }

    private int count(String filename) throws IOException {
        InputStream is = new BufferedInputStream(new FileInputStream(filename));
        try {
            byte[] c = new byte[1024];
            int count = 0;
            int readChars = 0;
            boolean endsWithoutNewLine = false;
            while ((readChars = is.read(c)) != -1) {
                for (int i = 0; i < readChars; ++i) {
                    if (c[i] == '\n')
                        ++count;
                }
                endsWithoutNewLine = (c[readChars - 1] != '\n');
            }
            if(endsWithoutNewLine) {
                ++count;
            }
            return count;
        } finally {
            is.close();
        }
    }
}
