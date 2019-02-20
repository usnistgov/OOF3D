// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modifed
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */


#include "common/coord.h"
#include "common/IO/canvaslayers.h"
#include "common/IO/oofcerr.h"
#include "common/geometry.h"
#include "common/voxelsetboundary.h"
#include "common/cmicrostructure.h"
#include "common/printvec.h"
#include "common/VSB/vsb.h"
#include <limits>

void initializeVSB() {
  initializeProtoNodes<Coord3D, ICoord3D>();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

VoxelSetBoundary::VoxelSetBoundary(const CMicrostructure *ms,
				   const BinList &bins,
				   int cat)
  : microstructure(ms)
{
  vsb =
    buildVSB<Coord3D, ICoord3D, Array<int>, int>(*ms->getCategoryMapRO(), cat,
						 ms->volumeOfVoxels(), bins);
}

VoxelSetBoundary::~VoxelSetBoundary() {
  delete vsb;
}

double VoxelSetBoundary::clippedVolume(
		       const CRectPrism<Coord3D> &ebbox,
		       const std::vector<VSBPlane<Coord3D>> &planes)
  const
{
  return vsb->clippedVolume(ebbox, planes);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

bool VoxelSetBoundary::checkEdges() const {
  return vsb->checkEdges();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void VoxelSetBoundary::dump(std::ostream &os) const {
  vsb->dump(os);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Converter is a functional that converts the voxel coordinates used
// by the VSB code to physical coordinates, so that the output of the
// debugging functions can be plotted properly.

struct Converter {
  const CMicrostructure *ms;
  Converter(const CMicrostructure *ms) : ms(ms) {}
  Coord3D operator()(const Coord3D &x) { return ms->pixel2Physical(x); }
};

void VoxelSetBoundary::dumpLines(const std::string &filename) const {
  Converter cnv(microstructure);
  vsb->dumpLines(filename, cnv);
}

void VoxelSetBoundary::saveClippedVSB(
			      const std::vector<VSBPlane<Coord3D>> &planes,
			      const std::string &filename)
  const
{
  Converter cnv(microstructure);
  vsb->saveClippedVSB(planes, cnv, filename);
}

VoxelSetBdy<Coord3D, ICoord3D, int>::EdgeIterator VoxelSetBoundary::iterator()
  const
{
  return vsb->iterator();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class GraphPlotter {
private:
  const CMicrostructure *ms;
  LineSegmentLayer *layer;
public:
  GraphPlotter(const CMicrostructure *ms, LineSegmentLayer *layer)
    : ms(ms), layer(layer)
  {}
  void operator()(const VoxelSetBdy<Coord3D, ICoord3D, int>::Graph *graph) {
    unsigned int nsegs = (3*graph->size())/2;
    layer->set_nSegs(nsegs);
    for(unsigned int i=0; i<graph->size(); i++) {
      auto node = graph->getNode(i);
      for(unsigned int nbrno=0; nbrno<3; nbrno++) {
	auto nbr = node->getNeighbor(nbrno);
	if(nbr && node->getIndex() < nbr->getIndex()) {
	  Coord3D pt0 = ms->pixel2Physical(node->position);
	  Coord3D pt1 = ms->pixel2Physical(nbr->position);
	  layer->addSegment(&pt0, &pt1);
	}
      }
    }
  }
};

void VoxelSetBoundary::drawClippedVSB(
			      const std::vector<VSBPlane<Coord3D>> &planes,
			      LineSegmentLayer *layer)
  const
{
  GraphPlotter plotter(microstructure, layer);
  vsb->drawClippedVSB(planes, plotter);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void printHomogRegionStats() {
  oofcerr << "printHomogRegionStats: nRegionsUsed=" << nRegionsUsed
	  << " nHomogCalcs=" << nHomogCalcs
	  << " average regions/calc =" << nRegionsUsed/(double)nHomogCalcs
	  << std::endl;
  nRegionsUsed = 0;
  nHomogCalcs = 0;
}
