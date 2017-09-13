import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.GridLayout;
import java.awt.Panel;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.io.File;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.Arrays;
import java.awt.event.ActionEvent;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JTextField;
import javax.swing.JPasswordField;
import javax.swing.JScrollBar;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.JOptionPane;

import javax.swing.JTree;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.TreeNode;
import javax.swing.tree.TreePath;


/**
 * The primary menu GUI of the classifier
 * consists of three primary panels:
 * 	- A browser showing available patent documents
 * 	- A command panel showing available actions to
 * 		be applied to selected documents
 * 	- A text panel displaying relevant messages/
 * 		results of applied actions.
 * 
 * @author Hall_John
 *
 */
public class Menu extends JFrame{
	
	//PRIMARY PANELS AND COMPONENTS
	private Panel file_browser_panel;
	private Panel buttons_panel;
	private Panel results_panel;
	
	private JButton display_patent_info;
	private JButton analyze_patent_text;
	private JButton import_files;
	private JTextArea analysis_results;
	
	/*
	 * Currently only handles one file at a time.
	 */
	private File selected_file;
	
	private File_Browser file_browser;
	private Text_Analyzer text_analyzer;
		
	/**
	 * Constructor for Menu. The JFrame consists of
	 * three panels:
	 * 	- FILE_BROWSER
	 * 	- BUTTONS
	 * 	- RESULTS
	 */
	public Menu() {
		super("The Hall Model Patent Classifier");
		
		// PRIMARY PANEL LAYOUT
		setLayout(new GridLayout(1, 3, 1, 1));
		this.file_browser_panel = new Panel();
		this.buttons_panel = new Panel();
		this.results_panel = new Panel();
		add(this.file_browser_panel);
		add(this.buttons_panel);
		add(this.results_panel);
		
		// 		FILE_BROWSER_PANEL LAYOUT
		this.file_browser_panel.setLayout(new GridLayout(1, 1, 0, 0));
		this.file_browser = new File_Browser(new File("PatentData"));
		this.file_browser.getTree().addMouseListener(new File_Browser_Mouse_Listener());
		this.file_browser_panel.add(this.file_browser.getJSP());
		
		// 		BUTTON_PANEL LAYOUT
		this.buttons_panel.setLayout(new GridLayout(3, 1, 1, 1));

		// 			DISPLAY_PATENT_INFO BUTTON
		this.display_patent_info = new JButton("Display Patent Info");
		this.display_patent_info.addActionListener(new Display_Patent_Info_Listener());
		this.display_patent_info.setEnabled(false);
		this.buttons_panel.add(this.display_patent_info);
		
		//			ANALYZE_PATENT_TEXT BUTTON
		this.analyze_patent_text = new JButton("Analyze Patent Text");
		this.analyze_patent_text.addActionListener(new Analyze_Patent_Text_Listener());
		this.analyze_patent_text.setEnabled(false);
		this.buttons_panel.add(this.analyze_patent_text);
		
		//			IMPORT_FILES BUTTON
		this.import_files = new JButton("Import Patent Files");
		this.import_files.addActionListener(new Import_Files_Listener());
		this.buttons_panel.add(this.import_files);
		
		// 		RESULTS_PANEL LAYOUT
		this.results_panel.setLayout(new GridLayout(1, 1, 1, 1));
		this.analysis_results = new JTextArea("Results will go here.");
		this.results_panel.add(this.analysis_results);		
	}

	//GET AND SET METHODS
	public JButton get_display_patent_info_button(){
		return this.display_patent_info;
	}
	
	public JButton get_analyze_patent_text_button(){
		return this.analyze_patent_text;
	}	
	
	public File_Browser get_file_browser(){
		return this.file_browser;
	}
	
	public void set_text_analyzer(Text_Analyzer ta){
		this.text_analyzer = ta;
	}
	
	public Text_Analyzer get_text_analyzer(){
		return this.text_analyzer;
	}
	
	public void set_selected_file(File file){
		this.selected_file = file;
	}

	public File get_selected_file(){
		return this.selected_file;
	}
	
	public void set_analysis_results(JTextArea text){
		this.analysis_results = text;
	}
	
	public JTextArea get_analysis_results(){
		return this.analysis_results;
	}
	
	/**
	 * Mouse listener for selecting files in the
	 * file browser panel. Selecting a file
	 * enables analysis buttons; selecting a
	 * directory disables analysis buttons.
	 * 
	 * Single click selects the given file
	 * Double click displays patent info (if clicked
	 * item is a file)
	 * 
	 * @author Hall_John
	 *
	 */
	private class File_Browser_Mouse_Listener extends MouseAdapter{
		public void mouseClicked(MouseEvent e) {
			String path = "";
			DefaultMutableTreeNode node = (DefaultMutableTreeNode)
					get_file_browser().getTree().getLastSelectedPathComponent();
			if (node == null) {
				return;	
			}
			else {
				for(TreeNode n : node.getPath()){
					path += n.toString() + File.separator;	
				}
				set_selected_file(new File(path));
				if (get_selected_file().isFile()){
					get_display_patent_info_button().setEnabled(true);
					get_analyze_patent_text_button().setEnabled(true);	
				}
				else {
					get_display_patent_info_button().setEnabled(false);
					get_analyze_patent_text_button().setEnabled(false);							
				}							
			}
			if (e.getClickCount() == 2) {
				get_display_patent_info_button().doClick();
			}
		}
	}
	
	

	/**
	 * Action listener for Display_Patent_Info Button
	 * Creates Text_Analyzer for the selected file, extracts
	 * basic info from that file.
	 * 
	 * @author Hall_John
	 *
	 */
	private class Display_Patent_Info_Listener implements ActionListener{
		public void actionPerformed (ActionEvent e){
			set_text_analyzer(new Text_Analyzer(get_selected_file()));
			get_analysis_results().setText(get_text_analyzer().display_basic_info());
		}
	}

	/**
	 * Action listener for Analyze_Patent_Text Button
	 * 
	 * UNIMPLEMENTED
	 * 
	 * @author Hall_John
	 *
	 */
	private class Analyze_Patent_Text_Listener implements ActionListener{
		public void actionPerformed (ActionEvent e){
			get_analysis_results().setText("THIS ONE WORKS, TOO");
			
		}
	
	}
	
	/**
	 * Action listener for Import_Files button
	 * Creates a Download_Checkbox menu in which
	 * user can download additional files.
	 * 
	 * @author Hall_John
	 *
	 */
	private class Import_Files_Listener implements ActionListener{
		public void actionPerformed (ActionEvent e){
			Download_Checkbox dc = new Download_Checkbox();
		}
	}
	
}
