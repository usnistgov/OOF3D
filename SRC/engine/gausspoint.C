// -*- C++ -*-
// $RCSfile: gausspoint.C,v $
// $Revision: 1.18.10.6 $
// $Author: fyc $
// $Date: 2014/07/24 21:36:26 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "common/IO/oofcerr.h"
#include "engine/edge.h"
#include "engine/element.h"
#include "engine/gausspoint.h"
#include "engine/masterelement.h"
#include <math.h>
#include <string>
#include <vector>

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

GaussPoint::GaussPoint(const ElementBase *el,
		       MasterCoord pos, double wgt, int currpt, int order)
  : element(el),
    weight_(wgt),
    position_(pos),
    index_(currpt),
    order_(order)
{}

double GaussPoint::weight() const {
  return weight_ * (element->det_jacobian(*this)); 
}

// Redundant with the iterator's index, but needed so the cache can
// identify already-found gausspoints.
int GaussPoint::index() const {
  return index_; 
}

MasterCoord GaussPoint::mastercoord() const {
  return position_;
}

Coord GaussPoint::coord() const {
  return element->from_master(mastercoord());
}

#ifndef DONT_USE_CACHED_VALUES

double GaussPoint::shapefunction(const ShapeFunction &sf, ShapeFunctionIndex n)
  const
{
  return sf.value(n, *this);
}

double GaussPoint::mdshapefunction(const ShapeFunction &sf,
				  ShapeFunctionIndex n, SpaceIndex i)
  const
{
  return sf.masterderiv(n, i, *this);
}

double GaussPoint::dshapefunction(const ElementBase *el,
				  const ShapeFunction &sf,
				  ShapeFunctionIndex n, SpaceIndex i)
  const
{
  return sf.realderiv(el, n, i, *this);
}

#else  // DONT_USE_CACHED_VALUES

double GaussPoint::shapefunction(const ShapeFunction &sf, ShapeFunctionIndex n)
  const
{
  return sf.value(n, mastercoord());
}

double GaussPoint::mdshapefunction(const ShapeFunction &sf,
				  ShapeFunctionIndex n, SpaceIndex i)
  const
{
  return sf.masterderiv(n, i, mastercoord());
}

double GaussPoint::dshapefunction(const ElementBase *el,
				  const ShapeFunction &sf,
				  ShapeFunctionIndex n, SpaceIndex i)
  const
{
  return sf.realderiv(el, n, i, mastercoord());
}

#endif // DONT_USE_CACHED_VALUES

std::ostream& operator<<(std::ostream &o, const GaussPoint &gpt) {
  o << "GaussPoint(" << gpt.position_[0] << ", " <<  
    gpt.position_[1] <<  
#if DIM==3
    ", " << gpt.position_[2] << 
#endif
    ", weight=" << gpt.weight_ << ")";
  return o;
}

std::ostream &GaussPoint::print(std::ostream &os) const {
  os << *this;
  return os;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

GaussPointIterator::GaussPointIterator(const ElementBase *el, int order)
  : element(el),
    gptable(el->masterelement().gausspointtable(order)),
    currentpt(0) 
{}

void GaussPointIterator::operator++() {
  if(!end())
    ++currentpt;
}

bool GaussPointIterator::end() const {
  return currentpt == gptable.size();
}

GaussPoint GaussPointIterator::gausspoint() const {
  return GaussPoint(element, gptable[currentpt].position,
		    gptable[currentpt].weight, currentpt, order() );
}

GaussPoint *GaussPointIterator::gausspointptr() const {
  return new GaussPoint(element, gptable[currentpt].position,
			gptable[currentpt].weight, currentpt, order() );
}


int GaussPointIterator::index() const {
  return currentpt;
}

int GaussPointIterator::order() const {
  return gptable.order();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

GaussPtTable::GaussPtTable(int ordr, int npts)
  : order_(ordr)
{
  assert(npts > 0);
  gpdata.reserve(npts);
}

GaussPtTable::GaussPtTable(const GaussPtTable &other) 
  : order_(other.order()),
    gpdata(other.gpdata)
{
  gpdata.reserve(other.gpdata.capacity());
}

void GaussPtTable::addpoint(const MasterCoord &p, double w) {
  assert(size() < gpdata.capacity());
  gpdata.push_back(GaussPtData(p, w));
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

static std::vector<GaussPtTable1> &one_d_gauss_pts();

GaussPoint1::GaussPoint1(int order, double xmin, double xmax)
  : gptable(one_d_gauss_pts()[order]),
    currentpt(0),
    min(xmin),
    max(xmax)
{}

void GaussPoint1::operator++() {
  if(!end())
    ++currentpt;
}

bool GaussPoint1::end() const {
  return currentpt == gptable.size();
}

double GaussPoint1::weight() const {
  return gptable[currentpt].weight
    * (max - min)/(GaussPoint1::Mmax - GaussPoint1::Mmin);
}

double GaussPoint1::position() const {
  return min
    + (gptable[currentpt].position - GaussPoint1::Mmin)*(max - min)/
    (GaussPoint1::Mmax - GaussPoint1::Mmin);
}

double GaussPoint1::mposition() const {
  return gptable[currentpt].position;
}

int GaussPoint1::order() const {
  return gptable.order();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

GaussPtTable1::GaussPtTable1(int ordr, int npts)
  : order_(ordr)
{
  assert(npts > 0);
  gpdata.reserve(npts);
}

GaussPtTable1::GaussPtTable1(const GaussPtTable1 &other)
  : order_(other.order()),
    gpdata(other.gpdata)
{
  gpdata.reserve(other.gpdata.capacity());
}

GaussPtTable1::~GaussPtTable1() {}

void GaussPtTable1::addpoint(double x, double w) {
  assert(size() < gpdata.capacity());
  gpdata.push_back(GaussPtData1(x, w));
}

// The 1-D gauss points are defined for integration over the range (-1, 1).

// Gaussian integration of order N exactly integrates polynomials of
// order 2N-1.

double GaussPoint1::Mmin = -1;
double GaussPoint1::Mmax =  1;

static std::vector<GaussPtTable1> &one_d_gauss_pts() {
  static std::vector<GaussPtTable1> table;
  static int set = false;
  if(!set) {
    set = true;
    table.push_back(GaussPtTable1(0,1)); // order = 0, npts = 1
    table[0].addpoint(0., 2.);

    table.push_back(GaussPtTable1(1,1)); // order = 1, npts = 1
    table[1].addpoint(0., 2.);

    table.push_back(GaussPtTable1(2, 2)); // order = 2, npts = 2
    table[2].addpoint(-1./sqrt(3.), 1.0);
    table[2].addpoint( 1./sqrt(3.), 1.0);

    table.push_back(GaussPtTable1(3, 3)); // order = 3, npts = 3
    table[3].addpoint(-sqrt(3./5.), 5./9.);
    table[3].addpoint(0, 8./9.);
    table[3].addpoint( sqrt(3./5.), 5./9.);

    // Below here, the code was computed by AUX/findgauss

    table.push_back(GaussPtTable1(4, 4)); // order = 4, npts = 4
    table[4].addpoint(-0.8611363115940525, 0.3478548451374537);
    table[4].addpoint(-0.3399810435848563, 0.652145154862546);
    table[4].addpoint(0.3399810435848563, 0.652145154862546);
    table[4].addpoint(0.8611363115940525, 0.3478548451374537);

    table.push_back(GaussPtTable1(5, 5)); 
    table[5].addpoint( -0.9061798459386639, 0.236926885056189);
    table[5].addpoint( -0.5384693101056831, 0.4786286704993664);
    table[5].addpoint(                   0, 0.5688888888888888);
    table[5].addpoint(  0.5384693101056831, 0.4786286704993664);
    table[5].addpoint(  0.9061798459386639, 0.236926885056189);

    table.push_back(GaussPtTable1(6, 6));
    table[6].addpoint(    -0.9324695142031, 0.1713244923791);
    table[6].addpoint(    -0.6612093864662, 0.3607615730481);
    table[6].addpoint(    -0.2386191860832, 0.4679139345726);
    table[6].addpoint(     0.2386191860832, 0.4679139345726);
    table[6].addpoint(     0.6612093864662, 0.3607615730481);
    table[6].addpoint(     0.9324695142031, 0.1713244923791);

#ifdef HIGH_ORDERS
    table.push_back(GaussPtTable1(7, 7));
    table[7].addpoint(    -0.9491079123427, 0.1294849661688);
    table[7].addpoint(    -0.7415311855993, 0.2797053914892);
    table[7].addpoint(    -0.4058451513774, 0.381830050505);
    table[7].addpoint(                   0, 0.4179591836734);
    table[7].addpoint(     0.4058451513774, 0.381830050505);
    table[7].addpoint(     0.7415311855993, 0.2797053914892);
    table[7].addpoint(     0.9491079123427, 0.1294849661688);

    table.push_back(GaussPtTable1(8, 8));
    table[8].addpoint(    -0.9602898564975, 0.1012285362903);
    table[8].addpoint(    -0.7966664774136, 0.2223810344533);
    table[8].addpoint(    -0.5255324099163, 0.3137066458776);
    table[8].addpoint(    -0.1834346424956, 0.3626837833783);
    table[8].addpoint(     0.1834346424956, 0.3626837833783);
    table[8].addpoint(     0.5255324099163, 0.3137066458776);
    table[8].addpoint(     0.7966664774136, 0.2223810344533);
    table[8].addpoint(     0.9602898564975, 0.1012285362903);

    table.push_back(GaussPtTable1(9, 9));
    table[9].addpoint(    -0.9681602395076, 0.08127438836156);
    table[9].addpoint(    -0.8360311073266, 0.1806481606948);
    table[9].addpoint(    -0.6133714327005, 0.2606106964029);
    table[9].addpoint(    -0.3242534234038, 0.31234707704);
    table[9].addpoint(                   0, 0.3302393550012);
    table[9].addpoint(     0.3242534234038, 0.31234707704);
    table[9].addpoint(     0.6133714327005, 0.2606106964029);
    table[9].addpoint(     0.8360311073266, 0.1806481606948);
    table[9].addpoint(     0.9681602395076, 0.08127438836156);

    table.push_back(GaussPtTable1(10, 10));
    table[10].addpoint(    -0.9739065285171, 0.06667134430868);
    table[10].addpoint(    -0.8650633666889, 0.1494513491505);
    table[10].addpoint(     -0.679409568299, 0.2190863625159);
    table[10].addpoint(    -0.4333953941292, 0.2692667193099);
    table[10].addpoint(    -0.1488743389816, 0.2955242247147);
    table[10].addpoint(     0.1488743389816, 0.2955242247147);
    table[10].addpoint(     0.4333953941292, 0.2692667193099);
    table[10].addpoint(      0.679409568299, 0.2190863625159);
    table[10].addpoint(     0.8650633666889, 0.1494513491505);
    table[10].addpoint(     0.9739065285171, 0.06667134430868);

    table.push_back(GaussPtTable1(11, 11));
    table[11].addpoint(     -0.978228658146, 0.05566856711617);
    table[11].addpoint(    -0.8870625997681, 0.1255803694649);
    table[11].addpoint(     -0.730152005574, 0.1862902109277);
    table[11].addpoint(    -0.5190961292068, 0.2331937645919);
    table[11].addpoint(    -0.2695431559523, 0.2628045445102);
    table[11].addpoint(                   0, 0.2729250867779);
    table[11].addpoint(     0.2695431559523, 0.2628045445102);
    table[11].addpoint(     0.5190961292068, 0.2331937645919);
    table[11].addpoint(      0.730152005574, 0.1862902109277);
    table[11].addpoint(     0.8870625997681, 0.1255803694649);
    table[11].addpoint(      0.978228658146, 0.05566856711617);

    table.push_back(GaussPtTable1(12, 12));
    table[12].addpoint(    -0.9815606342467, 0.0471753363865);
    table[12].addpoint(    -0.9041172563704, 0.1069393259953);
    table[12].addpoint(    -0.7699026741943, 0.1600783285433);
    table[12].addpoint(    -0.5873179542866, 0.203167426723);
    table[12].addpoint(    -0.3678314989981, 0.2334925365383);
    table[12].addpoint(    -0.1252334085114, 0.2491470458134);
    table[12].addpoint(     0.1252334085114, 0.2491470458134);
    table[12].addpoint(     0.3678314989981, 0.2334925365383);
    table[12].addpoint(     0.5873179542866, 0.203167426723);
    table[12].addpoint(     0.7699026741943, 0.1600783285433);
    table[12].addpoint(     0.9041172563704, 0.1069393259953);
    table[12].addpoint(     0.9815606342467, 0.0471753363865);

    table.push_back(GaussPtTable1(13, 13));
    table[13].addpoint(    -0.9841830547185, 0.04048400476531);
    table[13].addpoint(    -0.9175983992229, 0.09212149983772);
    table[13].addpoint(    -0.8015780907333, 0.1388735102197);
    table[13].addpoint(    -0.6423493394403, 0.1781459807619);
    table[13].addpoint(    -0.4484927510364, 0.2078160475368);
    table[13].addpoint(    -0.2304583159551, 0.2262831802629);
    table[13].addpoint(                   0, 0.2325515532308);
    table[13].addpoint(     0.2304583159551, 0.2262831802629);
    table[13].addpoint(     0.4484927510364, 0.2078160475368);
    table[13].addpoint(     0.6423493394403, 0.1781459807619);
    table[13].addpoint(     0.8015780907333, 0.1388735102197);
    table[13].addpoint(     0.9175983992229, 0.09212149983772);
    table[13].addpoint(     0.9841830547185, 0.04048400476531);

    table.push_back(GaussPtTable1(14, 14));
    table[14].addpoint(    -0.9862838086968, 0.03511946033174);
    table[14].addpoint(    -0.9284348836635, 0.08015808715976);
    table[14].addpoint(    -0.8272013150697, 0.1215185706879);
    table[14].addpoint(    -0.6872929048116, 0.1572031671581);
    table[14].addpoint(    -0.5152486363581, 0.1855383974779);
    table[14].addpoint(    -0.3191123689278, 0.2051984637213);
    table[14].addpoint(    -0.1080549487073, 0.2152638534631);
    table[14].addpoint(     0.1080549487073, 0.2152638534631);
    table[14].addpoint(     0.3191123689278, 0.2051984637213);
    table[14].addpoint(     0.5152486363581, 0.1855383974779);
    table[14].addpoint(     0.6872929048116, 0.1572031671581);
    table[14].addpoint(     0.8272013150697, 0.1215185706879);
    table[14].addpoint(     0.9284348836635, 0.08015808715976);
    table[14].addpoint(     0.9862838086968, 0.03511946033174);

    table.push_back(GaussPtTable1(15, 15));
    table[15].addpoint(    -0.9879925180204, 0.03075324199611);
    table[15].addpoint(    -0.9372733924007, 0.0703660474881);
    table[15].addpoint(    -0.8482065834104, 0.1071592204671);
    table[15].addpoint(    -0.7244177313601, 0.1395706779261);
    table[15].addpoint(    -0.5709721726085, 0.1662692058169);
    table[15].addpoint(    -0.3941513470775, 0.1861610000155);
    table[15].addpoint(    -0.2011940939974, 0.1984314853271);
    table[15].addpoint(  0.0, 0.2025782419255);
    table[15].addpoint(     0.2011940939974, 0.1984314853271);
    table[15].addpoint(     0.3941513470775, 0.1861610000155);
    table[15].addpoint(     0.5709721726085, 0.1662692058169);
    table[15].addpoint(     0.7244177313601, 0.1395706779261);
    table[15].addpoint(     0.8482065834104, 0.1071592204671);
    table[15].addpoint(     0.9372733924007, 0.0703660474881);
    table[15].addpoint(     0.9879925180204, 0.03075324199611);

    table.push_back(GaussPtTable1(16, 16));
    table[16].addpoint(    -0.9894009349916, 0.02715245941175);
    table[16].addpoint(    -0.9445750230732, 0.06225352393864);
    table[16].addpoint(    -0.8656312023878, 0.09515851168249);
    table[16].addpoint(     -0.755404408355, 0.1246289712554);
    table[16].addpoint(    -0.6178762444026, 0.1495959888165);
    table[16].addpoint(    -0.4580167776572, 0.169156519395);
    table[16].addpoint(    -0.2816035507792, 0.1826034150449);
    table[16].addpoint(   -0.09501250983763, 0.189450610455);
    table[16].addpoint(    0.09501250983763, 0.189450610455);
    table[16].addpoint(     0.2816035507792, 0.1826034150449);
    table[16].addpoint(     0.4580167776572, 0.169156519395);
    table[16].addpoint(     0.6178762444026, 0.1495959888165);
    table[16].addpoint(      0.755404408355, 0.1246289712554);
    table[16].addpoint(     0.8656312023878, 0.09515851168249);
    table[16].addpoint(     0.9445750230732, 0.06225352393864);
    table[16].addpoint(     0.9894009349916, 0.02715245941175);

    table.push_back(GaussPtTable1(17, 17));
    table[17].addpoint(    -0.9905754753144, 0.02414830286854);
    table[17].addpoint(    -0.9506755217687, 0.05545952937398);
    table[17].addpoint(    -0.8802391537269, 0.08503614831717);
    table[17].addpoint(    -0.7815140038968, 0.1118838471933);
    table[17].addpoint(    -0.6576711592166, 0.1351363684685);
    table[17].addpoint(    -0.5126905370864, 0.1540457610768);
    table[17].addpoint(    -0.3512317634538, 0.1680041021564);
    table[17].addpoint(    -0.1784841814958, 0.1765627053669);
    table[17].addpoint(  0.0, 0.1794464703562);
    table[17].addpoint(     0.1784841814958, 0.1765627053669);
    table[17].addpoint(     0.3512317634538, 0.1680041021564);
    table[17].addpoint(     0.5126905370864, 0.1540457610768);
    table[17].addpoint(     0.6576711592166, 0.1351363684685);
    table[17].addpoint(     0.7815140038968, 0.1118838471933);
    table[17].addpoint(     0.8802391537269, 0.08503614831717);
    table[17].addpoint(     0.9506755217687, 0.05545952937398);
    table[17].addpoint(     0.9905754753144, 0.02414830286854);

    table.push_back(GaussPtTable1(18, 18));
    table[18].addpoint(    -0.9915651684209, 0.02161601352648);
    table[18].addpoint(    -0.9558239495714, 0.04971454889497);
    table[18].addpoint(    -0.8926024664975, 0.07642573025488);
    table[18].addpoint(    -0.8037049589725, 0.1009420441062);
    table[18].addpoint(    -0.6916870430603, 0.1225552067114);
    table[18].addpoint(    -0.5597708310739, 0.1406429146706);
    table[18].addpoint(    -0.4117511614628, 0.1546846751262);
    table[18].addpoint(    -0.2518862256915, 0.1642764837458);
    table[18].addpoint(   -0.08477501304173, 0.1691423829631);
    table[18].addpoint(    0.08477501304173, 0.1691423829631);
    table[18].addpoint(     0.2518862256915, 0.1642764837458);
    table[18].addpoint(     0.4117511614628, 0.1546846751262);
    table[18].addpoint(     0.5597708310739, 0.1406429146706);
    table[18].addpoint(     0.6916870430603, 0.1225552067114);
    table[18].addpoint(     0.8037049589725, 0.1009420441062);
    table[18].addpoint(     0.8926024664975, 0.07642573025488);
    table[18].addpoint(     0.9558239495714, 0.04971454889497);
    table[18].addpoint(     0.9915651684209, 0.02161601352648);

    table.push_back(GaussPtTable1(19, 19));
    table[19].addpoint(    -0.9924068438435, 0.01946178822972);
    table[19].addpoint(    -0.9602081521348, 0.0448142267657);
    table[19].addpoint(    -0.9031559036148, 0.06904454273764);
    table[19].addpoint(    -0.8227146565371, 0.09149002162237);
    table[19].addpoint(    -0.7209661773352, 0.1115666455473);
    table[19].addpoint(    -0.6005453046616, 0.1287539625393);
    table[19].addpoint(    -0.4645707413759, 0.1426067021736);
    table[19].addpoint(    -0.3165640999636, 0.1527660420658);
    table[19].addpoint(    -0.1603586456402, 0.1589688433939);
    table[19].addpoint(  0.0, 0.1610544498487);
    table[19].addpoint(     0.1603586456402, 0.1589688433939);
    table[19].addpoint(     0.3165640999636, 0.1527660420658);
    table[19].addpoint(     0.4645707413759, 0.1426067021736);
    table[19].addpoint(     0.6005453046616, 0.1287539625393);
    table[19].addpoint(     0.7209661773352, 0.1115666455473);
    table[19].addpoint(     0.8227146565371, 0.09149002162237);
    table[19].addpoint(     0.9031559036148, 0.06904454273764);
    table[19].addpoint(     0.9602081521348, 0.0448142267657);
    table[19].addpoint(     0.9924068438435, 0.01946178822972);

    table.push_back(GaussPtTable1(20, 20));
    table[20].addpoint(     -0.993128599185, 0.01761400713915);
    table[20].addpoint(    -0.9639719272779, 0.04060142980038);
    table[20].addpoint(    -0.9122344282513, 0.0626720483341);
    table[20].addpoint(    -0.8391169718222, 0.08327674157662);
    table[20].addpoint(    -0.7463319064601, 0.1019301198172);
    table[20].addpoint(    -0.6360536807265, 0.1181945319615);
    table[20].addpoint(    -0.5108670019508, 0.1316886384491);
    table[20].addpoint(    -0.3737060887154, 0.1420961093183);
    table[20].addpoint(    -0.2277858511416, 0.1491729864726);
    table[20].addpoint(   -0.07652652113349, 0.1527533871307);
    table[20].addpoint(    0.07652652113349, 0.1527533871307);
    table[20].addpoint(     0.2277858511416, 0.1491729864726);
    table[20].addpoint(     0.3737060887154, 0.1420961093183);
    table[20].addpoint(     0.5108670019508, 0.1316886384491);
    table[20].addpoint(     0.6360536807265, 0.1181945319615);
    table[20].addpoint(     0.7463319064601, 0.1019301198172);
    table[20].addpoint(     0.8391169718222, 0.08327674157662);
    table[20].addpoint(     0.9122344282513, 0.0626720483341);
    table[20].addpoint(     0.9639719272779, 0.04060142980038);
    table[20].addpoint(      0.993128599185, 0.01761400713915);

    table.push_back(GaussPtTable1(21, 21));
    table[21].addpoint(    -0.9937521706203, 0.01601722825777);
    table[21].addpoint(    -0.9672268385663, 0.03695378977085);
    table[21].addpoint(    -0.9200993341504, 0.05713442542685);
    table[21].addpoint(    -0.8533633645833, 0.0761001136283);
    table[21].addpoint(    -0.7684399634756, 0.09344442345602);
    table[21].addpoint(    -0.6671388041974, 0.1087972991671);
    table[21].addpoint(    -0.5516188358872, 0.1218314160537);
    table[21].addpoint(    -0.4243421202074, 0.1322689386333);
    table[21].addpoint(    -0.2880213168024, 0.139887394791);
    table[21].addpoint(    -0.1455618541609, 0.1445244039899);
    table[21].addpoint(  0.0, 0.1460811336496);
    table[21].addpoint(     0.1455618541609, 0.1445244039899);
    table[21].addpoint(     0.2880213168024, 0.139887394791);
    table[21].addpoint(     0.4243421202074, 0.1322689386333);
    table[21].addpoint(     0.5516188358872, 0.1218314160537);
    table[21].addpoint(     0.6671388041974, 0.1087972991671);
    table[21].addpoint(     0.7684399634756, 0.09344442345602);
    table[21].addpoint(     0.8533633645833, 0.0761001136283);
    table[21].addpoint(     0.9200993341504, 0.05713442542685);
    table[21].addpoint(     0.9672268385663, 0.03695378977085);
    table[21].addpoint(     0.9937521706203, 0.01601722825777);

    table.push_back(GaussPtTable1(22, 22));
    table[22].addpoint(    -0.9942945854824, 0.01462799529827);
    table[22].addpoint(    -0.9700604978354, 0.03377490158481);
    table[22].addpoint(    -0.9269567721871, 0.05229333515268);
    table[22].addpoint(    -0.8658125777203, 0.06979646842444);
    table[22].addpoint(    -0.7878168059792, 0.08594160621706);
    table[22].addpoint(    -0.6944872631866, 0.1004141444428);
    table[22].addpoint(    -0.5876404035069, 0.1129322960805);
    table[22].addpoint(    -0.4693558379867, 0.1232523768105);
    table[22].addpoint(     -0.341935820892, 0.131173504787);
    table[22].addpoint(    -0.2078604266882, 0.136541498346);
    table[22].addpoint(   -0.06973927331972, 0.1392518728556);
    table[22].addpoint(    0.06973927331972, 0.1392518728556);
    table[22].addpoint(     0.2078604266882, 0.136541498346);
    table[22].addpoint(      0.341935820892, 0.131173504787);
    table[22].addpoint(     0.4693558379867, 0.1232523768105);
    table[22].addpoint(     0.5876404035069, 0.1129322960805);
    table[22].addpoint(     0.6944872631866, 0.1004141444428);
    table[22].addpoint(     0.7878168059792, 0.08594160621706);
    table[22].addpoint(     0.8658125777203, 0.06979646842444);
    table[22].addpoint(     0.9269567721871, 0.05229333515268);
    table[22].addpoint(     0.9700604978354, 0.03377490158481);
    table[22].addpoint(     0.9942945854824, 0.01462799529827);

    table.push_back(GaussPtTable1(23, 23));
    table[23].addpoint(    -0.9947693349975, 0.01341185948714);
    table[23].addpoint(    -0.9725424712181, 0.03098800585697);
    table[23].addpoint(     -0.932971086826, 0.04803767173108);
    table[23].addpoint(    -0.8767523582704, 0.06423242140845);
    table[23].addpoint(    -0.8048884016188, 0.07928141177671);
    table[23].addpoint(    -0.7186613631319, 0.09291576606003);
    table[23].addpoint(    -0.6196098757636, 0.1048920914645);
    table[23].addpoint(     -0.509501477846, 0.1149966402224);
    table[23].addpoint(    -0.3903010380302, 0.1230490843067);
    table[23].addpoint(    -0.2641356809703, 0.128905722188);
    table[23].addpoint(    -0.1332568242984, 0.1324620394047);
    table[23].addpoint(  0.0, 0.1336545721861);
    table[23].addpoint(     0.1332568242984, 0.1324620394047);
    table[23].addpoint(     0.2641356809703, 0.128905722188);
    table[23].addpoint(     0.3903010380302, 0.1230490843067);
    table[23].addpoint(      0.509501477846, 0.1149966402224);
    table[23].addpoint(     0.6196098757636, 0.1048920914645);
    table[23].addpoint(     0.7186613631319, 0.09291576606003);
    table[23].addpoint(     0.8048884016188, 0.07928141177671);
    table[23].addpoint(     0.8767523582704, 0.06423242140845);
    table[23].addpoint(      0.932971086826, 0.04803767173108);
    table[23].addpoint(     0.9725424712181, 0.03098800585697);
    table[23].addpoint(     0.9947693349975, 0.01341185948714);

    table.push_back(GaussPtTable1(24, 24));
    table[24].addpoint(     -0.995187219997, 0.01234122979998);
    table[24].addpoint(    -0.9747285559713, 0.02853138862893);
    table[24].addpoint(    -0.9382745520027, 0.04427743881742);
    table[24].addpoint(    -0.8864155270044, 0.05929858491536);
    table[24].addpoint(    -0.8200019859739, 0.07334648141107);
    table[24].addpoint(    -0.7401241915785, 0.08619016153195);
    table[24].addpoint(    -0.6480936519369, 0.09761865210411);
    table[24].addpoint(    -0.5454214713888, 0.1074442701159);
    table[24].addpoint(     -0.433793507626, 0.1155056680537);
    table[24].addpoint(    -0.3150426796961, 0.1216704729278);
    table[24].addpoint(    -0.1911188674736, 0.1258374563468);
    table[24].addpoint(    -0.0640568928626, 0.1279381953467);
    table[24].addpoint(     0.0640568928626, 0.1279381953467);
    table[24].addpoint(     0.1911188674736, 0.1258374563468);
    table[24].addpoint(     0.3150426796961, 0.1216704729278);
    table[24].addpoint(      0.433793507626, 0.1155056680537);
    table[24].addpoint(     0.5454214713888, 0.1074442701159);
    table[24].addpoint(     0.6480936519369, 0.09761865210411);
    table[24].addpoint(     0.7401241915785, 0.08619016153195);
    table[24].addpoint(     0.8200019859739, 0.07334648141107);
    table[24].addpoint(     0.8864155270044, 0.05929858491536);
    table[24].addpoint(     0.9382745520027, 0.04427743881742);
    table[24].addpoint(     0.9747285559713, 0.02853138862893);
    table[24].addpoint(      0.995187219997, 0.01234122979998);

    table.push_back(GaussPtTable1(25, 25));
    table[25].addpoint(    -0.9955569697905, 0.01139379850102);
    table[25].addpoint(    -0.9766639214595, 0.02635498661503);
    table[25].addpoint(    -0.9429745712289, 0.0409391567013);
    table[25].addpoint(    -0.8949919978782, 0.05490469597576);
    table[25].addpoint(    -0.8334426287608, 0.06803833381234);
    table[25].addpoint(    -0.7592592630373, 0.080140700335);
    table[25].addpoint(    -0.6735663684734, 0.09102826198296);
    table[25].addpoint(    -0.5776629302412, 0.100535949067);
    table[25].addpoint(    -0.4730027314457, 0.1085196244742);
    table[25].addpoint(    -0.3611723058093, 0.1148582591457);
    table[25].addpoint(    -0.2438668837209, 0.1194557635357);
    table[25].addpoint(    -0.1228646926107, 0.1222424429903);
    table[25].addpoint(                   0, 0.1231760537267);
    table[25].addpoint(     0.1228646926107, 0.1222424429903);
    table[25].addpoint(     0.2438668837209, 0.1194557635357);
    table[25].addpoint(     0.3611723058093, 0.1148582591457);
    table[25].addpoint(     0.4730027314457, 0.1085196244742);
    table[25].addpoint(     0.5776629302412, 0.100535949067);
    table[25].addpoint(     0.6735663684734, 0.09102826198296);
    table[25].addpoint(     0.7592592630373, 0.080140700335);
    table[25].addpoint(     0.8334426287608, 0.06803833381234);
    table[25].addpoint(     0.8949919978782, 0.05490469597576);
    table[25].addpoint(     0.9429745712289, 0.0409391567013);
    table[25].addpoint(     0.9766639214595, 0.02635498661503);
    table[25].addpoint(     0.9955569697905, 0.01139379850102);

    table.push_back(GaussPtTable1(26, 26));
    table[26].addpoint(    -0.9958857011456, 0.01055137261734);
    table[26].addpoint(    -0.9783854459564, 0.02441785109263);
    table[26].addpoint(    -0.9471590666617, 0.03796238329436);
    table[26].addpoint(    -0.9026378619843, 0.05097582529707);
    table[26].addpoint(    -0.8454459427885, 0.06327404632956);
    table[26].addpoint(    -0.7763859488206, 0.07468414976565);
    table[26].addpoint(    -0.6964272604199, 0.08504589431348);
    table[26].addpoint(    -0.6066922930176, 0.09421380035591);
    table[26].addpoint(    -0.5084407148245, 0.1020591610944);
    table[26].addpoint(    -0.4030517551234, 0.1084718405285);
    table[26].addpoint(    -0.2920048394859, 0.1133618165463);
    table[26].addpoint(    -0.1768588203568, 0.1166604434853);
    table[26].addpoint(   -0.05923009342931, 0.1183214152792);
    table[26].addpoint(    0.05923009342931, 0.1183214152792);
    table[26].addpoint(     0.1768588203568, 0.1166604434853);
    table[26].addpoint(     0.2920048394859, 0.1133618165463);
    table[26].addpoint(     0.4030517551234, 0.1084718405285);
    table[26].addpoint(     0.5084407148245, 0.1020591610944);
    table[26].addpoint(     0.6066922930176, 0.09421380035591);
    table[26].addpoint(     0.6964272604199, 0.08504589431348);
    table[26].addpoint(     0.7763859488206, 0.07468414976565);
    table[26].addpoint(     0.8454459427885, 0.06327404632956);
    table[26].addpoint(     0.9026378619843, 0.05097582529707);
    table[26].addpoint(     0.9471590666617, 0.03796238329436);
    table[26].addpoint(     0.9783854459564, 0.02441785109263);
    table[26].addpoint(     0.9958857011456, 0.01055137261734);

    table.push_back(GaussPtTable1(27, 27));
    table[27].addpoint(    -0.9961792628889, 0.009798996051293);
    table[27].addpoint(    -0.9799234759615, 0.02268623159618);
    table[27].addpoint(    -0.9509005578147, 0.03529705375742);
    table[27].addpoint(    -0.9094823206774, 0.04744941252054);
    table[27].addpoint(    -0.8562079080182, 0.05898353685982);
    table[27].addpoint(    -0.7917716390705, 0.06974882376624);
    table[27].addpoint(    -0.7170134737394, 0.07960486777305);
    table[27].addpoint(    -0.6329079719465, 0.08842315854375);
    table[27].addpoint(    -0.5405515645794, 0.09608872737002);
    table[27].addpoint(      -0.44114825175, 0.1025016378177);
    table[27].addpoint(    -0.3359939036385, 0.1075782857885);
    table[27].addpoint(    -0.2264593654395, 0.1112524883568);
    table[27].addpoint(    -0.1139725856095, 0.1134763461089);
    table[27].addpoint(  0.0, 0.1142208673789);
    table[27].addpoint(     0.1139725856095, 0.1134763461089);
    table[27].addpoint(     0.2264593654395, 0.1112524883568);
    table[27].addpoint(     0.3359939036385, 0.1075782857885);
    table[27].addpoint(       0.44114825175, 0.1025016378177);
    table[27].addpoint(     0.5405515645794, 0.09608872737002);
    table[27].addpoint(     0.6329079719465, 0.08842315854375);
    table[27].addpoint(     0.7170134737394, 0.07960486777305);
    table[27].addpoint(     0.7917716390705, 0.06974882376624);
    table[27].addpoint(     0.8562079080182, 0.05898353685982);
    table[27].addpoint(     0.9094823206774, 0.04744941252054);
    table[27].addpoint(     0.9509005578147, 0.03529705375742);
    table[27].addpoint(     0.9799234759615, 0.02268623159618);
    table[27].addpoint(     0.9961792628889, 0.009798996051293);

    table.push_back(GaussPtTable1(28, 28));
    table[28].addpoint(    -0.9964424975739, 0.009124282593093);
    table[28].addpoint(    -0.9813031653708, 0.02113211259277);
    table[28].addpoint(    -0.9542592806289, 0.0329014277823);
    table[28].addpoint(    -0.9156330263921, 0.04427293475893);
    table[28].addpoint(    -0.8658925225744, 0.0551073456757);
    table[28].addpoint(    -0.8056413709171, 0.06527292396699);
    table[28].addpoint(    -0.7356108780136, 0.07464621423456);
    table[28].addpoint(    -0.6566510940388, 0.0831134172289);
    table[28].addpoint(    -0.5697204718114, 0.09057174439303);
    table[28].addpoint(    -0.4758742249551, 0.09693065799793);
    table[28].addpoint(     -0.376251516089, 0.102112967578);
    table[28].addpoint(    -0.2720616276351, 0.1060557659228);
    table[28].addpoint(    -0.1645692821333, 0.1087111922582);
    table[28].addpoint(   -0.05507928988403, 0.1100470130164);
    table[28].addpoint(    0.05507928988403, 0.1100470130164);
    table[28].addpoint(     0.1645692821333, 0.1087111922582);
    table[28].addpoint(     0.2720616276351, 0.1060557659228);
    table[28].addpoint(      0.376251516089, 0.102112967578);
    table[28].addpoint(     0.4758742249551, 0.09693065799793);
    table[28].addpoint(     0.5697204718114, 0.09057174439303);
    table[28].addpoint(     0.6566510940388, 0.0831134172289);
    table[28].addpoint(     0.7356108780136, 0.07464621423456);
    table[28].addpoint(     0.8056413709171, 0.06527292396699);
    table[28].addpoint(     0.8658925225744, 0.0551073456757);
    table[28].addpoint(     0.9156330263921, 0.04427293475893);
    table[28].addpoint(     0.9542592806289, 0.0329014277823);
    table[28].addpoint(     0.9813031653708, 0.02113211259277);
    table[28].addpoint(     0.9964424975739, 0.009124282593093);

    table.push_back(GaussPtTable1(29, 29));
    table[29].addpoint(    -0.9966794422606, 0.008516903878745);
    table[29].addpoint(    -0.9825455052614, 0.01973208505612);
    table[29].addpoint(     -0.957285595778, 0.03074049220209);
    table[29].addpoint(     -0.921180232953, 0.04140206251862);
    table[29].addpoint(    -0.8746378049201, 0.05159482690248);
    table[29].addpoint(    -0.8181854876152, 0.06120309065707);
    table[29].addpoint(    -0.7524628517344, 0.07011793325505);
    table[29].addpoint(    -0.6782145376026, 0.07823832713576);
    table[29].addpoint(    -0.5962817971382, 0.08547225736617);
    table[29].addpoint(    -0.5075929551242, 0.09173775713925);
    table[29].addpoint(     -0.413152888174, 0.0969638340944);
    table[29].addpoint(    -0.3140316378676, 0.1010912737599);
    table[29].addpoint(     -0.211352286166, 0.1040733100777);
    table[29].addpoint(    -0.1062782301326, 0.1058761550973);
    table[29].addpoint(  0.0, 0.1064793817183);
    table[29].addpoint(     0.1062782301326, 0.1058761550973);
    table[29].addpoint(      0.211352286166, 0.1040733100777);
    table[29].addpoint(     0.3140316378676, 0.1010912737599);
    table[29].addpoint(      0.413152888174, 0.0969638340944);
    table[29].addpoint(     0.5075929551242, 0.09173775713925);
    table[29].addpoint(     0.5962817971382, 0.08547225736617);
    table[29].addpoint(     0.6782145376026, 0.07823832713576);
    table[29].addpoint(     0.7524628517344, 0.07011793325505);
    table[29].addpoint(     0.8181854876152, 0.06120309065707);
    table[29].addpoint(     0.8746378049201, 0.05159482690248);
    table[29].addpoint(      0.921180232953, 0.04140206251862);
    table[29].addpoint(      0.957285595778, 0.03074049220209);
    table[29].addpoint(     0.9825455052614, 0.01973208505612);
    table[29].addpoint(     0.9966794422606, 0.008516903878745);

    table.push_back(GaussPtTable1(30, 30));
    table[30].addpoint(    -0.9968934840746, 0.007968192496165);
    table[30].addpoint(    -0.9836681232797, 0.01846646831109);
    table[30].addpoint(    -0.9600218649683, 0.02878470788332);
    table[30].addpoint(    -0.9262000474292, 0.03879919256956);
    table[30].addpoint(     -0.882560535792, 0.04840267283058);
    table[30].addpoint(    -0.8295657623827, 0.05749315621761);
    table[30].addpoint(    -0.7677774321048, 0.06597422988218);
    table[30].addpoint(    -0.6978504947933, 0.0737559747377);
    table[30].addpoint(    -0.6205261829892, 0.08075589522942);
    table[30].addpoint(     -0.536624148142, 0.08689978720108);
    table[30].addpoint(     -0.447033769538, 0.09212252223778);
    table[30].addpoint(    -0.3527047255308, 0.09636873717464);
    table[30].addpoint(    -0.2546369261678, 0.09959342058679);
    table[30].addpoint(    -0.1538699136085, 0.1017623897484);
    table[30].addpoint(   -0.05147184255531, 0.1028526528935);
    table[30].addpoint(    0.05147184255531, 0.1028526528935);
    table[30].addpoint(     0.1538699136085, 0.1017623897484);
    table[30].addpoint(     0.2546369261678, 0.09959342058679);
    table[30].addpoint(     0.3527047255308, 0.09636873717464);
    table[30].addpoint(      0.447033769538, 0.09212252223778);
    table[30].addpoint(      0.536624148142, 0.08689978720108);
    table[30].addpoint(     0.6205261829892, 0.08075589522942);
    table[30].addpoint(     0.6978504947933, 0.0737559747377);
    table[30].addpoint(     0.7677774321048, 0.06597422988218);
    table[30].addpoint(     0.8295657623827, 0.05749315621761);
    table[30].addpoint(      0.882560535792, 0.04840267283058);
    table[30].addpoint(     0.9262000474292, 0.03879919256956);
    table[30].addpoint(     0.9600218649683, 0.02878470788332);
    table[30].addpoint(     0.9836681232797, 0.01846646831109);
    table[30].addpoint(     0.9968934840746, 0.007968192496165);

    table.push_back(GaussPtTable1(31, 31));
    table[31].addpoint(    -0.9970874818194, 0.007470831579248);
    table[31].addpoint(    -0.9846859096651, 0.01731862079031);
    table[31].addpoint(    -0.9625039250929, 0.02700901918497);
    table[31].addpoint(    -0.9307569978966, 0.03643227391232);
    table[31].addpoint(    -0.8897600299482, 0.04549370752719);
    table[31].addpoint(    -0.8399203201462, 0.05410308242491);
    table[31].addpoint(    -0.7817331484166, 0.06217478656102);
    table[31].addpoint(    -0.7157767845868, 0.06962858323541);
    table[31].addpoint(    -0.6427067229242, 0.07639038659877);
    table[31].addpoint(    -0.5632491614071, 0.08239299176158);
    table[31].addpoint(    -0.4781937820449, 0.08757674060847);
    table[31].addpoint(    -0.3883859016082, 0.09189011389364);
    table[31].addpoint(    -0.2947180699817, 0.09529024291232);
    table[31].addpoint(    -0.1981211993355, 0.09774333538632);
    table[31].addpoint(   -0.09955531215234, 0.09922501122667);
    table[31].addpoint(  0.0, 0.09972054479342);
    table[31].addpoint(    0.09955531215234, 0.09922501122667);
    table[31].addpoint(     0.1981211993355, 0.09774333538632);
    table[31].addpoint(     0.2947180699817, 0.09529024291232);
    table[31].addpoint(     0.3883859016082, 0.09189011389364);
    table[31].addpoint(     0.4781937820449, 0.08757674060847);
    table[31].addpoint(     0.5632491614071, 0.08239299176158);
    table[31].addpoint(     0.6427067229242, 0.07639038659877);
    table[31].addpoint(     0.7157767845868, 0.06962858323541);
    table[31].addpoint(     0.7817331484166, 0.06217478656102);
    table[31].addpoint(     0.8399203201462, 0.05410308242491);
    table[31].addpoint(     0.8897600299482, 0.04549370752719);
    table[31].addpoint(     0.9307569978966, 0.03643227391232);
    table[31].addpoint(     0.9625039250929, 0.02700901918497);
    table[31].addpoint(     0.9846859096651, 0.01731862079031);
    table[31].addpoint(     0.9970874818194, 0.007470831579248);

    table.push_back(GaussPtTable1(32, 32));
    table[32].addpoint(    -0.9972638618494, 0.007018610009469);
    table[32].addpoint(    -0.9856115115452, 0.0162743947309);
    table[32].addpoint(    -0.9647622555875, 0.02539206530926);
    table[32].addpoint(    -0.9349060759377, 0.03427386291296);
    table[32].addpoint(     -0.896321155766, 0.04283589802221);
    table[32].addpoint(    -0.8493676137325, 0.05099805926237);
    table[32].addpoint(    -0.7944837959679, 0.05868409347853);
    table[32].addpoint(    -0.7321821187402, 0.06582222277636);
    table[32].addpoint(    -0.6630442669302, 0.07234579410884);
    table[32].addpoint(    -0.5877157572407, 0.07819389578707);
    table[32].addpoint(    -0.5068999089322, 0.08331192422694);
    table[32].addpoint(    -0.4213512761306, 0.0876520930044);
    table[32].addpoint(    -0.3318686022821, 0.09117387869576);
    table[32].addpoint(    -0.2392873622521, 0.0938443990808);
    table[32].addpoint(    -0.1444719615828, 0.09563872007927);
    table[32].addpoint(   -0.04830766568773, 0.09654008851472);
    table[32].addpoint(    0.04830766568773, 0.09654008851472);
    table[32].addpoint(     0.1444719615828, 0.09563872007927);
    table[32].addpoint(     0.2392873622521, 0.0938443990808);
    table[32].addpoint(     0.3318686022821, 0.09117387869576);
    table[32].addpoint(     0.4213512761306, 0.0876520930044);
    table[32].addpoint(     0.5068999089322, 0.08331192422694);
    table[32].addpoint(     0.5877157572407, 0.07819389578707);
    table[32].addpoint(     0.6630442669302, 0.07234579410884);
    table[32].addpoint(     0.7321821187402, 0.06582222277636);
    table[32].addpoint(     0.7944837959679, 0.05868409347853);
    table[32].addpoint(     0.8493676137325, 0.05099805926237);
    table[32].addpoint(      0.896321155766, 0.04283589802221);
    table[32].addpoint(     0.9349060759377, 0.03427386291296);
    table[32].addpoint(     0.9647622555875, 0.02539206530926);
    table[32].addpoint(     0.9856115115452, 0.0162743947309);
    table[32].addpoint(     0.9972638618494, 0.007018610009469);
#endif // HIGH_ORDERS
  }
  return table;
}

int GaussPtTable1::n_orders() {
  return one_d_gauss_pts().size();
}

int GaussPtTable1::npts(int order) {
  return one_d_gauss_pts()[order].size();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// EdgeGaussPoint is a mapping wrapper (also a wrapping mapper)
// for GaussPoint1.

EdgeGaussPoint::EdgeGaussPoint(const BoundaryEdge *e, int order)
  : edge(e),
    gpone(order, 0, 1),
    gweight(0.0),
    recalculate_geometry(true)
{
}

EdgeGaussPoint::~EdgeGaussPoint() {}

void EdgeGaussPoint::operator++() {
  ++gpone;
  recalculate_geometry = true;
}

double EdgeGaussPoint::weight() const {
  geometry();
  return gweight;
}

Coord EdgeGaussPoint::position() const {
  geometry();
  return here;
}

#if DIM == 2
Coord EdgeGaussPoint::normal() const {
  geometry();
  return normal_;
}
#endif // DIM == 2

MasterCoord EdgeGaussPoint::mastercoord() const {
  geometry();
  return mhere;
}

void EdgeGaussPoint::geometry() const {
  if(recalculate_geometry) {
    recalculate_geometry = false;
    gweight = gpone.weight();  // Starting value.
    mhere = edge->start + gpone.position()*(edge->director);
    here = edge->el->from_master(mhere);

    double jac[DIM][DIM];

    for(SpaceIndex i=0; i<DIM; ++i) {
      for(SpaceIndex j=0; j<DIM; ++j) { 
	jac[i][j] = edge->el->jacobian(i,j,mhere);
      }
    }
#if DIM==2
    // tangent = (e dot grad) u
    // where e is the directed master element edge vector
    // grad is the gradient in master space
    // u is the function that maps master space to physical space
    tangent = Coord(jac[0][0]*(edge->director[0])    
		    + jac[0][1]*(edge->director[1]),
		    jac[1][0]*(edge->director[0])
		    + jac[1][1]*(edge->director[1]) );
#elif DIM==3
    tangent = Coord(jac[0][0]*(edge->director[0])    
		    + jac[0][1]*(edge->director[1])    
		    + jac[0][2]*(edge->director[2]),
		    jac[1][0]*(edge->director[0])
		    + jac[1][1]*(edge->director[1])
		    + jac[1][2]*(edge->director[2]),
		    jac[2][0]*(edge->director[0])
		    + jac[2][1]*(edge->director[1])
		    + jac[2][2]*(edge->director[2]) );
#endif
  
    double tnorm = sqrt(norm2(tangent));
    gweight*=tnorm;
    // Normalized tangent is the Jacobian of the 1D map.
#if DIM==2
    normal_ = Coord(tangent(1)/tnorm, -tangent(0)/tnorm);
#endif // DIM==2
    // Real space normal is normalized cross product of tangent w/ +z.
  }
}

double EdgeGaussPoint::shapefunction(const ShapeFunction &sf,
				     ShapeFunctionIndex n) const {
  return sf.value(n, mastercoord());
}

double EdgeGaussPoint::mdshapefunction(const ShapeFunction &sf,
				      ShapeFunctionIndex n, SpaceIndex i)
  const
{
  return sf.masterderiv(n, i, mastercoord());
}

double EdgeGaussPoint::dshapefunction(const ElementBase *el,
				      const ShapeFunction &sf,
				      ShapeFunctionIndex n, SpaceIndex i)
const
{
  return sf.realderiv(el, n, i, mastercoord());
}

std::ostream &EdgeGaussPoint::print(std::ostream &os) const {
  os << "EdgeGaussPoint" << mhere; // TODO OPT: probably not the most useful output
  return os;
}

