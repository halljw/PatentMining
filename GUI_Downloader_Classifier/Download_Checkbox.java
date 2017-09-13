import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.util.ArrayList;

import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;


// NEEDS A LOGFILE OF THOSE ALREADY DOWNLOADED


public class Download_Checkbox extends JFrame{
	
	private ArrayList<String> already_downloaded;
	private final String[] ZIP_FILES_2017 = new String[]{
			"170103",
			"170110",
			"170117",
			"170124",
			"170131",
			"170207",
			"170214",
			"170221",
			"170228",
			"170307",
			"170314",
			"170321",
			"170328",
			"170404",
			"170411",
			"170418",
			"170425",
			"170502",
			"170509",
			"170516",
			"170523",
			"170530",
			"170606",
			"170613",
			"170620",
			"170627",
			"170704",
			"170711",
			"170718",
			"170725",
			"170801",
			"170808",
			"170815",
			"170822",
			"170829"
	};
	private final String[] ZIP_FILES_2016 = new String[]{
			"160105"
	};
	private ArrayList<JCheckBox> files = new ArrayList<JCheckBox>();
	private JButton import_selected_files = new JButton("Import Selected Files");
		
	public Download_Checkbox(){
		super("Import Files");
		
		//ADD SCROLL BAR TO THIS
		setLayout(new GridLayout(1, 2, 1, 1));
		JPanel text_panel = new JPanel();
		JPanel checklist_panel = new JPanel();
		checklist_panel.setLayout(new GridLayout(1, 2, 1, 1));
		text_panel.add(new JLabel("Please check zip files to be downloaded."));
		text_panel.add(this.import_selected_files);
		Import_Selected_Files_Listener isfl = new Import_Selected_Files_Listener();
		this.import_selected_files.addActionListener(isfl);
		add(text_panel);
		
		JPanel checklist_2017 = new JPanel();
		JPanel checklist_2016 = new JPanel();
		JScrollPane jsp_2017 = new JScrollPane(checklist_2017);
		JScrollPane jsp_2016 = new JScrollPane(checklist_2016);
		
		
		int rows_2017 = ZIP_FILES_2017.length;
		checklist_2017.setLayout(new GridLayout(rows_2017, 1, 4, 4));
		for(String file : ZIP_FILES_2017){
			JCheckBox box = new JCheckBox(file);
			box.setName(file);
			checklist_2017.add(box);
			files.add(box);
		}
		checklist_panel.add(jsp_2017);

		int rows_2016 = ZIP_FILES_2016.length;
		checklist_2016.setLayout(new GridLayout(rows_2016, 1, 4, 4));
		for(String file : ZIP_FILES_2016){
			JCheckBox box = new JCheckBox(file);
			box.setName(file);
			checklist_2016.add(box);
			files.add(box);
		}
		checklist_panel.add(jsp_2016);		
		
		add(checklist_panel);
		
		setSize(700, 700);
		setVisible(true);
	}
	
	private class Import_Selected_Files_Listener implements ActionListener{
		
		public void actionPerformed(ActionEvent e) {
			
			for(JCheckBox box : getFiles()) {
				if(box.isSelected()){
					String num = box.getName();
					String fileName = "RawData" + File.separator + "ipg" + num + ".zip";
					System.out.println(box.getName());
					
					Downloader d = new Downloader(num);
					
					d.downloadZipFile();
					d.unZipFile(fileName);
					d.deleteFile(fileName);
				}
			}
			
		}
	}
	
	public ArrayList<JCheckBox> getFiles(){
		return this.files;
	}
	
	public void get_already_downloaded(){
		
	}
	
}
