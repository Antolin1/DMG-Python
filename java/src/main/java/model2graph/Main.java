package model2graph;

import org.eclipse.emf.ecore.EObject;
import org.eclipse.emf.ecore.resource.Resource;
import org.jgrapht.Graph;
import org.jgrapht.graph.DefaultEdge;


public class Main {
	
	public static void main(String[] args) {
		//read input parameters
	}
	
	public static Graph<Node, Edge> getGraph(Resource r){
		return null;
	}
	
	public static class Node {
		
		EObject object;

		public Node(EObject object) {
			super();
			this.object = object;
		}

		public EObject getElement() {
			return object;
		}

		@Override
		public int hashCode() {
			final int prime = 31;
			int result = 1;
			result = prime * result + ((object == null) ? 0 : object.hashCode());
			return result;
		}

		@Override
		public boolean equals(Object obj) {
			if (this == obj)
				return true;
			if (obj == null)
				return false;
			if (getClass() != obj.getClass())
				return false;
			Node other = (Node) obj;
			if (object == null) {
				if (other.object != null)
					return false;
			} else if (!object.equals(other.object))
				return false;
			return true;
		}

		@Override
		public String toString() {
			return object.eClass().getName();
		}
		
		
	}
	
	public static class Edge extends DefaultEdge {
		
		String label;

		public Edge(String label) {
			super();
			this.label = label;
		}

		public String getLabel() {
			return label;
		}

		public void setLabel(String label) {
			this.label = label;
		}
		
		
		
		
	}

}
