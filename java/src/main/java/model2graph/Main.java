package model2graph;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.StringWriter;
import java.io.Writer;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.Collection;

import org.eclipse.emf.common.util.TreeIterator;
import org.eclipse.emf.common.util.URI;
import org.eclipse.emf.ecore.EObject;
import org.eclipse.emf.ecore.EPackage;
import org.eclipse.emf.ecore.EReference;
import org.eclipse.emf.ecore.EStructuralFeature;
import org.eclipse.emf.ecore.resource.Resource;
import org.eclipse.emf.ecore.resource.ResourceSet;
import org.eclipse.emf.ecore.resource.impl.ResourceSetImpl;
import org.eclipse.emf.ecore.xmi.impl.XMIResourceFactoryImpl;
import org.eclipse.emf.ecore.xmi.impl.XMIResourceImpl;
import org.jgrapht.Graph;
import org.jgrapht.graph.DefaultEdge;
import org.jgrapht.graph.builder.GraphTypeBuilder;
import org.jgrapht.io.ComponentNameProvider;
import org.jgrapht.io.DOTExporter;
import org.jgrapht.io.IntegerComponentNameProvider;
import org.jgrapht.io.StringComponentNameProvider;



public class Main {
	
	public static void main(String[] args) throws FileNotFoundException, IOException {
		//read input parameters
		if (args.length != 2) {
			System.err.println("Input: <type of model> <path_to_model>");
			return;
		}
		//inputs
		String modelType = args[0];
		String modelPath = args[1];
		//emf
		Resource.Factory.Registry.INSTANCE.getExtensionToFactoryMap().put("*", new XMIResourceFactoryImpl());
		//serialization
		IntegerComponentNameProvider<Node> p1=new IntegerComponentNameProvider<Node>();
		ComponentNameProvider<Node> p2 = new ComponentNameProvider<Node>() {
			@Override
			public String getName(Node arg0) {
				return arg0.object.eClass().getName();
			}
		};
		ComponentNameProvider<Edge> p3 = new ComponentNameProvider<Edge>() {
			@Override
			public String getName(Edge arg0) {
				return arg0.label;
			}
		};
		DOTExporter<Node, Edge> exporter = new DOTExporter(p1,p2,p3);
		Writer writer = new StringWriter();
		
		if (modelType.toLowerCase().equals("ecore")) {
			ResourceSet rs = new ResourceSetImpl();
			Resource resource = null;
			MetaFilterNames mfn = MetaFilterNames.getEcoreFilter();
			try {
				resource = rs.getResource(URI.createFileURI(modelPath), true);
			} catch (Exception e) {
				System.err.println("Error when reading the resource");
				return;
			}
			Graph<Node, Edge> g = getGraph(resource, mfn);
			
			//export
	        exporter.exportGraph(g, writer);
	        System.out.println(writer.toString());
			
		} else if (modelType.toLowerCase().equals("rds")) {
			//load metamodel of rds
			ResourceSet rs = new ResourceSetImpl();
			MetaFilterNames mfn = MetaFilterNames.getRDSFilter();
			String metamodelpath = "data/metamodels/rds_manual.ecore";
			Resource r = rs.createResource(URI.createURI(metamodelpath));
			r.load(new FileInputStream(metamodelpath), null);
			r.getAllContents().forEachRemaining(o -> {
				if (o instanceof EPackage) {
					EPackage pkg = (EPackage) o;
					EPackage.Registry.INSTANCE.put(pkg.getNsURI(), pkg);
				}
			});
			
			Resource resource = new XMIResourceImpl();
			resource.load(new FileInputStream(new File(modelPath)), null);
			Graph<Node, Edge> g = getGraph(resource, mfn);
			
			//export
	        exporter.exportGraph(g, writer);
	        System.out.println(writer.toString());
			
		} else if (modelType.toLowerCase().equals("yakindu")) {
			
		}
		
	}
	
	public static Graph<Node, Edge> getGraph(Resource r, IMetaFilter mf){
		
		Graph<Node, Edge> g = GraphTypeBuilder.<Node, Edge>directed().allowingMultipleEdges(true)
				.allowingSelfLoops(true).edgeClass(Edge.class).buildGraph();
		
		TreeIterator<EObject> it = r.getAllContents();
		ArrayList<EObject> allObjects = new ArrayList<EObject>();
		while (it.hasNext()) {
			EObject obj = it.next();
			if (!obj.eIsProxy()) {
				allObjects.add(obj);
			}
		}
		
		for (EObject obj : allObjects) {
			if (obj != null && mf.passFilterObject(obj)) {
				Node n1 = new Node(obj);
				g.addVertex(n1);
				
				for (EStructuralFeature f : obj.eClass().getEAllStructuralFeatures()) {
					if (f.isDerived())
						continue;
					// ignore the structural feature (attribute or reference)
					if (!mf.passFilerStructural(f))
						continue;
					
					if (f instanceof EReference && f.isMany()) {
						Collection<EObject> elements = (Collection<EObject>) obj.eGet(f);
						for (EObject e : elements) {
							// ignore the class
							if (e != null && !mf.passFilterObject(e))
								continue;
							if (e != null && e.eIsProxy())
								continue;
							if (!allObjects.contains(e))
								continue;

							if (e != null) {
								Node n2 = new Node(e);
								g.addVertex(n2);
								g.addEdge(n1, n2, new Edge(f.getName()));
							}
						}
						continue;
					}
					
					// take the reference
					if (f instanceof EReference && !f.isMany()) {
						EObject element = (EObject) obj.eGet(f);
						// ignore the class
						if (element != null &&!mf.passFilterObject(element))
							continue;
						if (element != null && element.eIsProxy())
							continue;
						if (!allObjects.contains(element))
							continue;
						if (element != null) {
							Node n2 = new Node(element);
							g.addVertex(n2);
							g.addEdge(n1, n2, new Edge(f.getName()));
							continue;
						}
					}
				}
				
			}
		}
		
		return g;
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
