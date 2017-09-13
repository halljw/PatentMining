import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * The Text_Analyzer method implements a rudimentary analysis of 
 * text douments. Intended for use with the HallModelPatentClassifier.
 * 
 * Analyzes a patent file:
 * 	- Contains raw text
 * 	- Contains word-tokenized ArrayList of clean text
 * 	- Tokenized text lower case, punctuation and stop words removed by default
 * Quantitative analysis of cleaned text:
 * 	- Number of words
 * 	- Vocab size
 * 	- Lexical diversity
 * 	- 10 most common words
 * 
 * @author 	Hall_John
 * @version	1.0
 * @since	2017-08-26
 */


// REWORK THIS FROM SCRACH
// IN PARTICULAR, FOCUS ON SEPARATING THE TEXT BY SECTION


public class Text_Analyzer {

	private final String PUNCTUATION = "`~!@#$%^&*()-_=+[{]}\\|:;'\",<.>/?";
	private final ArrayList<String> STOP_WORDS = new ArrayList<String>(Arrays.asList("a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has", "he", "in", "is", "it", "its", "of", "on", "that", "the", "to", "was", "were", "will", "with"));
	private File patent;
	private boolean remove_punctuation;
	private boolean remove_stop_words;
	private String raw_text;
	private String spec_text;
	
	private String title;
	private String appl_type;
	private String classification;
	private String main_classification;
	private ArrayList<String> further_classifications;
	private ArrayList<String> citations;
	private ArrayList<String> authors_assignees;
	
	private ArrayList<String> tokenized_text;
	private int total_words;
	private int vocabulary_count;
	private double lexical_diversity;
	private Map<String, Integer> word_counts;
	
	public String get_raw_text(){
		return this.raw_text;
	}
	
	public Text_Analyzer(File patent, boolean remove_punctuation, boolean remove_stop_words) {
		this.patent = patent;
		this.remove_punctuation = remove_punctuation;
		this.remove_stop_words = remove_stop_words;
		this.raw_text = read_file(patent);
		this.tokenized_text = clean_text();
	}
	
	public Text_Analyzer(File patent) {
		this.patent = patent;
		this.remove_punctuation = true;
 		this.remove_stop_words = true;
		this.raw_text = read_file();
		this.tokenized_text = clean_text();
	}
	
	/**
	 * This method reads the analyzer's designated
	 * file and converts it to a usable String 
	 * variable.
	 * @return String The text read from the file
	 */
	public String read_file() {
		String text = "";
		try {
			FileReader fileReader = new FileReader(this.patent);
			BufferedReader bufferedReader = new BufferedReader(fileReader);	
			String line;
			while((line = bufferedReader.readLine()) != null) {
				text += line + "\n";
				
			}
			bufferedReader.close();
			} catch(IOException e) {
				System.out.println("Error reading file.");
			}
		return text;
	}

	/**
	 * This method converts a String of text into an
	 * ArrayList of words. A space character is taken to
	 * indicate a word boundary.
	 * @param text Raw String to be tokenized
	 * @return ArrayList<String> contained tokens within the text
	 */
	public ArrayList<String> tokenize(String text) {
		ArrayList tokenized_text = new ArrayList<String>();
		for(String item : text.split(" ")){
			tokenized_text.add(item);
		}
		return tokenized_text;
	}
	
	
	public ArrayList<String> clean_text() {
		String clean_text = this.raw_text.toLowerCase();
		if (this.remove_punctuation)
			clean_text = remove_punctuation(clean_text);
		ArrayList<String> tokenized_text = tokenize(clean_text);
		if (this.remove_stop_words)
			tokenized_text = remove_stop_words(tokenized_text);
		return tokenized_text;
	}
	
	/**
	 * Removes punctuation from a String.
	 * 
	 * @param raw_text
	 * @return String containing no punctuation
	 */
	public String remove_punctuation(String raw_text) {
		String clean_text = "";
		for(int i = 0; i<raw_text.length(); i++){
			if (-1 == PUNCTUATION.indexOf(raw_text.charAt(i))){
				clean_text += raw_text.charAt(i);
			}
		}
		return clean_text;
	}
	
	/**
	 * Removes stop words from an array of tokenized words.
	 * 
	 * @param raw_text Tokenized words of a text
	 * @return ArrayList containing the same tokenized words less stops
	 */	
	public ArrayList<String> remove_stop_words(ArrayList<String> raw_text) {
		ArrayList<String> clean_text = new ArrayList<String>();
		for (String word : raw_text){
			if (!STOP_WORDS.contains(word)) {
				clean_text.add(word);
			}
		}
		return clean_text;
	}
	
	public void print_clean_text(){
		for(String word : this.tokenized_text) {
			System.out.println(word);
		}
	}
	
	public String display_basic_info(){
		String results = "";
		/*
		"TITLE:";
		"APPL_TYPE:";
		"CLASSIFICATION:";
		"CITATION:";
		"SPECIFICATION:";
		"CLAIM:";
		*/
		
		for(String line : this.raw_text.split("\n")){
			if(!line.contains("SPECIFICATION") & !line.contains("CLAIM")){
				if(line.split(":::")[0].length() > 8){
					results += line.split(":::")[0].substring(0, 8) + ":\t" + line.split(":::")[1] + "\n";					
				}
				else {
					results += line.split(":::")[0] + ":\t" + line.split(":::")[1] + "\n";
				}
			}
		}
		return results;
	}
	
	public String analyze_text(){
		String results = "";
		total_words();
		vocabulary_count();
		lexical_diversity();
		word_counts();
		most_common_words();
		return results;
	}
	
	public void total_words(){
		this.total_words = this.tokenized_text.size();
	}
	
	public void vocabulary_count(){
		ArrayList<String> already_seen = new ArrayList<String>();
		for(String word : this.tokenized_text){
			if(!already_seen.contains(word)){
				already_seen.add(word);
			}
		}
		this.vocabulary_count = already_seen.size();
	}
	
	public void lexical_diversity(){
		this.lexical_diversity = (double)this.vocabulary_count/this.total_words;
	}
	
	public Map<String, Integer> word_counts(){
		Map<String, Integer> word_counts = new HashMap<String, Integer>();
		for(String word : this.tokenized_text){
			if(!word_counts.containsKey(word)){
				word_counts.put(word, new Integer(1));
			}
			else {
				word_counts.put(word, word_counts.get(word) + 1);
			}
		}
		this.word_counts = word_counts;
		return word_counts;
	}
	
	public void most_common_words(){
		int counter = 10;
		ArrayList<String> most_common = new ArrayList<String>();
		while(counter > 0){
			for(String word_i : this.word_counts.keySet()){
				if(!most_common.contains(word_i)){
					String greatest = word_i;
					for(String word_j : this.word_counts.keySet()){
						if(word_counts.get(greatest) < word_counts.get(word_j) & !most_common.contains(word_j)){
							greatest = word_j;
						}
					}
					most_common.add(greatest);
					counter--;
					break;
				}
			}
		}
		for(String word : most_common){
			System.out.println(word);
		}
	}
	
}
