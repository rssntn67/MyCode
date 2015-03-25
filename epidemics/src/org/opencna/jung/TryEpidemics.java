package org.opencna.jung;

import org.apache.commons.collections15.Factory;

import edu.uci.ics.jung.algorithms.generators.random.EppsteinPowerLawGenerator;
import edu.uci.ics.jung.graph.Graph;
import edu.uci.ics.jung.graph.SparseMultigraph;

class AreaNetwork {
    static int nodeCount=0;
	int size;
	int infected;
	int id;

	public AreaNetwork() {
		this.id = nodeCount++;
	}
	
	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}	
	
	public int getSize() {
		return size;
	}
	public void setSize(int size) {
		this.size = size;
	}
	public int getInfected() {
		return infected;
	}
	public void setInfected(int infected) {
		this.infected = infected;
	}
	
	public String toString() {
		return "V"+id;
	}
}

class AreaNetworkLink {
    static int nodeCount=0;

	int id;
    int capacity;
    
	public AreaNetworkLink() {
		this.id = nodeCount++;
	}
	

	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}

	public int getCapacity() {
		return capacity;
	}

	public void setCapacity(int capacity) {
		this.capacity = capacity;
	}

	public String toString() {
		return "E"+id;
	}
}

class GraphFactory implements Factory<Graph<AreaNetwork, AreaNetworkLink>> {

	public Graph<AreaNetwork,AreaNetworkLink> create() {
		return new SparseMultigraph<AreaNetwork, AreaNetworkLink>();
	}
	
}

class VertexFactory implements Factory<AreaNetwork> {

	public AreaNetwork create() {
		return new AreaNetwork();
	}
	
}

class EdgeFactory implements Factory<AreaNetworkLink> {

	public AreaNetworkLink create() {
		
		return new AreaNetworkLink();
	}	
}

public class TryEpidemics {

	public static void main (String args[]) {
		int vertexes = 26;
		int links = 50;
		int iters = 50;
		
		Graph<AreaNetwork, AreaNetworkLink> g = 
			new EppsteinPowerLawGenerator<AreaNetwork,AreaNetworkLink>(
					new GraphFactory(),new VertexFactory(),new EdgeFactory(), vertexes, links, iters).create();
		System.out.println(g.toString());
		
		for (AreaNetwork an: g.getVertices()) {
			Double db = new Double(Math.random()*100+10);
			an.setSize(db.intValue());
			an.setInfected(0);
		}
		
		
	}
}
