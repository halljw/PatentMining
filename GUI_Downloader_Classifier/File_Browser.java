import java.awt.Dimension;
import java.io.File;

import javax.swing.JFrame;
import javax.swing.JScrollBar;
import javax.swing.JScrollPane;
import javax.swing.JTree;
import javax.swing.SwingUtilities;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.DefaultTreeModel;

public class File_Browser {

	private JTree tree;
	private DefaultMutableTreeNode root;
	private JScrollPane jsp;
	private JScrollBar bar;
	
	public File_Browser(File file) {
		this.root = new DefaultMutableTreeNode(file.getName());
		getChildNodes(file, this.root);
		this.tree = new JTree(this.root);
		this.tree.setRootVisible(false);
		this.tree.setShowsRootHandles(true);
		this.jsp = new JScrollPane(tree,
				JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED,
				JScrollPane.HORIZONTAL_SCROLLBAR_NEVER);
		this.bar = jsp.getVerticalScrollBar();
		this.bar.setPreferredSize(new Dimension(50, 0));
	}
	
	public JTree getTree(){
		return this.tree;
	}
	
	public JScrollPane getJSP() {
		return this.jsp;
	}
	
	
	/*
	http://www.codejava.net/java-se/swing/jtree-basic-tutorial-and-examples
	*/
	
	public void getChildNodes(File fileRoot, DefaultMutableTreeNode root) {
		for (File f : fileRoot.listFiles()) {
			DefaultMutableTreeNode child = new DefaultMutableTreeNode(f.getName());
			root.add(child);
			if (f.isDirectory()) {
				getChildNodes(f, child);
			}
		}
		
	}
}
