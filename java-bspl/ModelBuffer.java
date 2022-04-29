
import java.util.Dictionary;
import java.util.Hashtable;
import java.util.Enumeration;

public class ModelBuffer {
	
	private static Dictionary<String, String> dictionary = new Hashtable<String, String>();
	private String result = null;
	private static int counter = 0;
	
	public ModelBuffer(){
		if (counter == 0){
			dictionary.put("R2D2", "learningModelR2D2");
			counter++;
		} 
	}

	
	public boolean lookFor(String model){
		result = dictionary.get(model);
		
		if(result != null){
			return true;
		}
		else {
			return false;
		}
	}
	
	public String getModel(){
		return result;
	}
	
	public void save(String model, String result){
		System.out.println("Buffer:\t\t speichere " + model + "-" + result);
		dictionary.put(model, result);
	}
	
	private void status(){
		Enumeration<String> key = dictionary.keys();
		while(key.hasMoreElements())
			System.out.print(key.nextElement() + ", ");
		
	}
}
