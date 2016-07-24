// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef SEGINTERSECTION_H
#define SEGINTERSECTION_H

// Given the end points of two line segments, (a0, a1) and (b0, b1)
// which are known to be coplanar, compute whether or not the segments
// intersect.  If they do, set alpha to the parametric position of the
// intersection on A, and beta to the position on B.  That is, the
// intersection point X is

//   X = a0 + alpha*(a1 - a0) = b0 + beta*(b1 - b0)

// Dotting this equation with A=(a1-a0) and with B=(b1-b0) gives two
// equations which can be solved for alpha and beta.

// COORD can be a two or three dimensional coordinate.

#include "common/IO/oofcerr.h"

template <class COORD>
bool segIntersection(const COORD &a0, const COORD &a1,
		     const COORD &b0, const COORD &b1,
		     double &alpha, double &beta
#ifdef DEBUG
		     , bool verbose
#endif // DEBUG
		     )
{
#ifdef DEBUG
  if(verbose)
    oofcerr << "segIntersection: a0=" << a0 << " a1=" << a1
	    << " b0=" << b0 << " b1=" << b1 << std::endl;
#endif // DEBUG
  Coord A = a1 - a0;
  Coord B = b1 - b0;
  double A2 = norm2(A);
  double B2 = norm2(B);
  double AB = dot(A, B);

  double denom = A2*B2 - AB*AB;
#ifdef DEBUG
  if(verbose)
    oofcerr << "segIntersection: denom=" << denom << std::endl;
#endif // DEBUG
  
  if(denom == 0)
    return false;		// segments are parallel
#ifdef DEBUG
  if(verbose) {
    oofcerr << "segIntersection: B2*A=" << B2*A << " AB*B=" << AB*B
	    << " diff=" << B2*A-AB*B << std::endl;
    oofcerr << "segIntersection: b0-a0=" << b0-a0 << std::endl;
  }
#endif // DEBUG
  double invdenom = 1./denom;
  alpha = dot(B2*A - AB*B, b0 - a0)*invdenom;
  beta =  dot(A2*B - AB*A, a0 - b0)*invdenom;
#ifdef DEBUG
  if(verbose)
    oofcerr << "segIntersection: alpha=" << alpha << " beta=" << beta
	    << std::endl;
#endif // DEBUG

  return alpha >= 0.0 && alpha <= 1.0 && beta >= 0.0 && beta <= 1.0;
}

template <class COORD>
bool segIntersection(const COORD &a0, const COORD &a1,
		     const COORD &b0, const COORD &b1
#ifdef DEBUG
		     , bool verbose
#endif // DEBUG
		     )
{
  double alpha = 0.0;
  double beta = 0.0;
  return segIntersection(a0, a1, b0, b1, alpha, beta
#ifdef DEBUG
			 , verbose
#endif // DEBUG
			 );
}

#endif // SEGINTERSECTION_H

