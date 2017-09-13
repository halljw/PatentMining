import static org.junit.Assert.*;

import java.io.File;

import org.junit.Test;

public class read_file_test {

	@Test
	public void test() {
		File file = new File("Testing\\test1.txt");
		Text_Analyzer test = new Text_Analyzer(file);
		String actual = test.read_file();
		//System.out.println(text);
		String expected = "Hello, world. My name is John! :)\n";
		assertEquals(actual, expected);
	}

}
