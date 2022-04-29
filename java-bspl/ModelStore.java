
import java.util.Dictionary;
import java.util.Hashtable;


public class ModelStore{

	private Dictionary<String, String> store = new Hashtable<String, String>();
	private String result = null;
	
	public ModelStore(){
		store.put("K11", "K11-Learning-Model");
		store.put("ImageReco2", "ImageReco2-Learning-Model");
		store.put("R2D2-Version2", "R2D2-Version2-Learning-Model");
	}
	 
	 
	public String getModel(String model){
		result = store.get(model);
		if(result != null){
			return result;
		} else {
			return "NotFound";
		}
	}
}
