import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

public class XML_Parser {
	
	public void parse_patent(String patent_location) {
		
		File f = new File(patent_location);
		String line; 
		String pat_no = patent_location.split("/")[1];
		
		
		try {
			FileReader fileReader = new FileReader(f);
			BufferedReader bufferedReader = new BufferedReader(fileReader);			
			FileWriter fileWriter = new FileWriter("ParsedPatents/" + pat_no);
			BufferedWriter bufferedWriter = new BufferedWriter(fileWriter);
			
			boolean add_classifications = true;
			String title = null;
			String appl_type = null;
			String section = null;
			String main_class = null;
			String subclass = null;
			String maingroup = null;
			String subgroup = null;
			String mainclassification = null;
			String furtherclassification = null;
			String doc_no = null;
			String category = null;


			while((line = bufferedReader.readLine()) != null) {
				
				//INVENTION TITLE
				if(line.contains("<invention-title")) {
					title = line.split("\">")[1].split("</")[0];
					bufferedWriter.write("TITLE: " + title);
					bufferedWriter.newLine();
				}
				
				//APPLICATION TYPE
				if(line.contains("appl-type")) {
					appl_type = line.split("appl-type=")[1].split("\">")[0];
					bufferedWriter.write("APPL_TYPE: " + appl_type);
					bufferedWriter.newLine();
				}
				
				//SECTION
				if(line.contains("<section>")) {
					section = line.split("section>")[1].split("<")[0];
				}
				
				//CLASS
				if(line.contains("<class>")) {
					main_class = line.split("class>")[1].split("<")[0];
				}
				
				//SUBCLASS
				if(line.contains("<subclass>")) {
					subclass = line.split("subclass>")[1].split("<")[0];
				}
				
				//MAIN-GROUP
				if(line.contains("<main-group>")) {
					maingroup = line.split("main-group>")[1].split("<")[0];
				}
				
				//SUBGROUP
				if(line.contains("<subgroup>") & add_classifications) {
					subgroup = line.split("subgroup>")[1].split("<")[0];
					bufferedWriter.write("CLASSIFICATION: " + section + "." + main_class + "." + subclass + "." + maingroup + "." + subgroup);
					bufferedWriter.newLine();
				}
				
				//FURTHER CLASSIFICATIONS
				if(line.contains("<main-classification>") & add_classifications) {
					mainclassification = line.split(">")[1].split("<")[0];
					bufferedWriter.write("MAIN_CLASSIFICATION: " + mainclassification);
					bufferedWriter.newLine();
				}
				if(line.contains("<further-classification>") & add_classifications) {
					furtherclassification = line.split(">")[1].split("<")[0];
					bufferedWriter.write("FURTHER_CLASSIFICATION: " + furtherclassification);
					bufferedWriter.newLine();
				}
				
				//END CLASSIFICATION COLLECTION
				if(line.contains("<patcit")) {
					add_classifications = false;
				}
				
				//CITATION INFO
				if(line.contains("<doc-number>")) {
					doc_no = line.split("<doc-number>")[1].split("<")[0];
				}
				if(line.contains("<category>")) {
					category = line.split("<category>")[1].split("<")[0];
				}
				if(line.contains("</us-citation>")) {
					bufferedWriter.write("CITATION: " + doc_no + " " + category);
					bufferedWriter.newLine();
				}
				
				//AUTHOR AND ASSIGNEE
				
				//TEXT INFORMATION
				
				}
				bufferedReader.close();
				bufferedWriter.close();
			
		} catch(FileNotFoundException e) {
			System.out.println("Unable to open file.");
		} catch(IOException e) {
			System.out.println("Error reading file.");
		}
		
	}
}
