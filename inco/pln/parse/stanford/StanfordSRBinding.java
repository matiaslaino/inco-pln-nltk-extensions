// javac -cp {};{};{};.;*;stanford-parser.jar  StanfordSRBinding.java

import edu.stanford.nlp.ling.TaggedWord;
import edu.stanford.nlp.parser.shiftreduce.ShiftReduceParser;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.PrintWriter;
import java.util.ArrayList;

public class StanfordSRBinding {
    public static void main(String[] args) {
        String modelPath = null;
        String inputPath = null;
        String outputPath = "output.txt";

        for (int argIndex = 0; argIndex < args.length; ) {
            switch (args[argIndex]) {
                case "-input":
                    inputPath = args[argIndex + 1];
                    argIndex += 2;
                    break;
                case "-model":
                    modelPath = args[argIndex + 1];
                    argIndex += 2;
                    break;
                case "-output":
                    outputPath = args[argIndex + 1];
                    argIndex += 2;
                default:
                    //throw new RuntimeException("Unknown argument " + args[argIndex]);
            }
        }

        try {

            ShiftReduceParser model = ShiftReduceParser.loadModel(modelPath);

//        Not available for spanish.
//        model.setOptionFlags("-factored", "-outputFormat", "penn,typedDependencies");

            ArrayList<TaggedWord> taggedWords = new ArrayList<TaggedWord>();

            File file = new File(inputPath);

            BufferedReader br = new BufferedReader(new FileReader(file));
            String line;
            while ((line = br.readLine()) != null) {
                int lastIndex = line.lastIndexOf('/');
                String posTag = line.substring(lastIndex + 1);
                String word = line.substring(0, lastIndex);

                taggedWords.add(new TaggedWord(word, posTag));
            }
            br.close();

            String resultTreeStr = model.parse(taggedWords).toString();

            PrintWriter out = new PrintWriter(outputPath);
            out.println(resultTreeStr);
            out.close();
        } catch (Exception ex) {
            System.err.println(ex.getMessage());
        }
    }
}
