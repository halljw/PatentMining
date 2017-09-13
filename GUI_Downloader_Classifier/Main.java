import javax.swing.JOptionPane;

import java.io.BufferedOutputStream;
import java.io.File;
import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;

import javax.swing.JFrame;

/**
 * The HallModelPatentClassifier implements a simple
 * program which conducts basic text analysis of
 * patent documents, trains machine learning models
 * for document classification, and tests efficacy
 * of the trained models.
 * 
 * @author 	Hall_John
 * @version 1.0
 * @since 	2017-08-26
 *
 */

public class Main {

	/**
	 * The main method of the classifier which
	 * initializes the primary JFrame of the
	 * interface as Menu m.
	 * 
	 * @param args
	 */
	public static void main(String[] args) {
		
		/*
		 * Constructs necessary directory structure if not
		 * already existent. Presently constructs:
		 * 	- PatentData
		 * 		- A
		 * 		- B
		 * 		- C
		 * 		- D
		 * 		- E
		 * 		- F
		 * 		- G
		 * 		- H
		 * 	- RawData
		 */
		File_Hierarchy_Maker maker = new File_Hierarchy_Maker();
		maker.make_hierarchy();
		
		Menu m = new Menu();
		m.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		m.setSize(1000,1000);
		m.setVisible(true);
		
		
		//Text_Analyzer ta = new Text_Analyzer(new File("PatentData\\A\\US00000001"));
		//ta.print_clean_text();
		//ta.analyze_text();
		
		/*
		 * DOWNLOADER SECTION, FOR WHENEVER I GET IT WORKING
		 */
		//File file = new File("downloadFileNames");
		//downloader d = new downloader(file);
		//d.printList();
		
		/*
		 * SEPARATE AND PARSE PATENTS
		 */
		//XML_separator xs = new XML_separator();
		//xs.read_file();
		//XML_parser xp = new XML_parser();
		//xp.parse_patent("SeparatedPatents/US09532496");
		
		}
	}