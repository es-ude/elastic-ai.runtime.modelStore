

public class StoreConnection {
	private ModelStore store = new ModelStore();
	
	
	public StoreConnection(){
	}
	
	public String connectForSearch(String model){
		return store.getModel(model);
		
	}
}
