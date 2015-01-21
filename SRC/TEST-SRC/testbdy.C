// -*- C++ -*-
// $RCSfile: testbdy.C,v $
// $Revision: 1.3.142.1 $
// $Author: langer $
// $Date: 2014/09/27 22:33:39 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

// Create a mesh, put some nodes into the boundary and make sure
// that the iterator does all the right things with it.
//   This is a copied-and-modified "teststiffness".  


#include <unistd.h>
#include <oofconfig.h>
#include <iostream>
#include <stdlib.h>
#define MAIN
#include "element.h"
#include "element/tri3.h"
#include "element/tri6.h"
#include "element/quad4.h"
#include "element/quad8.h"
#include "element/quad_8_4.h"
#include "element/tri_6_3.h"
#include "material.h"
#include "mesh.h"
#include "node.h"
#include "property/elasticity/aniso/aniso.h"
#include "property/elasticity/cijkl.h"
#include "property/orientation/orientation.h"
#include "stiffnessmatrix.h"
#include "common/trace.h"
#include "boundary.h"
#include "edge.h"


using namespace std;

void usage() {
  cerr << "Usage: teststiffness [-3|4][-o 1|2][-n meshsize]" << endl;
}

int main(int argc, char *argv[]) {
#ifdef DEBUG
  Trace_t::enable();
  Trace("main");
#endif // DEBUG
  try {

    extern char *optarg;
    int meshsize = 1;
    int quad=0;
    int param = 0;    // -1 for subpara, 0 for iso, 1 for super
    void sqmesh(Mesh *, int), enmesh(Mesh *, int, int);
    void trimesh(Mesh *, int), snmesh(Mesh *, int, int);

    int c;
    while((c = getopt(argc, argv, "qbpn:")) != -1) {
      switch(c) {

      case 'b':
	param--;
        break;

      case 'p':
	param++;  // Sub and super can both be specified, which adds up to iso.
	break;

      case 'q':
	quad=1;
	break;

      case 'n':
    	meshsize = atoi(optarg);
	break;
	      
      default:
	cout <<"Usage: testbdy [-b][-p][-n meshsize]" << endl;
        exit(4);
      }
    }

    Mesh *mesh = new Mesh;
    Boundary *bdy = new Boundary(meshsize); 

    // NB "meshsize" refers to the number of *elements* on each
    // side of the grid, not (necessarily) the number of nodes.
    if(quad==1) {
      switch(param) {
      case 0:
	// sqmesh puts the first n nodes/elements along the bottom.
	sqmesh(mesh, meshsize);
	
	for(int i=0; i<meshsize; i++) {
	  Element *el = mesh->getElement(meshsize-1-i); // works for bottom row.
	  Node *n1 = mesh->getNode(meshsize-1-i); 
	  Node *n2 = mesh->getNode(meshsize-i);
	  Edge *ed = el->getEdge(n1,n2);
	  bdy->addEdge(ed);
	} // Should be a fully populated boundary structure.
	break;
	
      case 1:
      case -1:
	enmesh(mesh, meshsize, param);
	
	for(int i=0; i<meshsize; i++) {
	  Element *el = mesh->getElement(i);
	  Node *n1 = mesh->getNode(2*i);
	  Node *n2 = mesh->getNode(2*(i+1));
	  Edge *ed = el->getEdge(n1,n2);
	  bdy->addEdge(ed);
	}
	break;
	
      }
    }
    else {  // quad not equal to 1, therefore triangular.
      switch(param) {
      case 0:
	trimesh(mesh,meshsize);
	
	for(int i=0; i<meshsize; i++) {
	  Element *el = mesh->getElement(2*i);
	  Node *n1 = mesh->getNode(i);
	  Node *n2 = mesh->getNode(i+1);
	  Edge *ed = el->getEdge(n1,n2);
	  bdy->addEdge(ed);
	}
	break;

      case 1:
      case -1:
	snmesh(mesh, meshsize, param);

	for(int i=0; i<meshsize; i++) {
	  Element *el = mesh->getElement(2*i);
	  Node *n1 = mesh->getNode(2*i);
	  Node *n2 = mesh->getNode(2*(i+1));
	  Edge *ed = el->getEdge(n1,n2);
	  bdy->addEdge(ed);
	}
	break;
      }
    }
    // Boundary node iterator should work in for-loops.
    for(BoundaryNodeIterator bdi = bdy->node_iterator(); !bdi.end(); ++bdi)
      cout << (bdi.node()).position() << endl;

  }
  catch(OOFerror::ProgrammingError &oops) {
    cout.flush();
    cerr << endl << "Oops!" << endl;
    cerr << oops.message() << endl;
    throw;
  }
  return 0;
}


     
void sqmesh(Mesh *m, int size) {
  int nodecount=0;

  for(int i=0; i<=size; i++)
    for(int j=0; j<=size; j++)
      m->AddNode(new Node(nodecount++,Coord(j,i)));
  
  for(int i=0; i<size; i++) {
    for(int j=0; j<size; j++) {
      Node *ll = m->getNode(j+i*(size+1));
      Node *lr = m->getNode(j+1 + i*(size+1));
      Node *ul = m->getNode(j + (i+1)*(size+1));
      Node *ur = m->getNode(j+1 + (i+1)*(size+1));
      m->AddElement(new Quad4Element(0,ll,lr,ur,ul));
    }
  }
  
}

// Builds the wacky mesh for eight-noded square elements.  Parameter
// p flags super vs. subpara, for creating the right nodes.
void enmesh(Mesh *m, int size, int p) {
  int nodecount=0;

  // Set up the point array.  
  for(int i=0; i<=2*size; i++)
    if(i%2==0)
      for(int j=0; j<=2*size; j++) 
	m->AddNode(new Node(nodecount++,Coord(j/2.0,i/2.0)));
    else
      for(int j=0; j<=size; j++)
	m->AddNode(new Node(nodecount++,Coord(j,i/2.0)));

  // Build the elements.  Code not stolen from teststiffness.
  for(int i=0; i<size; i++)
    for(int j=0; j<size; j++) {
      int startnode= 2*j+i*(3*size+2);
      Node *ll = m->getNode( startnode );
      Node *lm = m->getNode( startnode + 1 );
      Node *lr = m->getNode( startnode + 2 );
      Node *ml = m->getNode( startnode + (2*size-j) );
      Node *mr = m->getNode( startnode + (2*size-j) + 1 );
      Node *ul = m->getNode( startnode + (3*size+2) );
      Node *um = m->getNode( startnode + 1 + (3*size+2) );
      Node *ur = m->getNode( startnode + 2 + (3*size+2) );
  
      if(p==1)
	m->AddElement(new Quad_8_4Element(0, ll, lm, lr, mr, ur, um, ul, ml));
      else
	m->AddElement(new Quad8Element(0, ll, lm, lr, mr, ur, um, ul, ml));
    }
}



void trimesh(Mesh *m, int size) {
  int nodecount=0;

  for(int i=0; i<=size; i++)
    for(int j=0; j<=size; j++)
      m->AddNode(new Node(nodecount++,Coord(j,i)));
  
  for(int i=0; i<size; i++) {
    for(int j=0; j<size; j++) {
      Node *ll = m->getNode(j+i*(size+1));
      Node *lr = m->getNode(j+1 + i*(size+1));
      Node *ul = m->getNode(j + (i+1)*(size+1));
      Node *ur = m->getNode(j+1 + (i+1)*(size+1));
      m->AddElement(new Tri3Element(0,ll,lr,ul));
      m->AddElement(new Tri3Element(0,lr,ur,ul));
    }
  }
}


// Builds the rather less wacky mesh for six-noded square elements. 
// Again, parameter p  flags super vs. subpara, for creating the right nodes.
void snmesh(Mesh *m, int size, int p) {
  int nodecount=0;

  // Set up the point array.  
  for(int i=0; i<=2*size; i++)
      for(int j=0; j<=2*size; j++) 
	m->AddNode(new Node(nodecount++,Coord(j/2.0,i/2.0)));
    

  // Build the elements.  Code not stolen from teststiffness.
  for(int i=0; i<size; i++)
    for(int j=0; j<size; j++) {
      int startnode= 2*j+2*i*(2*size);
      Node *ll = m->getNode( startnode );
      Node *lm = m->getNode( startnode + 1 );
      Node *lr = m->getNode( startnode + 2 );
      Node *ml = m->getNode( startnode + (2*size+1));
      Node *mm = m->getNode( startnode + 1 + (2*size+1));
      Node *mr = m->getNode( startnode + 2 + (2*size+2));
      Node *ul = m->getNode( startnode + 2*(2*size+1));
      Node *um = m->getNode( startnode + 2*(2*size+1) + 1);
      Node *ur = m->getNode( startnode + 2*(2*size+1) + 2);
  
      if(p==1) {
	m->AddElement(new Tri_6_3Element(0, ll, lm, lr, mm, ul, ml));
	m->AddElement(new Tri_6_3Element(0, lr, mr, ur, um, ul, mm));
      }
      else {
	m->AddElement(new Tri6Element(0, ll, lm, lr, mm, ul, ml));
	m->AddElement(new Tri6Element(0, lr, mr, ur, um, ul, mm));
      }
    }
}
