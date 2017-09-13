import java.io.File;

public class File_Hierarchy_Maker {

	private final String[] SECTIONS = new String[]{"A", "B", "C", "D", "E", "F", "G", "H"};
	//private final String[] A_CLASSES = new String[]{"01", "21", "22", "23", "24", "41", "42", "43", "44", "45", "46", "47", "61", "62", "63"};
	//private final String[] SUBCLASSES;
	//private final String[] GROUP;
	//private final String[] SUBGROUP;
	
	//public File_Hierarchy_Maker(){
	//	
	//}
	
	public void make_hierarchy(){
		if (! new File("PatentData").exists()) {
			new File("PatentData").mkdirs();
			for(String letter : new String[]{"A", "B", "C", "D", "E", "F", "G", "H"}) {
				new File("PatentData\\" + letter).mkdirs();
			}
		}
		else {
			for(String letter : new String[]{"A", "B", "C", "D", "E", "F", "G", "H"}) {
				if (! new File("PatentData\\" + letter).exists()){
					new File("PatentData\\" + letter).mkdirs();	
				}
			}
		}
		
		if (! new File("RawData").exists()) {
			new File("RawData").mkdirs();
		}
	}
}
