

public class ServiceConnection {
	
	private Service service = new Service();
			
	public String connectForSearch(String model){
		return service.handleSearch(model);
	}
	
}
