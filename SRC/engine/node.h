// -*- C++ -*-
// $RCSfile: node.h,v $
// $Revision: 1.25.6.9 $
// $Author: langer $
// $Date: 2014/09/17 17:48:00 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

class Node;

#ifndef NODE_H
#define NODE_H

#include "common/coord.h"
#include "engine/equation.h"
#include "engine/field.h"
#include "engine/fieldeqnlist.h"
#include "engine/freedom.h"
#include "engine/pointdata.h"
#include "common/pythonexportable.h"
#include <vector>
#include <iostream>

class FEMesh;
class GridSource;
class NodalEquation;
class ElementMapNodeIterator;
class SimpleCellLayer;

#include <vtkSmartPointer.h>

class Node : public PythonExportable<Node>, public Position {
private:
  static const std::string classname_;
  static const std::string modulename_;
protected:
  Node(int n, const Coord &p);	// only called by FEMesh::newMapNode()
  Node(const Node&);		// prohibited
  Node &operator=(const Node&);	// prohibited

  Coord pos;
  int index_;	// unique for this Node. TODO 3.1: should be changed to
		// uid to be consistent with skeleton

public:
  int index() const { return index_; }
  
  virtual ~Node() {}
  virtual const std::string &classname() const { return classname_; }
  virtual const std::string &modulename() const { return modulename_; }
  // You'd think that position() should return a const Coord&, but
  // you'd be wrong.  GaussPoint and Node are both derived from
  // Position, and GuassPoint::position() has to compute its result,
  // and can't return reference to it.
  virtual Coord position() const { return pos; } // get original position
  virtual Coord displaced_position(const FEMesh*, double) const { return pos; }

  void drawGridCell(vtkSmartPointer<GridSource>, SimpleCellLayer*) const;

  friend bool operator==(const Node&, const Node&);
  friend bool operator!=(const Node &n0, const Node &n1) { return !(n0==n1); }

  friend std::ostream& operator<<(std::ostream&, const Node&);
  friend class FEMesh;

  virtual std::vector<std::string> *fieldNames() const;
};

// Node at which function parameters (degrees of freedom, nodal
// equations) are defined

class FuncNode : public Node, public PointData {
private:
  static const std::string classname_;
#ifdef HAVE_MPI
  // This may be generalized to include other flags
  //  that require only a bit of storage
  bool _bshare;
#endif
protected:
  FuncNode(FEMesh*, int n, const Coord &p);
                  // only called by FEMesh::newFuncNode()
public:
  virtual ~FuncNode() {}
  virtual const std::string &classname() const { return classname_; }
  // Used by the regression tests to check solutions.
  virtual Coord displaced_position(const FEMesh*, double enhancement=1.0) const;
  virtual Coord position() const { return Node::position(); }

  friend class FEMesh;
  
  virtual std::vector<std::string> *fieldNames() const;
};				// FuncNode

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


#endif	// NODE_H
