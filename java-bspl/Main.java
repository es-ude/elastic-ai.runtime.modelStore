


public class Main {

	public static void main(String[] args){
		EmbeddedSystem elasticNode1 = new EmbeddedSystem("elasticNode1");
		EmbeddedSystem elasticNode2 = new EmbeddedSystem("elasticNode2");
		EmbeddedSystem elasticNode3 = new EmbeddedSystem("elasticNode3");
		String separator = "\n ============================================= \n";
		
		System.out.println(separator);
		System.out.println(elasticNode1.getName() + ":\t suche nach Modell R2D2");
		elasticNode1.load("R2D2");
		
		System.out.println(separator);
		System.out.println(elasticNode1.getName() + ":\t suche nach Modell R2D2-Version2");
		elasticNode1.load("R2D2-Version2");
		System.out.println(separator);
		
		
		System.out.println(elasticNode2.getName() + ":\t suche nach nicht vorhandenem Modell SuperHyper");
		elasticNode2.load("SuperHyper");
		System.out.println(separator);
		
		
		
		System.out.println(elasticNode2.getName() + ":\t suche nun nach Modell ImageReco2");
		elasticNode2.load("ImageReco2");
		System.out.println(separator);
	
		System.out.println(elasticNode3.getName() + ":\t suche auch nach ImageReco2; sollte nun im Buffer sein");
		elasticNode3.load("ImageReco2");
		
	}
}
