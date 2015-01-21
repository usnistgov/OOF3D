// -*- C++ -*-
// $RCSfile: teststiffness.C,v $
// $Revision: 1.3.142.1 $
// $Author: langer $
// $Date: 2014/09/27 22:33:44 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

// create a simple mesh and print its stiffness matrix

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
#include "material.h"
#include "mesh.h"
#include "node.h"
#include "flux.h"
#include "field.h"
#include "equation.h"
#include "property/elasticity/aniso/aniso.h"
#include "property/elasticity/cijkl.h"
#include "property/orientation/orientation.h"
#include "stiffnessmatrix.h"
#include "common/trace.h"

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
    bool quad = false;		// element type
    int order = 1;

    int c;
    while((c = getopt(argc, argv, "34o:n:")) != -1) {
      switch(c) {
      case '4':
	quad = true;
	break;
      case '3':
	quad = false;
	break;
      case 'o':
	order = atoi(optarg);
	break;
      case 'n':
	meshsize = atoi(optarg);
	break;
      case '?':
	usage();
	exit(1);
      }
    }

    if(meshsize != 1 && meshsize != 3) {
      cerr << "meshsize must be 1 or 3!" << endl;
      exit(1);
    }

    //    Equation::initialize();
    TwoVectorField displacement("Displacement");
    SymmetricTensorFlux stress_flux("Stress");
    DivergenceEquation forcebalance_eqn("Force_Balance", stress_flux, spacedim);
    forcebalance_eqn.uses_flux(stress_flux);

    Cijkl cijkl;
    cijkl(0,0) = cijkl(1,1) = 1.0;
    cijkl(0,1) = 0.5;
    cijkl(5,5) = 0.25;
    AnisoElasticity *hexprop = new AnisoElasticity("hex", cijkl);	
// 					       1.0,	// c11	
// 					       0.5,	// c12	
// 					       0.0,	// c13	
// 					       0.0,	// c33	
// 					       0.0);	// c44	
    Orientation *orientation = new Orientation("unrotated", EulerAngle(0,0,0));
    Material mat("material");
    mat.addProperty(hexprop);
    mat.addProperty(orientation);
    mat.cross_reference();
#ifdef DEBUG
    Material::dump_all(cerr);
#endif

    mesh = new Mesh;

    if(order == 1) {
      // create nodes
      int nodecount = 0;
      for(int i=0; i<=meshsize; i++) {
	for(int j=0; j<=meshsize; j++) {
	  mesh->AddNode(new Node(nodecount++, Coord(j/(double)meshsize,
						    i/(double)meshsize)));
	}
      }
      // create elements
      if(quad == false) {
	// Linear triangular elements
	for(int i=0; i<meshsize; i++) {
	  for(int j=0; j<meshsize; j++) {
	    Node *ll = mesh->getNode(j + i*(meshsize+1));
	    Node *lr = mesh->getNode(j+1 + i*(meshsize+1));
	    Node *ul = mesh->getNode(j + (i+1)*(meshsize+1));
	    Node *ur = mesh->getNode(j+1 + (i+1)*(meshsize+1));
	    mesh->AddElement(new Tri3Element(&mat, ll, lr, ul));
	    mesh->AddElement(new Tri3Element(&mat, lr, ur, ul));
	  }
	}
      }
      else {			// quad == true
	// Linear quadrilateral elements
	for(int i=0; i<meshsize; i++) {
	  for(int j=0; j<meshsize; j++) {
	    Node *ll = mesh->getNode(j + i*(meshsize+1));
	    Node *lr = mesh->getNode(j+1 + i*(meshsize+1));
	    Node *ul = mesh->getNode(j + (i+1)*(meshsize+1));
	    Node *ur = mesh->getNode(j+1 + (i+1)*(meshsize+1));
	    mesh->AddElement(new Quad4Element(&mat, ll, lr, ur, ul));
	  }
	}
      }
    }
    else if(order == 2) {
      if(quad == false) {
	// Quadratic triangular elements
	int nodecount = 0;
	int npts = 2*meshsize + 1; // number of nodes in a row
	// create nodes
	for(int i=0; i<npts; i++) {
	  for(int j=0; j<npts; j++) {
	    mesh->AddNode(new Node(nodecount++, Coord(j/(2.*meshsize),
						      i/(2.*meshsize))));
	  }
	}
	// create elements
	for(int i=0; i<meshsize; i++) {
	  for(int j=0; j<meshsize; j++) {
	    // Nodes in a two-element square
	    //   ul um ur
	    //   *--*--*
	    //   |\    |
	    // ml*  *  * mr
	    //   |   \ |
	    //   *--*--*
	    //   ll lm lr
	    Node *ll = mesh->getNode(2*j   + 2*i*npts); // lower left
	    Node *lm = mesh->getNode(2*j+1 + 2*i*npts); // lower middle
	    Node *lr = mesh->getNode(2*j+2 + 2*i*npts); // lower right
	    Node *ml = mesh->getNode(2*j   + (2*i+1)*npts); // middle left
	    Node *mm = mesh->getNode(2*j+1 + (2*i+1)*npts);	// middle middle
	    Node *mr = mesh->getNode(2*j+2 + (2*i+1)*npts);	// middle right
	    Node *ul = mesh->getNode(2*j   + (2*i+2)*npts); // upper left
	    Node *um = mesh->getNode(2*j+1 + (2*i+2)*npts);	// upper middle
	    Node *ur = mesh->getNode(2*j+2 + (2*i+2)*npts);	// upper right
	    mesh->AddElement(new Tri6Element(&mat, ll, lm, lr, mm, ul, ml));
	    mesh->AddElement(new Tri6Element(&mat, lr, mr, ur, um, ul, mm));
	  }
	}
      }
      else {			// quad == true
	// Quadratic quadrilateral elements
	//   *--*--*
	//   |     |
	//   *     *
	//   |     |
	//   *--*--*
	int nodecount = 0;
	int npts = 2*meshsize + 1; // number of nodes in bottom and top rows
	int nmid = meshsize + 1; // number of points in the middle row
	// For each row of elements, create the bottom and middle rows of nodes
	for(int i=0; i<meshsize; i++) {
	  for(int j=0; j<npts; j++) { // bottom row
	    mesh->AddNode(new Node(nodecount++, Coord(j/(2.*meshsize),
						      i/(double) meshsize)));
	  }
	  for(int j=0; j<nmid; j++) { // middle row
	    mesh->AddNode(new Node(nodecount++, Coord(j/(double) meshsize,
						      (i+0.5)/ meshsize)));
	  }
	}
	// Create the nodes on the very top
	for(int j=0; j<npts; j++) {
	  mesh->AddNode(new Node(nodecount++, Coord(j/(2.*meshsize), 1.0)));
	}
	for(int i=0; i<meshsize; i++) {
	  int ll0 = i*(npts + nmid); // node number at ll of first el in row
	  int ml0 = ll0 + npts;	// number number at ml of first el in row
	  int ul0 = ml0 + nmid;
	  for(int j=0; j<meshsize; j++) {
	    Node *ll = mesh->getNode(ll0 + 2*j);
	    Node *lm = mesh->getNode(ll0 + 2*j + 1);
	    Node *lr = mesh->getNode(ll0 + 2*j + 2);
	    Node *ml = mesh->getNode(ml0 + j);
	    Node *mr = mesh->getNode(ml0 + j + 1);
	    Node *ul = mesh->getNode(ul0 + 2*j);
	    Node *um = mesh->getNode(ul0 + 2*j + 1);
	    Node *ur = mesh->getNode(ul0 + 2*j + 2);
	    mesh->AddElement(new Quad8Element(&mat,
					      ll, lm, lr, mr, ur, um, ul, ml));
	  }
	}
      }
    }
      
    forcebalance_eqn.activate();
    displacement.set_in_plane(true);
    displacement.define(mesh);
    displacement.activate();

    mesh->make_stiffness();

    const StiffnessMatrix &K = mesh->stiffness_matrix();
    cout << "K is " << K.nrows() << " x " << K.ncols() << endl;
    cout << K << endl;
  }
  catch(OOFerror::ProgrammingError &oops) {
    cout.flush();
    cerr << endl << "Oops!" << endl;
    cerr << oops.message() << endl;
    throw;
  }
  return 0;
}
