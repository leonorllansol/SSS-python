package lucene_resources;

import java.io.Serializable;

public class SimpleQA implements Serializable {
    private long previousQA;
    private String question;
    private String answer;
    private String normalizedQuestion;
    private String normalizedAnswer;
    private long diff;

    public SimpleQA(long previousQA, String question, String answer, String normalizedQuestion, String normalizedAnswer, long diff) {
        this.previousQA = previousQA;
        this.question = question;
        this.answer = answer;
        this.normalizedAnswer = normalizedAnswer;
        this.normalizedQuestion = normalizedQuestion;
        this.diff = diff;
    }

    public String getQuestion() {
        return question;
    }

    public String getAnswer() {
        return answer;
    }

    public String getNormalizedQuestion() {
        return normalizedQuestion;
    }

    public String getNormalizedAnswer() {
        return normalizedAnswer;
    }

    public long getDiff() {
        return diff;
    }

    public long getPreviousQA() {
        return previousQA;
    }
}
