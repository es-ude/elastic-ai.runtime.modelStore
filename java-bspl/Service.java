

public class Service {
	private ModelBuffer buffer = new ModelBuffer();  //"Pseudo-Singelton"
	
	private StoreConnection storeConnection = new StoreConnection();
	private String result;
	
	public Service(){
	}
		
	public String handleSearch(String model){
		
		if (buffer.lookFor(model)) {
			System.out.println("Service:\t im Buffer vorhanden ...");
			return buffer.getModel();
						
		} else {
			System.out.println("Service:\t nicht im Buffer vorhanden ...");
			result = storeConnection.connectForSearch(model);
			
			if(result.equals("NotFound")) {
				System.out.println("Service:\t im Store nicht gefunden");
				return "NotFound";
			} else {
				System.out.println("Service:\t im Store gefunden");
				buffer.save(model, result);
				return result;
			  }
		  }	
	}
	
	
}
