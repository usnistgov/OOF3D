// -*- C++ -*-
// $RCSfile: bdyanalysis.C,v $
// $Revision: 1.5.4.4 $
// $Author: langer $
// $Date: 2014/03/24 21:09:22 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "common/cleverptr.h"
#include "common/vectormath.h"
#include "engine/edgeset.h"
#include "engine/element.h"
#include "engine/femesh.h"
#include "engine/field.h"
#include "engine/flux.h"
#include "engine/gausspoint.h"
#include "engine/outputval.h"

// Helper function for integrating the flux through a boundary. 

// // OLD 2D version
// OutputValue integrateFlux(const FEMesh *mesh, const Flux *flux,
// 			  const EdgeSet *es)
// {
//   OutputVal *resultptr = 0;
//   for(EdgeSetIterator esi=EdgeSetIterator(es); !esi.end(); ++esi) {
//     BoundaryEdge *bdy_edge = esi.edge();
//     const Element *el = bdy_edge->el;
//     int order = el->shapefun_degree();
//     for(EdgeGaussPoint egpt=bdy_edge->integrator(order); !egpt.end(); ++egpt) {
//       if(!resultptr) {
// 	resultptr = flux->contract(mesh, el, egpt);
// 	*resultptr *= egpt.weight();
//       }
//       else {
// 	OutputVal *r = flux->contract(mesh, el, egpt);
// 	*r *= egpt.weight();
// 	*resultptr += *r;
// 	delete r;
//       }
//     }
//   }
//   return OutputValue(resultptr);
// }

OutputValue integrateFlux(const FEMesh *mesh, const Flux *flux, 
			  const SubDimensionalSet *s)
{
  // s is either an EdgeSet or a FaceSet.
  OutputVal *resultptr = 0;
  for(CleverPtr<SubDimensionalIterator> si(s->iterator()); !si->end();
      ++*si) 
    {
      Element *el = si->part();
      int order = el->shapefun_degree();
      for(GaussPointIterator gpi=el->integrator(order); !gpi.end(); ++gpi) {
	GaussPoint gpt = gpi.gausspoint();
	if(!resultptr) {
	  resultptr = flux->contract(mesh, el, gpt);
	  *resultptr *= gpt.weight();
	}
	else {
	  OutputVal *r = flux->contract(mesh, el, gpt);
	  *r *= gpt.weight();
	  *resultptr += *r;
	  delete r;
	}
      }
    }
  return OutputValue(resultptr);
}

OutputValue averageField(const FEMesh *m, const Field *field,
			 const SubDimensionalSet *es)
{
  OutputValue result(field->newOutputValue());
  double weight = 0.0;
  // for(EdgeSetIterator esi=EdgeSetIterator(es); !esi.end(); ++esi) {
  for(CleverPtr<SubDimensionalIterator> i(es->iterator()); !i->end(); ++(*i)) {
    Element *el = i->part();
    int order = el->shapefun_degree();

    for(GaussPointIterator egpt=el->integrator(order); !egpt.end(); ++egpt) {
      GaussPoint gpt = egpt.gausspoint();
      double w = gpt.weight();
      result += el->outputField(m, *field, gpt.mastercoord())*w;
      weight += w;
    }
  }
  return result/weight;
}
