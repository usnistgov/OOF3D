// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef BARYCENTRIC_H
#define BARYCENTRIC_H

#include <oofconfig.h>
#include "common/coord.h"
#include <vector>

class PixelPlane;

class BarycentricCoord {
private:
  std::vector<double> bcoord;
public:
  BarycentricCoord() : bcoord(4, 0.0) {}
  BarycentricCoord(const Coord3D&, const std::vector<Coord3D>&);
  BarycentricCoord(double b0, double b1, double b2, double b3);
  BarycentricCoord(const BarycentricCoord&);
  BarycentricCoord(BarycentricCoord&&);
  BarycentricCoord &operator=(const BarycentricCoord&);
  bool interior(unsigned int) const;
  bool interior() const;
  double operator[](unsigned int i) const { return bcoord[i]; }
  double &operator[](unsigned int i) { return bcoord[i]; }
  Coord3D position3D(const std::vector<Coord3D> &epts) const;
  void repair();
  bool onEdge() const;
  bool operator<(const BarycentricCoord&) const;
  bool operator==(const BarycentricCoord&) const;
};


// BarycentricCoord &getBarycentricCoord(
// 	      const Coord3D&, const std::vector<Coord3D>&,
// 	      const std::vector<const PixelPlane*>&, BaryCoordCache&);
// BarycentricCoord &getBarycentricCoord(
// 	      const ICoord3D&, const std::vector<Coord3D>&,
// 	      const std::vector<const PixelPlane*>&, BaryCoordCache&);
// BarycentricCoord &getBarycentricCoord(
// 	      const ICoord2D&, const PixelPlane&, const std::vector<Coord3D>&,
// 	      const std::vector<const PixelPlane*>&, BaryCoordCache&);

const BarycentricCoord &nodeBCoord(unsigned int);


BarycentricCoord averageBary(const BarycentricCoord&, const BarycentricCoord&,
			     double weight=0.5);

// BarycentricCoord mergeBary(const BarycentricCoord&, const BarycentricCoord&);

std::ostream &operator<<(std::ostream&, const BarycentricCoord&);

#endif // BARYCENTRIC_H
