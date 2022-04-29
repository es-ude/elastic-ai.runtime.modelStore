


public class EmbeddedSystem {
	
	private String name;
	private ServiceConnection service = new ServiceConnection();
	
	
	public EmbeddedSystem(String name){
		this.name = name;
	}
	
	public String getName(){
		return name;
	}
	
	public void load(String model){
		model = service.connectForSearch(model);
		System.out.println("Embedded System: " + model); 
	}	
	
}
