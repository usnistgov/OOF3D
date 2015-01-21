// -*- C++ -*-
// $RCSfile: testintgrl.C,v $
// $Revision: 1.2.142.1 $
// $Author: langer $
// $Date: 2014/09/27 22:33:41 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

// Test integration over tri3elements
// And superparametric 6 and 8 node elements.  

#include "common/config.h"
#include <iostream>
#include <string>
#include <vector>
using namespace std;

#define MAIN
#include "mesh.h"
#include "element/tri3.h"
#include "element/tri6.h"
#include "element/tri_6_3.h"
#include "node.h"
#include "common/ooferror.h"
#include "element/quad4.h"
#include "element/quad8.h"
#include "element/quad_8_4.h"
#include "masterelement.h"

int functionnumber = 0;

double f(const Coord &coord) {
  switch(functionnumber) {	// tri     quad (master)
  case 0:			// 1/2      4
    return 1;
  case 1:			// 1/6      0
    return coord(0);
  case 2:			// 1/6      0
    return coord(1);
  case 3:			// 1/12     4/3	
    return coord(0)*coord(0);
  case 4:			// 1/24=0.0416667     0
    return coord(0)*coord(1);
  case 5:			//  1/30  4/5
     return coord(1)*coord(1)*coord(1)*coord(1);
  case 6:			//  1/180=.00555...  4/9    
    return coord(0)*coord(0)*coord(1)*coord(1);
  default:
    cerr << "Bad function number!" << endl;
    exit(1);
  }
}

void test_integral(Element *el, int deg) {
  double intgrl = 0;
  int intgrlorder;
  for(GaussPoint g=el->integrator(deg); !g.end(); ++g) {
    intgrlorder = g.order();
    double ff = f(g.coord());
    double w = g.weight();
//      cout << "f" << g.coord() << "=" << ff << "  w=" << w
//  	 << " |J|=" << el->det_jacobian(g) << endl;
    intgrl += ff*w;
  }
  
  cout << "Integral (deg=" << deg << " order=" << intgrlorder<< ") is "
       << intgrl << endl;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class NoNode {};

Node *getnode(int index) {
  Coord x;
  cout << "Enter position of node " << index << ": ";
  cin >> x;
  if(!cin) throw NoNode();
  return new Node(index, x);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

int main(int argc, char *argv[]) {
  if(argc != 3) {
    cerr << "Usage: testintgrl <order> <functionnumber>" << endl;
    exit(1);
  }
  int order = atoi(argv[1]);
  functionnumber = atoi(argv[2]);

  if(order != 3 && order != 4 && order != 6 && order != 8) {
    cerr << "Order must be 3, 4 6, or 8!" << endl;
    exit(1);
  }
  try {
    while(1) {
      vector<Node*> nodes(order);
      cout << endl;
      for(int i=0; i<order; i++)
	nodes[i] = getnode(i);

      Element *el;
      if(order == 3)
	el = new Tri3Element(0, nodes[0], nodes[1], nodes[2]);
      else if(order == 4)
	el = new Quad4Element(0, nodes[0], nodes[1], nodes[2], nodes[3]);
      else if(order == 6)
	el = new Tri_6_3Element(0, nodes[0], nodes[1], nodes[2], nodes[3],
			     nodes[4], nodes[5]);
      else if(order == 8)
	el = new Quad_8_4Element(0, nodes[0], nodes[1], nodes[2], nodes[3],
			     nodes[4], nodes[5], nodes[6], nodes[7]);
	
      
      for(int deg=0; deg<10; deg++) {
	try {
	  test_integral(el, deg);
	}
	catch (OOFerror::BadOrder&) {
	  break; 
	}
      }

      if(order == 6 || order == 8) break;
    }
  }
  catch (OOFerror::ProgrammingError &exc) {
    cout.flush();
    cerr << endl << "Fatal Error!" << endl;
    cerr << exc.message() << endl;
    throw;			// will dump core
  }
  catch (NoNode &) {
    cerr << "bye" << endl;
  }
  return 0;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//
