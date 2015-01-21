// -*- C++ -*-
// $RCSfile: shapefunction.C,v $
// $Revision: 1.13.10.7 $
// $Author: langer $
// $Date: 2014/12/14 22:49:21 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>
#include "common/coord.h"
#include "common/doublevec.h"
#include "common/tostring.h"
#include "common/trace.h"
#include "engine/element.h"
#include "engine/masterelement.h"
#include "engine/shapefunction.h"
#include "engine/shapefunctioncache.h"

#if DIM==3
#include <vtkMath.h>
#endif 

class ShapeFunctionTable {
  // Stores values of shape function and its derivatives at a set of
  // Gauss points.
private:
  ShapeFunctionTable(int ngauss, int nnodes);
  // f[i][j] = f(gausspoint i, node j)
  std::vector<DoubleVec> f_table;
  // df[i][j][k] = df(gausspoint i, node j)/dx_k
  std::vector<std::vector<DoubleVec> > df_table;
  friend class ShapeFunction;
};

ShapeFunctionTable::ShapeFunctionTable(int ngauss, int nsf)
  : f_table(ngauss, DoubleVec(nsf)),
    df_table(ngauss, std::vector<DoubleVec>(nsf, DoubleVec(DIM)))
{
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

ShapeFunction::ShapeFunction(int nsf, const MasterElement &master)
  : sftable(master.ngauss_sets()),
    sfcache(master.ngauss_sets()),
    nfunctions(nsf)
{
  for(int i=0; i<master.ngauss_sets(); i++) {
    sftable[i] = new ShapeFunctionTable(master.ngauss(i), nsf);
    sfcache[i] = new ShapeFunctionCache(master.ngauss(i), nsf);
  }
}

ShapeFunction::~ShapeFunction() {
  for(std::vector<ShapeFunctionTable*>::size_type i=0; i<sftable.size(); i++)
    delete sftable[i]; 
  for(std::vector<ShapeFunctionCache*>::size_type i=0; i<sfcache.size(); i++)
    delete sfcache[i];

}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Use double dispatch to evaluate shape functions at Positions, since
// the evaluation is done differently at GaussPoints and MasterCoords

double ShapeFunction::value(ShapeFunctionIndex n, const MasterPosition &p)
  const
{
  //  Trace("ShapeFunction::value p=" + to_string(p.mastercoord()));
  return p.shapefunction(*this, n);
}

double ShapeFunction::masterderiv(ShapeFunctionIndex n, SpaceIndex j,
				  const MasterPosition &p)
  const
{
  //  Trace("ShapeFunction::masterderiv sf=" + to_string(n) + " p=" + to_string(p.mastercoord()));
  return p.mdshapefunction(*this, n, j);
}

double ShapeFunction::realderiv(const ElementBase *el, ShapeFunctionIndex n,
				SpaceIndex j, const MasterPosition &p)
  const
{
  //  Trace("ShapeFunction::realderiv sf=" + to_string(n) + " p=" + to_string(p.mastercoord()));
  return p.dshapefunction(el, *this, n, j);
}

// Find the value and derivative at Gauss points by using the lookup tables.

double ShapeFunction::value(ShapeFunctionIndex n, const GaussPoint &g)
  const
{
  return sftable[g.order()]->f_table[g.index()][n];
}

// derivative wrt master coordinates
double ShapeFunction::masterderiv(ShapeFunctionIndex n, SpaceIndex j,
			    const GaussPoint &g) const
{
  //  Trace("ShapeFunction::masterderiv sf=" + to_string(n) + " gpt=" + to_string(g.mastercoord()));
  return sftable[g.order()]->df_table[g.index()][n][j];
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Fill in the lookup tables

void ShapeFunction::precompute(const MasterElement &master) {
  // Use the virtual functions that evaluate the shapefunction at
  // arbitrary points to store its values at the Gauss points.

  // loop over integration orders (sets of gauss points)
  for(int ord=0; ord<master.ngauss_sets(); ord++) {

    const GaussPtTable &gptable = master.gptable(ord);

    sftable[ord] = new ShapeFunctionTable(gptable.size(), nfunctions);
    std::vector<DoubleVec> &f_table = sftable[ord]->f_table;
    std::vector<std::vector<DoubleVec> > &df_table =
      sftable[ord]->df_table;

    // loop over gausspoints
    for(std::vector<GaussPtData>::size_type g=0; g<gptable.size(); g++) {
      MasterCoord mpos = gptable[g].position;
      for(ShapeFunctionIndex n=0; n<nfunctions; ++n) { // loop over sf's
	f_table[g][n] = value(n, mpos);
	DoubleVec &dftemp = df_table[g][n];
	for(SpaceIndex j=0; j<DIM; ++j) // loop over spatial dimensions
	  dftemp[j] = masterderiv(n, j, mpos);
      }
    }
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

double ShapeFunction::realderiv(const ElementBase *el,
				ShapeFunctionIndex n, SpaceIndex i,
				const GaussPoint &g) const
{
  //  Trace("ShapeFunction::realderiv 1");
  double result = 0;
 
  if(sfcache[g.order()]->query_dsf(el, n, i, g, result))
    return result;

  // don't be tempted to rewrite this in terms of
  // realderiv(ElementBase*, ..., MasterCoord&) because that one
  // doesn't use the precomputed values of the shape function
  // derivatives!
  for(SpaceIndex j=0; j<DIM; ++j)
    result += el->Jdmasterdx(j, i, g)*masterderiv(n, j, g);
  result /= el->det_jacobian(g);

  sfcache[g.order()]->store_dsf(el, n, i, g, result);
  return result;
}

double ShapeFunction::realderiv(const ElementBase *el,
				ShapeFunctionIndex n, SpaceIndex i,
				const MasterCoord &mc) const
{
  //  Trace("ShapeFunction::realderiv 2");
  double result = 0;
  for(SpaceIndex j=0; j<DIM; ++j)
    result += el->Jdmasterdx(j, i, mc)*masterderiv(n, j, mc);
  result /= el->det_jacobian(mc);
  return result;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Routines that compute the determinant of the Jacobian for various
// dimensions of master and physical space.  By "determinant of the
// Jacobian" we really mean the factor that relates length, area, or
// volume in real space to a product of differentials (dx, dxdy,
// dxdydz) in master space.

// There are two versions of each routine, one for GaussPoints and one
// for MasterCoords.  Don't be tempted to rewrite the GaussPoint
// version in terms of the MasterCoord version, because the
// MasterCoord version doesn't use the precomputed values of the shape
// function derivatives!

// One dimensional element.
double ShapeFunction::det_jacobian1(const ElementBase *el,
				    const GaussPoint &g)
  const
{
  // dL = norm(dr/dx) where r is a 2D real space vector and x is the
  // master space coordinate.
#if DIM==2
  Coord drdx(el->jacobian(0,0,g), el->jacobian(1,0,g));
#elif DIM==3
  Coord drdx(el->jacobian(0,0,g), el->jacobian(1,0,g), el->jacobian(2,0,g));
#endif // DIM==3
  return sqrt(norm2(drdx));
}

double ShapeFunction::det_jacobian1(const ElementBase *el, 
				    const MasterCoord &mc)
  const
{
  // dL = norm(dr/dx) where r is a 2D real space vector and x is the
  // master space coordinate.
#if DIM==2
  Coord drdx(el->jacobian(0,0,mc), el->jacobian(1,0,mc));
#elif DIM==3
  Coord drdx(el->jacobian(0,0,mc), el->jacobian(1,0,mc), el->jacobian(2,0,mc));
#endif // DIM==3
  return sqrt(norm2(drdx));
}

// Two dimensional element.
double ShapeFunction::det_jacobian2(const ElementBase *el, 
				    const GaussPoint &g) 
  const
{
#if DIM==2
  // 2D element in 2D
  return (el->jacobian(0, 0, g) * el->jacobian(1, 1, g) -
	  el->jacobian(0, 1, g) * el->jacobian(1, 0, g));
#elif DIM==3
  // 2D element is embedded in 3D. The differential area is the norm
  // of dr/dx cross dr/dy, where r is the real space position and has
  // *3* components.
  Coord drdx(el->jacobian(0, 0, g), 
	     el->jacobian(1, 0, g),
	     el->jacobian(2, 0, g));
  Coord drdy(el->jacobian(0, 1, g), 
	     el->jacobian(1, 1, g),
	     el->jacobian(2, 1, g));
  return sqrt(norm2(cross(drdx, drdy)));
#endif // DIM==3
}

double ShapeFunction::det_jacobian2(const ElementBase *el,
				    const MasterCoord &mc) 
  const
{
#if DIM==2
  // 2D element in 2D
  return (el->jacobian(0, 0, g) * el->jacobian(1, 1, mc) -
	  el->jacobian(0, 1, g) * el->jacobian(1, 0, mc));
#elif DIM==3
  Coord drdx(el->jacobian(0, 0, mc), 
	     el->jacobian(1, 0, mc),
	     el->jacobian(2, 0, mc));
  Coord drdy(el->jacobian(0, 1, mc), 
	     el->jacobian(1, 1, mc),
	     el->jacobian(2, 1, mc));
  return sqrt(norm2(cross(drdx, drdy)));
#endif // DIM==3
}

#if DIM==3
double ShapeFunction::det_jacobian3(const ElementBase *el, const GaussPoint &g)
  const
{
  // 3D element in 3D.  Typing out a closed form in code is messy.
  double m[DIM][DIM]; 
  int ii, jj;
  for(ii=0; ii<DIM; ++ii) {
    for(jj=0; jj<DIM; ++jj) {
      m[ii][jj] = el->jacobian(ii,jj,g);
    }
  }
  return vtkMath::Determinant3x3(m);
}

double ShapeFunction::det_jacobian3(const ElementBase *el,
				    const MasterCoord &mc)
  const
{
  double m[DIM][DIM]; 
  int ii, jj;
  for(ii=0; ii<DIM; ++ii) {
    for(jj=0; jj<DIM; ++jj) {
      m[ii][jj] = el->jacobian(ii,jj,mc);
    }
  }
  return vtkMath::Determinant3x3(m);
}
#endif // DIM==3

double ShapeFunction::det_jacobian(const ElementBase *el, const GaussPoint &g)
  const
{
  double result = 0;
  if(sfcache[g.order()]->query_jac(el, g, result))
    return result;

  switch(el->masterelement().dimension()) {
  case 1:
    result = det_jacobian1(el, g);
    break;
  case 2:
    result = det_jacobian2(el, g);
    break;
#if DIM==3
  case 3:
    result = det_jacobian3(el, g);
    break;
#endif // DIM==3
  }

  sfcache[g.order()]->store_jac(el, g, result);
  return result;
}

double ShapeFunction::det_jacobian(const ElementBase *el, const MasterCoord &mc)
  const
{
  double result = 0;
  switch(el->masterelement().dimension()) {
  case 1:
    result = det_jacobian1(el, mc);
    break;
  case 2:
    result = det_jacobian2(el, mc);
    break;
#if DIM==3
  case 3:
    result = det_jacobian3(el, mc);
    break;
#endif // DIM==3
  }
  return result;
}
