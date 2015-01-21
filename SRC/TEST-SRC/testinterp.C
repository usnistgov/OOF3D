// -*- C++ -*-
// $RCSfile: testinterp.C,v $
// $Revision: 1.3.142.1 $
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


// Test (my understanding of) interpolation, starting with the 
// shape of the real-space interpolating functions.
// Input is all the nodes, then a real-space coordinate, at
// which is output the values of each of the parnode shape
// functions at that point in real space.

#include <oofconfig.h>
#include <iostream>
using namespace std;

#define MAIN
#include "mesh.h"
#include "element/tri3.h"
#include "element/tri6.h"
#include "node.h"
#include "common/ooferror.h"
#include "element/quad4.h"
#include "element/quad8.h"
#include "element/tri_6_3.h"
#include "element/quad_8_4.h"

class NoNode {};

Node *getnode(int index) {
  Coord x;
  cout << "Enter position of node " << index << ": ";
  cin >> x;
  if(!cin) throw NoNode();
  return new Node(index, x);
}

int main(int argc, char *argv[]) {
  if(argc != 2) {
    cerr << "Usage: testinterp <order>" << endl;
    exit(1);
  }
  int order = atoi(argv[1]);
  if(order != 3 && order != 4 && order != 6 && order != 8) {
    cerr << "Order must be 3, 4, 6 or 8!" << endl;
    exit(1);
  }
  try {
    while(1) {
      vector<Node*> nodes(order);
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
      
      cout << "Area = " << el->area() << endl;

      do {
	cout << "Enter a master coordinate: ";
	MasterCoord mc;
	cin >> mc;
       	if(cin) {
          cout << "  Real coord: " << el->from_master(mc) << endl;
          for(ElementNodeIterator ni=el->parnode_iterator(); 
                  !ni.end(); ++ni) {
            cout << "  Shape function " << ni.sf_index() << " = "
                 << el->shapefun(ni,mc) << endl;
          }
	}
      } while(cin);		// get next master coordinate
      cin.clear();
      
      do {
	cout << "Enter a real space coordinate: ";
	Coord coord;
	cin >> coord;
	if(cin) {
          for(ElementNodeIterator ni=el->parnode_iterator();
	      !ni.end(); ++ni) {
            cout << "  Shape function " << ni.sf_index() << " = "
                 << el->shapefun(ni,coord) << endl;
          }
        }

      } while(cin);
      cin.clear();
      // get next set of nodes
      }
    return 0;
    }
  catch (OOFerror::ProgrammingError &exc) {
    cout.flush();
    cerr << endl << "Fatal Error!" << endl;
    cerr << exc.message() << endl;
    throw;			// will dump core
  }
  catch (NoNode &) {
    cerr << "Good-bye!" << endl;
  }
  return 0;
  }
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

#undef MAIN






