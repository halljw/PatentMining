import java.awt.GridLayout;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.concurrent.TimeUnit;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JProgressBar;
import javax.swing.SwingConstants;
import javax.swing.SwingUtilities;
import javax.swing.WindowConstants;


public class Downloader {
	
	//DO SOME THIS STUFF WITH THIS CLASS
	
	private String target_file;
	private String urlString;
	private JProgressBar jProgressBar;
	private JFrame frame;
	
	
	public Downloader(String target_file){
		
		this.target_file = target_file;
		this.urlString = "https://bulkdata.uspto.gov/data/patent/grant/redbook/fulltext/2017/ipg" + target_file + ".zip";
		this.jProgressBar = new JProgressBar();
		this.jProgressBar.setMaximum(100000);
		this.frame = new JFrame();
        this.frame.setLayout(new GridLayout(2, 1, 1, 1));
        this.frame.add(new JLabel("Downloading " + target_file + ", please wait...", SwingConstants.CENTER));
        this.frame.add(this.jProgressBar);
        this.frame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        this.frame.setSize(300, 150);
        this.frame.setVisible(true);

	}
	
	public JProgressBar getJProgressBar(){
		return this.jProgressBar;
	}
	
	public String getUrlString(){
		return this.urlString;
	}
	
	public String getTargetFile(){
		return this.target_file;
	}
	
	public JFrame getFrame(){
		return this.frame;
	}
	
	public void downloadZipFile() {
		
		Runnable updatethread = new Runnable() {
		public void run(){
			
		
		try {
			URL url = new URL(getUrlString());
			HttpURLConnection httpConnection = (HttpURLConnection) (url.openConnection());
            long completeFileSize = httpConnection.getContentLength();

            java.io.BufferedInputStream in = new java.io.BufferedInputStream(httpConnection.getInputStream());
            java.io.FileOutputStream fos = new java.io.FileOutputStream("RawData\\ipg" + getTargetFile() + ".zip");
            java.io.BufferedOutputStream bout = new BufferedOutputStream(
                    fos, 1024);
            byte[] data = new byte[1024];
            long downloadedFileSize = 0;
            int x = 0;
            while ((x = in.read(data, 0, 1024)) >= 0) {
                downloadedFileSize += x;

                // calculate progress
                final int currentProgress = (int) ((((double)downloadedFileSize) / ((double)completeFileSize)) * 100000d);

                // update progress bar
                SwingUtilities.invokeLater(new Runnable() {

                    @Override
                    public void run() {
                        getJProgressBar().setValue(currentProgress);
                    }
                });

                bout.write(data, 0, x);
            }
            bout.close();
            in.close();
            getFrame().dispose(); 
        } catch (FileNotFoundException e) {
        } catch (IOException e) {
        }}
		};
		Thread t = new Thread(updatethread);
		t.start();
    }
	
	
	public void unZipFile(String zipFileLocation) {
        JFrame frame = new JFrame();
        frame.setLayout(new GridLayout(1, 1, 1, 1));
        frame.add(new JLabel("Unzipping " + zipFileLocation + ", please wait...", SwingConstants.CENTER));
        
        frame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        frame.setSize(300, 150);
        frame.setVisible(true);

		FileInputStream fis;
		byte[] buffer = new byte[1024];
		try {
			fis = new FileInputStream(zipFileLocation);
			ZipInputStream zis = new ZipInputStream(fis);
			ZipEntry ze = zis.getNextEntry();
			while(ze != null) {
				String fileName = ze.getName();
				File newFile = new File("RawData" + File.separator + fileName);
				new File(newFile.getParent()).mkdirs();
				FileOutputStream fos = new FileOutputStream(newFile);
				int len;
				while ((len = zis.read(buffer)) > 0) {
					fos.write(buffer, 0, len);
				}
				fos.close();
				zis.closeEntry();
				ze = zis.getNextEntry();
			}
			zis.closeEntry();
			zis.close();
			fis.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
		frame.dispose();
	}
	
	public void deleteFile(String fileLocation){
		try {
			File file = new File(fileLocation);
			file.delete();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

			
			
			
			
	
	
		
	//Download Zip File
	//Unzip
	//Delete zip file
	//Parse xml files into distinct patents
	//Categorize patents by classification
	//Update filebrowser
	
	
	
	
	

	
}
