// findFaceFacetsOLD outline:

// 0. Create FaceFacet objects in faceFacets

// 1. Get segments that cross faces from PixelPlaneFacets.

// 2. For each face that's not also a pixel plane:
//   2a. Call checkEquiv for start and end points of each segment.
//   2b. Create lists of FaceEdgeIntersection objects for start and end points.
//   2c. Find matches between start and end points.
//   2d. Store unmatched points in the LooseEnd catalog for each edge,
//       if they're on edges, and in the stranded list if they're not.

// 3. Pair up and merge stranded points that are on different faces
//    but share the same pixel planes.  Merging will put them on
//    edges, so put them in the LooseEnd catalog.

// 4. Put stranded points that can't be merged into the marooned list
//    for their face.

// 5. For each face that's not also a pixel plane:
//   5a. Put marooned points onto the closest edge and in the LooseEnds catalog.

//   5b. Look for facet edges that lie along a face edge and store
//       them in the edgeEdges list.

//   5c. For each edge of the face:
//     5c1. Coincidence check part 1: merge pts at the same parametric position
//      5c1a. Merge equivalence classes
//      5c1b. Remove equal numbers of start & stop points from LooseEnd catalog
//     5c2. Coincidence check part 2: remove crossing segments
//       For pairs of consecutive entries in the LooseEnd map for the edge
//        If the pixel plane edges cross
//          Delete the points from the loose end catalog
//     5c3. Occupied segment check
//        Look for nearby pairs of start-stop points that lie on face
//        edges that already contain an edge (from edgeEdges, 5b).
//           Remove the points from the LooseEnd map and merge their
//           equivalence classes.

//   5d. Check that the number of starts and stops agree and throw an
//       exception if they don't.  OR, if CLEAN_UP_LOOSE_ENDS is
//       defined, remove extra stops or starts, choosing the ones that
//       are closest to their neighbors.

//   5e. Create missing segments by joining stops to starts, going
//       clockwise around the perimeter of the face.



//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

#ifdef FINDFACEFACETS_OLD
FaceFacets HomogeneityTet::findFaceFacetsOLD(unsigned int cat,
					  const FacetMap2D &planeFacets)
{
#ifdef DEBUG
  verbosecategory = verboseCategory_(verbose, cat);
  if(verbosecategory)
    oofcerr << "HomogeneityTet::findFaceFacets: cat=" << cat << std::endl;
  OOFcerrIndent indent(2);
#endif // DEBUG
  FaceFacets faceFacets;
  faceFacets.reserve(NUM_TET_FACES);
  for(unsigned int f=0; f<NUM_TET_FACES; f++)
    faceFacets.emplace_back(f, this);

  // Loop over pixel plane facets, sorting the edges that lie in tet
  // faces.

  for(FacetMap2D::const_iterator fm=planeFacets.begin(); fm!=planeFacets.end();
      ++fm)
    {
      PixelPlaneFacet *planeFacet = (*fm).second;
      // getEdgesOnFaces asks each PolygonEdge to store a reversed
      // copy of itself in faceFacets.  A new FaceFacetEdge is created
      // in faceFacets for each edge of the PixelPlaneFacet that lies
      // in a tet face.
// #ifdef DEBUG
//       if(verbosecategory)
// 	oofcerr << "HomogeneityTet::findFaceFacets: calling getEdgesOnFaces for"
// 		<< " " << *planeFacet->pixplane << std::endl;
//       OOFcerrIndent indent(2);
// #endif	// DEBUG
      planeFacet->getEdgesOnFaces(faceFacets);
    }
#ifdef DEBUG
  if(verbosecategory) {
    oofcerr << "HomogeneityTet::findFaceFacets: edges from pixel plane facets:"
	    << std::endl;
    OOFcerrIndent indent(2);
    for(unsigned int f=0; f<NUM_TET_FACES; f++) {
      verboseface = verboseFace_(verbosecategory, f);
      if(verboseface) {
	if(coincidentPixelPlanes[f] == nullptr) {
	  oofcerr << "HomogeneityTet::findFaceFacets: facet=" << faceFacets[f]
		  << std::endl;
	  faceFacets[f].dump("facefacet_orig", cat);
	}
      }
      verboseface = false;
    }
  }
#endif	// DEBUG

  // The segments on each face facet must (eventually) join together
  // end to end to form a closed polygon.  They don't necessarily do
  // so yet, because the polygon may need to be closed by adding
  // segments along the perimeter of the face.  Also, if a VSB
  // boundary passed through a tet edge, it may have resulted in an
  // ENTRY/EXIT pair of points neither of which will be considered to
  // be on the edge, because each is composed of two pixel planes and
  // one tet face.  This will result in two unpaired endpoints on two
  // different faces in virtually the same location.  We need to
  // detect and merge these points so that they're on the tet edge.
  
  // This only needs to be done for faces that aren't coincident with
  // pixel planes, because the facets on the pixel planes have already
  // been found.

  // looseEndCatalog[f][e] is a LooseEndMap for edge e of face f.  It
  // maps parametric positions along the edge to the
  // FaceEdgeIntersection at that point.
  std::vector<std::vector<LooseEndMap>>
    looseEndCatalog(NUM_TET_FACES,
		    std::vector<LooseEndMap>(NUM_TET_FACE_EDGES));

  std::vector<StrandedPoint> strandedPoints;

  // Loop over all faces that aren't also pixel planes.
  for(unsigned int face=0; face<NUM_TET_FACES; face++) {
    if(coincidentPixelPlanes[face] == nullptr) {

#ifdef DEBUG
      verboseface = verboseFace_(verbosecategory, face);
#endif // DEBUG
    
      FaceFacet &facet = faceFacets[face];
      std::vector<LooseEndMap> &looseEnds = looseEndCatalog[face];
	    
#ifdef DEBUG
      if(verboseface) {
	oofcerr << "HomogeneityTet::findFaceFacets: looking for loose ends"
		<< " on face " << face << std::endl;
      }
      OOFcerrIndent indent(2);
#endif	// DEBUG

#ifdef DEBUG
      if(verboseface) {
	oofcerr << "HomogeneityTet::findFaceFacets: starting checkEquiv loop"
		<< std::endl;
	if(!verify())
	  throw ErrProgrammingError("Verification failed!", __FILE__, __LINE__);
      }
#endif // DEBUG
      // Make sure equivalence classes are up to date.
      for(auto seg=facet.edges().begin(); seg!=facet.edges().end(); ++seg) {
      	checkEquiv((*seg)->startPt());
      	checkEquiv((*seg)->endPt());
      }

      unsigned int nsegs = facet.size();
      std::vector<FaceEdgeIntersection> startPoints;
      std::vector<FaceEdgeIntersection> endPoints;
      startPoints.reserve(nsegs);
      endPoints.reserve(nsegs);

      // Loop over segments in the face facet, storing their start and
      // end points.  *seg is a FaceFacetEdge*.
      for(auto seg=facet.edges().begin(); seg!=facet.edges().end(); ++seg) {
	// Construct FaceEdgeIntersection objects in-place.
	startPoints.emplace_back((*seg)->startPt(), *seg, true);
	endPoints.emplace_back((*seg)->endPt(), *seg, false);
      }
#ifdef DEBUG
      if(verboseface) {
	// At this point, fEdge hasn't been set in the
	// FaceEdgeIntersection objects, so don't be surprised by the
	// printed value.
	oofcerr << "HomogeneityTet::findFaceFacets: startPoints="
		<< std::endl;
	for(const auto &p: startPoints) {
	  OOFcerrIndent indent(2);
	  oofcerr << "HomogeneityTet::findFaceFacets: " << p << std::endl;
	}
	oofcerr << "HomogeneityTet::findFaceFacets: endPoints="
		<< std::endl;
	for(const auto &p: endPoints) {
	  OOFcerrIndent indent(2);
	  oofcerr << "HomogeneityTet::findFaceFacets: " << p << std::endl;
	}
      }
      if(!verify())
      	throw ErrProgrammingError("Verification failed!", __FILE__, __LINE__);
#endif // DEBUG
      // matchedStarts and matchedEnds indicate which segment start
      // and end points have been paired up.  The loose ones that
      // haven't been paired will be used to construct the missing
      // segments.
      std::vector<bool> matchedStarts(nsegs, false);
      std::vector<bool> matchedEnds(nsegs, false);
      for(unsigned int s=0; s<nsegs; s++) {
	for(unsigned int e=0; e<nsegs; e++) {
	  if(!matchedEnds[e] &&
	     startPoints[s].corner()->isEquivalent(endPoints[e].corner()))
	    {
	      matchedStarts[s] = true;
	      matchedEnds[e] = true;
#ifdef DEBUG
	      if(verboseface) {
		oofcerr << "HomogeneityTet::findFaceFacets: matched s="
			<< s << " e=" << e << " "
			<< *startPoints[s].corner() << " to "
			<< *endPoints[e].corner() << std::endl;
	      }
#endif // DEBUG
	      break;		// don't match this s with another e
	    }
	} // end loop over end points e
      }   // end loop over start points s
#ifdef DEBUG
      // if(!verify())
      // 	throw ErrProgrammingError("Verification failed!", __FILE__, __LINE__);
      if(verboseface) {
	// oofcerr << "HomogeneityTet::findFaceFacets: got matches" << std::endl;
	oofcerr << "HomogeneityTet::findFaceFacets: matchedStarts=";
	std::cerr << matchedStarts;
	oofcerr << std::endl;
	oofcerr << "HomogeneityTet::findFaceFacets:   matchedEnds=";
	std::cerr << matchedEnds;
	oofcerr << std::endl;
      }
#endif // DEBUG
      
      // All of the truly unmatched points must be on tet edges.  Sort
      // them by the edge and intersection position along the edge.
      // The ones that don't appear to be on edges now are "stranded",
      // but must be very close to edges and will be paired up later
      // to stranded points on other faces, which will locate them on
      // the edge between the two faces.

      for(unsigned int i=0; i<nsegs; i++) {
	if(!matchedStarts[i]) {
	  startPoints[i].findFaceEdge(face, this);
	  unsigned int edge = startPoints[i].faceEdge();
	  if(edge != NONE) {
	    looseEnds[edge].emplace(startPoints[i].edgePosition(),
				    startPoints[i]);
	  }
	  else {
	    strandedPoints.emplace_back(startPoints[i], face);
	  }
	}
	if(!matchedEnds[i]) {
	  endPoints[i].findFaceEdge(face, this);
	  unsigned int edge = endPoints[i].faceEdge();
	  if(edge != NONE)
	    looseEnds[edge].emplace(endPoints[i].edgePosition(),
				    endPoints[i]);
	  else {
	    strandedPoints.emplace_back(endPoints[i], face);
	  }
	}
      }
#ifdef DEBUG
      // if(!verify())
      // 	throw ErrProgrammingError("Verification failed!", __FILE__, __LINE__);
      if(verboseface) {
	oofcerr << "HomogeneityTet::findFaceFacets: loose ends, face="
		<< face << ":" << std::endl;
	for(unsigned int i=0; i<NUM_TET_FACE_EDGES; i++) {
	  OOFcerrIndent indent(2);
	  if(!looseEnds[i].empty())
	    for(auto l=looseEnds[i].begin(); l!=looseEnds[i].end(); ++l) {
	      oofcerr << "HomogeneityTet::findFaceFacets: edge=" << i
		      << " pos=" << (*l).first
		      << ": " << (*l).second << std::endl;
	    }
	  else
	    oofcerr << "HomogeneityTet::findFaceFacets: edge=" << i
		    << " (none)" << std::endl;
	}
      }
#endif // DEBUG

#ifdef DEBUG
      verboseface = false;
#endif // DEBUG
    }  // end if tet face is not a pixel plane
  } // end loop over faces

#ifdef DEBUG
  if(verbosecategory) {
    oofcerr << "HomogeneityTet::findFaceFacets: strandedPoints="
	    << std::endl;
    OOFcerrIndent indent(2);
    for(const StrandedPoint &pt : strandedPoints)
      oofcerr << "HomogeneityTet::findFaceFacets: face=" << pt.face
	      << " " << pt.feInt << std::endl;
  }
#endif // DEBUG

  // if(!verify())
  //   throw ErrProgrammingError("Verification failed!", __FILE__, __LINE__);
  
  // If there are stranded points, pair them up.  Stranded points come
  // from situations where a VSB segment passes nearly through a
  // polygon vertex in one pixel plane, leading to an entry/exit pair
  // that should be on a tet edge but isn't.  They can also arise when
  // the intersection line of two perpendicular pixel planes passes
  // through a tet edge.  In that case, there will be points on the
  // two planes but on different faces, and because each point is only
  // on one face, it won't be assigned to a tet edge.  TODO: This
  // comment is confusing.  The second case encompasses the first,
  // doesn't it?

  // If there are no other pixel planes creating segments connecting
  // to those points, they will be loose ends of the face facet, but
  // they're not on tet edges, so they can't be joined by adding facet
  // edges on the tet edges.  When the stranded points are paired,
  // each point of each pair must be on a different tet face, and
  // merging the pair produces a point on a tet edge (the edge shared
  // by the two faces).  The new merged point can be inserted into the
  // looseEndCatalog.

  
  // Stranded points that can't be matched, sorted by face
  std::vector<std::vector<StrandedPoint>> marooned(NUM_TET_FACES);
  
  std::vector<bool> matched(strandedPoints.size(), false);
  for(unsigned int i=0; i<strandedPoints.size(); i++) {
    if(!matched[i]) {
      const StrandedPoint &pt0 = strandedPoints[i];
      unsigned int best = NONE;
      double mindist2 = std::numeric_limits<double>::max();
      for(unsigned int j=i+1; j<strandedPoints.size(); j++) {
	const StrandedPoint &pt1 = strandedPoints[j];
	if(pt0.face != pt1.face &&
	   pt0.feInt.corner()->samePixelPlanes(pt1.feInt.corner()))
	  {
	    double dist2 = norm2(pt0.feInt.corner()->location3D() -
				 pt1.feInt.corner()->location3D());
	    if(dist2 < mindist2) {
	      mindist2 = dist2;
	      best = j;
	    }
	  }
      }	// end loop over possible matches j
      if(best != NONE) {
	matched[best] = true;
	matched[i] = true;
	const StrandedPoint &pt1 = strandedPoints[best];
	// The pixel plane intersections are stored in
	// FaceEdgeIntersection as generic PlaneIntersections, but in
	// this case we know that they're PixelPlaneIntersections.
	PixelPlaneIntersection *ppi0 =
	  dynamic_cast<PixelPlaneIntersection*>(pt0.feInt.corner());
	PixelPlaneIntersection *ppi1 =
	  dynamic_cast<PixelPlaneIntersection*>(pt1.feInt.corner());
	assert(ppi0 != nullptr && ppi1 != nullptr);
	PixelPlaneIntersectionNR *merged =
	  new MultiCornerIntersection(this, ppi0->referent(), ppi1->referent());
	mergeEquiv(ppi0->referent(), ppi1->referent(), merged);
	PlaneIntersection *newpt0 =
	  pt0.feInt.edge()->replacePoint(merged, this, pt0.feInt.start());
	PlaneIntersection *newpt1 =
	  pt1.feInt.edge()->replacePoint(merged, this, pt1.feInt.start());
	FaceEdgeIntersection fei0(newpt0, pt0.feInt.edge(), pt0.feInt.start());
	FaceEdgeIntersection fei1(newpt1, pt1.feInt.edge(), pt1.feInt.start());
	fei0.findFaceEdge(pt0.face, this);
	fei1.findFaceEdge(pt1.face, this);
	looseEndCatalog[pt0.face][fei0.faceEdge()].emplace(
						   fei0.edgePosition(), fei0);
	looseEndCatalog[pt1.face][fei1.faceEdge()].emplace(
						   fei1.edgePosition(), fei1);
	
	// The merged point isn't in a FacetEdge, so it won't be
	// automatically deleted.  Store it for later deletion.
	extraPoints.insert(merged);
#ifdef DEBUG
	if(verbosecategory) {
	  oofcerr << "HomogeneityTet::findFaceFacets: matched stranded points:"
		  << std::endl;
	  OOFcerrIndent indent(2);
	  oofcerr << "HomogeneityTet::findFaceFacets: pt0->feInt=" << pt0.feInt
		  << std::endl;
	  oofcerr << "HomogeneityTet::findFaceFacets: pt1->feInt=" << pt1.feInt
		  << std::endl;
	  oofcerr << "HomogeneityTet::findFaceFacets: fei0=" << fei0
		  << std::endl;
	  oofcerr << "HomogeneityTet::findFaceFacets: fei1=" << fei1
		  << std::endl;
	}
#endif // DEBUG
      }	// end if best is not NONE
      else {
	marooned[pt0.face].push_back(pt0);
#ifdef DEBUG
	if(verbosecategory)
	  oofcerr << "HomogeneityTet::findFaceFacets: marooned point! "
		  << *pt0.feInt << std::endl;
#endif // DEBUG
      }
    }	// end if point i hasn't been matched
  }	// end loop over stranded points i

  // Join the unmatched points in each FaceFacet.  This only needs to
  // be done for faces that aren't coincident with pixel planes,
  // because the facets on the pixel planes have already been found.

  // if(!verify())
  //   throw ErrProgrammingError("Verification failed!", __FILE__, __LINE__);

  for(unsigned int face=0; face<NUM_TET_FACES; face++) {
#ifdef DEBUG
    verboseface = verboseFace_(verbosecategory, face);
#endif // DEBUG
    FaceFacet &facet = faceFacets[face];
    if(coincidentPixelPlanes[face] == nullptr) { // face is not a pixel plane
      std::vector<LooseEndMap> &looseEnds = looseEndCatalog[face];
      Coord3D faceNormal = faceAreaVectors[face]; // not unit vector

      // Put any marooned points onto the closest edge.
      for(StrandedPoint &sp : marooned[face]) {
	sp.feInt.forceOntoEdge(sp.face, this);
	unsigned int edge = sp.feInt.faceEdge();
	looseEnds[edge].emplace(sp.feInt.edgePosition(), sp.feInt);
      }

#ifdef DEBUG
      if(verboseface) {
	oofcerr << "HomogeneityTet::findFaceFacets: before coincidence check, "
		<< "loose ends, face=" << face << ":" << std::endl;
	OOFcerrIndent indent(4);
	for(unsigned int i=0; i<NUM_TET_FACE_EDGES; i++) {
	  printLooseEnds(i, looseEnds[i]);
	}
      }
#endif // DEBUG

      
      // Find the existing facet edges that lie on the tet edges.
      // (TODO: Can this be done more efficiently earlier, perhaps
      // during the getEdgesOnFaces stage? Possibly not, because the
      // resolution of stranded and marooned points moves some points
      // onto edges.)
#ifdef DEBUG
      if(verboseface)
	oofcerr << "HomogeneityTet::findFaceFacets: looking for edge edges"
		<< std::endl;
#endif // DEBUG
      std::vector<FaceFacetEdgeSet> edgeEdges(NUM_TET_FACE_EDGES);
      for(FaceFacetEdge *edge : facet.edges()) {
	unsigned int faceEdge = edge->findFaceEdge(face, this);
	if(faceEdge != NONE) {
	  edgeEdges[faceEdge].insert(edge);
#ifdef DEBUG
	  if(verboseface) {
	    OOFcerrIndent indnt(2);
	    oofcerr << "HomogeneityTet::findFaceFacets: found edgeEdge, "
		    << "faceEdge=" << faceEdge << ", edge=" << *edge
		    << std::endl;
	  }
#endif // DEBUG
	}
      }

      // Look for near coincidences.  These are a problem if round-off
      // error has perturbed the edge positions, and a loose end
      // that's supposed to coincide with a loose start has an
      // edgePosition that's slightly after the start.  But first,
      // remove exact coincidences to simplify the near coincidence
      // check.  TODO: This comment is out of place.
      
      for(unsigned int e=0; e<NUM_TET_FACE_EDGES; e++) {
#ifdef DEBUG
	if(verboseface)
	  oofcerr
	    << "HomogeneityTet::findFaceFacets: looking for coincidences, cat "
	    << cat << " face " << face << " edge " << e << std::endl;
	OOFcerrIndent indent(2);
#endif // DEBUG
	if(looseEnds[e].size() > 1) {
	  // Coincidence check part 1.  If more than one segment
	  // intersects at *exactly* the same point on the edge of a
	  // face, throw out as many stop/start pairs as possible.
	  LooseEndMap &lem = looseEnds[e];
	  LooseEndMap::iterator x = lem.begin();
	  while(x != lem.end()) {
	    double t = (*x).first;	   // parametric coord of intersection
	    unsigned int n = lem.count(t); // no. of intersections at t
	    if(n > 1) {
	      auto range = lem.equal_range(t);

	      // Merge all of the equivalence classes of the coincident points
	      LooseEndMap::iterator x0 = range.first;
	      LooseEndMap::iterator xx = x0;
	      xx++;
	      IsecEquivalenceClass *eq0 = (*x0).second.corner()->equivalence();
	      for(; xx!=range.second; ++xx) {
		if(!(*x0).second.corner()->isEquivalent((*xx).second.corner())) {
		  IsecEquivalenceClass *eq1 =
		    (*xx).second.corner()->equivalence();
#ifdef DEBUG
		  if(verboseface) {
		    oofcerr << "HomogeneityTet::findFaceFacets: "
			    << "merging equivalence classes in coincidence 1"
			    << std::endl;
		    OOFcerrIndent indent(2);
		    oofcerr << "HomogeneityTet::findFaceFacets: eq0=" << *eq0
			    << std::endl;
		    oofcerr << "HomogeneityTet::findFaceFacets: eq1=" << *eq1
			    << std::endl;
		  }
#endif // DEBUG
		  mergeEquiv((*x0).second.corner(), (*xx).second.corner());
		}
	      }
	      
	      int nstartdiff = 0; // # of starts minus # of stops at this t
	      for(LooseEndMap::iterator y=range.first; y!=range.second; ++y) {
		if((*y).second.start())
		  nstartdiff++;
		else
		  nstartdiff--;
	      }
#ifdef DEBUG
	      if(verboseface)
		oofcerr << "HomogeneityTet::findFaceFacets: nstartdiff="
			<< nstartdiff << std::endl;
#endif // DEBUG
	      if(nstartdiff == 0) {
		// There are as many starts as stops.  They're all irrelevant.
		lem.erase(range.first, range.second);
	      }
	      else {
		// nstartdiff != 0
		std::vector<LooseEndMap::iterator> deleteThese;
		if(nstartdiff > 0) {
		  // Delete all but nstartdiff starts.
		  int kept = 0;
		  for(LooseEndMap::iterator y=range.first; y!=range.second; ++y)
		    {
		      if(kept >= nstartdiff || !(*y).second.start())
			deleteThese.push_back(y);
		      else
			kept++;
		    }
		}
		else if(nstartdiff < 0) {
		  // Delete all but -nstartdiff stops.
		  int kept = 0;
		  for(LooseEndMap::iterator y=range.first; y!=range.second; ++y)
		    {
		      if(kept >= -nstartdiff || (*y).second.start())
			deleteThese.push_back(y);
		      else
			kept++;
		    }
		}
#ifdef DEBUG
		if(verboseface && !deleteThese.empty())
		  oofcerr << "HomogeneityTet::findFaceFacets: deleting "
			  << deleteThese.size() << " loose ends" << std::endl;
#endif // DEBUG
		  
		for(auto y=deleteThese.rbegin(); y!=deleteThese.rend(); ++y)
		  lem.erase(*y);
	      }	// end if nstartdiff != 0
	      x = range.second;
	    } // end if there is more than one intersection at point t
	    else {
	      ++x;
	    }
	  } // end while loop over loose ends on edge e
	} // end if there are more than one loose ends on edge e
#ifdef DEBUG
	if(verboseface) {
	  oofcerr << "HomogeneityTet::findFaceFacets:"
		  << " after 1st coincidence check, face=" << face
		  << ", edge=" << e << ", loose ends=" << std::endl;
	  OOFcerrIndent indent(4);
	  printLooseEnds(e, looseEnds[e]);
	}
#endif // DEBUG
	
	// Coincidence check part 2.  Look for intersection points on
	// the face edges that are close to each other but not exactly
	// equivalent, and make sure that the facet segments that meet
	// the face edges there don't cross.  If they do, the
	// intersection points must be misordered by roundoff, and
	// should actually be identical.
	if(looseEnds[e].size() > 1) {
	  // Loop over loose ends on the edge.  The loop isn't simple
	  // because loose ends are removed by pairs, so the iterator
	  // has to increase by 2 and the stop criterion is that
	  // either the iterator (x) or its successor (xnext) points
	  // to the end of the array.
	  LooseEndMap::iterator x = looseEnds[e].begin();
	  LooseEndMap::iterator xnext = x;
	  xnext++;
	  unsigned int tetEdge = CSkeletonElement::faceEdges[face][e];
	  bool done = false;
	  while(!done) {
	    double dt = ((*xnext).second.edgePosition() -
			 (*x).second.edgePosition()) * edgeLengths[tetEdge];
#ifdef DEBUG
	    if(verboseface) {
	      oofcerr << "HomogeneityTet::findFaceFacets:     x=" << (*x).second
		      << std::endl;
	      oofcerr << "HomogeneityTet::findFaceFacets: xnext="
		      << (*xnext).second << std::endl;
	      oofcerr << "HomogeneityTet::findFaceFacets:    dt=" << dt
		      << std::endl;
	      oofcerr << "HomogeneityTet::findFaceFacets: alphas x="
		      << (*x).first << " xnext=" << (*xnext).first
		      << " diff=" << (*xnext).first - (*x).first
		      << std::endl;
	    }
#endif // DEBUG
	    bool equiv =
	      (*x).second.corner()->isEquivalent((*xnext).second.corner());
	    if(!equiv && dt < 0.5) {
	      // The two points are within a half a pixel of each
	      // other and can potentially coincide.
	      if((*x).second.start() != (*xnext).second.start()) {
#ifdef DEBUG
		if(verboseface) {
		  oofcerr << "HomogeneityTet::findFaceFacets: checking... "
			  << std::endl;
		}
		OOFcerrIndent indnt(2);
#endif // DEBUG
		// x is the start (end) of a facet segment that lies
		// in the face and has an endpoint on an edge of the
		// face, and xnext is the end (start) of another such
		// facet segment. xnext's endpoint is just past x's on
		// the facet edge (because xnext is after x in the
		// LooseEndMap).

		// If round-off error has put the edge intersections
		// in the wrong order, then the segments will
		// intersect.  Since facet segments can't cross, we
		// can tell if the ordering is incorrect.

		// a0 and b0 are the endpoints of x and xnext that lie
		// on the facet edge, irrespective of the directions
		// of the segments.  a1 and b1 are the other endpoints
		// of the segments.
		Coord3D a0, a1, b0, b1;
		const FaceFacetEdge *edgeA = (*x).second.edge();
		const FaceFacetEdge *edgeB = (*xnext).second.edge();
// #ifdef DEBUG
// 		if(verboseface) {
// 		  oofcerr << "HomogeneityTet::findFaceFacets: edgeA="
// 			  << *edgeA << std::endl;
// 		  oofcerr << "HomogeneityTet::findFaceFacets: edgeB="
// 			  << *edgeB << std::endl;
// 		}
// #endif // DEBUG
		if((*x).second.start()) {
		  a0 = edgeA->startPt()->location3D();
		  b0 = edgeB->endPt()->location3D();
		  a1 = edgeA->endPt()->location3D();
		  b1 = edgeB->startPt()->location3D();
		}
		else {
		  a1 = edgeA->startPt()->location3D();
		  b1 = edgeB->endPt()->location3D();
		  a0 = edgeA->endPt()->location3D();
		  b0 = edgeB->startPt()->location3D();
		}
// #ifdef DEBUG
// 		if(verboseface) {
// 		  oofcerr << "HomogeneityTet::findFaceFacets: normal="
// 			  << faceNormal << std::endl;
// 		  oofcerr << "HomogeneityTet::findFaceFacets: a0=" << a0
// 			  << " a1=" << a1 << " b0=" << b0 << " b1=" << b1
// 			  << std::endl;
// 		  oofcerr << "HomogeneityTet::findFaceFacets: a1-a0=" << a1-a0
// 			  << " b1-a0=" << b1-a0
// 			  << " cross=" << cross(a1-a0, b1-a0)
// 			  << std::endl;
// 		  oofcerr << "HomogeneityTet::findFaceFacets: b1-b0=" << b1-b0
// 			  << " a1-b0=" << a1-b0
// 			  << " cross=" << cross(b1-b0, a1-b0)
// 			  << std::endl;
// 		  oofcerr << "HomogeneityTet::findFaceFacets: dotA="
// 			  << dot(cross(a1-a0, b1-a0), faceNormal)
// 			  << " dotB=" << dot(cross(b1-b0, a1-b0), faceNormal)
// 			  << std::endl;
// 		}
// #endif // DEBUG
		// We know that b0 lies to the right of (a0,a1) and
		// that a0 lies to the left of (b0,b1).  If the
		// segments cross, then b1 must lie to the left of
		// (a0,a1) and a1 to the right of (b0,b1), which is
		// what these cross products check:
		equiv = (dot(cross(a1-a0, b1-a0), faceNormal) >= 0.0 ||
			 dot(cross(b1-b0, a1-b0), faceNormal) <= 0.0);
	      } // end if x is start and xnext is an end, or vice versa
	    }	// end if the points are within a pixel of each other
	    if(equiv) {
	      // The points are either identical, or are in the wrong
	      // order, so they must actually coincide but differ by
	      // roundoff error.  They're not really loose ends.
	      // Remove them from the list.
#ifdef DEBUG
	      if(verboseface) {
		oofcerr << "HomogeneityTet::findFaceFacets:"
			<< " removing coincidence" << std::endl;
	      }
#endif // DEBUG
	      LooseEndMap::iterator xtemp = xnext;
	      ++xtemp;
	      mergeEquiv((*x).second.corner(), (*xnext).second.corner());
	      looseEnds[e].erase(x);
	      looseEnds[e].erase(xnext);
	      x = xtemp;
	      if(xtemp == looseEnds[e].end()) 
		done = true;
	      else {
		xnext = x;
		xnext++;
		done = (xnext == looseEnds[e].end());
	      }
	    }
	    else {
#ifdef DEBUG
	      if(verboseface)
		oofcerr << "HomogeneityTet::findFaceFacets:"
			<< " not removing coincidence" << std::endl;
#endif // DEBUG
	      x = xnext;
	      xnext++;
	      done = (xnext == looseEnds[e].end());
	    }
	  } // end loop over loose ends x
	} // end if there is more than one loose end on the edge

	// Occupied segment check:
	// Remove pairs of points on an edge that is already occupied
	// by another segment.  This can happen in situations like
	// this:
	/*
	  ....c          B
	  .....\        /...
	  ......\      /.....    Points marked by capital letters are
          .......\    /......    starts and lower case are stops.
          ........\  /........
	  A--------Cb----------a 
	*/
	// C and b should be identical and should be on the edge A-a,
	// but roundoff error may make C come before b.  In that case,
	// C and b are loose ends, but the order of starts and stops
	// along the edge is start-start-stop-stop, and the points
	// can't be paired. Note that A and a need not be loose ends.
	// Also, b must not be joined to C counterclockwise, the way
	// stops and starts are normally joined.  If roundoff has put
	// Cb in the other order (bC), then the coincidence detector
	// will remove them.
#ifdef DEBUG
	if(verboseface) {
	  oofcerr << "HomogeneityTet::findFaceFacets: "
		  << "beginning occupied segment check, e=" << e
		  << " face=" << face << " cat=" << cat << std::endl;
	}
#endif // DEBUG
	if(looseEnds[e].size() >= 2 && !edgeEdges[e].empty()) {
	  LooseEndMap::iterator x = looseEnds[e].begin();
	  LooseEndMap::iterator xprev = x;
	  x++;
	  while(x != looseEnds[e].end()) {
	    bool found = false;
	    double dt = (*x).first - (*xprev).first; // parametric distance

	    if(dt*edgeLengths[e] < 0.5) {
	      // Points are within half a pixel of each other
	      if((*xprev).second.start() && !(*x).second.start()) {
		// It's a start-end pair.
		double tC = (*xprev).first; // parametric position of pt C
		double tb = (*x).first;	    // parametric position of pt b
		for(FaceFacetEdge *edge : edgeEdges[e]) {
		  if(!edge->startPt()->isEquivalent((*xprev).second.corner()) &&
		     !edge->endPt()->isEquivalent((*x).second.corner()))
		    {
		      double tA =
			faceEdgeCoord(edge->startPt()->baryCoord(this), face,e);
		      double ta =
			faceEdgeCoord(edge->endPt()->baryCoord(this), face, e);
		      // TODO: Should tA and ta be cached?
		      if(tA < tC && tC < ta && tA < tb && tb < ta) {
			//  Cb lies inside Aa on the edge of the tet face.
			//  Remove x and xprev (ie C and b) from the loose
			//  end map, and set up the next iteration.
			LooseEndMap::iterator next = x;
			next++;
#ifdef DEBUG
			if(verboseface) {
			  oofcerr << "HomogeneityTet::findFaceFacets: tA="
				  << tA << " tC=" << tC << "tC-tA=" << tC-tA
				  << " ta=" << ta << " tb=" << tb
				  << "ta-tb=" << ta-tb << std::endl;
			  oofcerr << "HomogeneityTet::findFaceFacets: "
				  << "occupied edge check deleting intersections"
				  << std::endl;
			  OOFcerrIndent indent(2);
			  oofcerr << "HomogeneityTet::findFaceFacets: xprev="
				  << (*xprev).second << std::endl;
			  oofcerr << "HomogeneityTet::findFaceFacets:     x="
				  << (*x).second << std::endl;
			}
#endif // DEBUG
			looseEnds[e].erase(x);
			looseEnds[e].erase(xprev);
			xprev = next;
			x = next;
			if(x != looseEnds[e].end())
			  x++;
			found = true;
		      }	// end if start and stop are within the segment
		    } // end if start and stop aren't endpoints of the segment
		}
	      }	// end if points are a start-stop pair
	    } // end if points are close
	    if(!found) {
	      xprev = x;
	      x++;
	    }
	  } // end loop over loose ends x
	} // end if there are at least 2 loose ends and a collinear segment
	
      }   // end loop over face edges e
// #ifdef DEBUG
//       if(verbosecategory)
// 	oofcerr << "HomogeneityTet::findFaceFacets: coincidence check done "
// 		<< std::endl;
// #endif	// DEBUG

#ifdef DEBUG
      // if(!verify())
      // 	throw ErrProgrammingError("Verification failed!", __FILE__, __LINE__);
      if(verboseface) {
	oofcerr << "HomogeneityTet::findFaceFacets: after coincidence checks, "
		<< "loose ends, face=" << face << ":" << std::endl;
	OOFcerrIndent indent(4);
	for(unsigned int i=0; i<NUM_TET_FACE_EDGES; i++) {
	  printLooseEnds(i, looseEnds[i]);
	}
      }
#endif // DEBUG

#ifdef DEBUG
      // Check that the number of loose starts and ends match
      int nStarts = 0;
      int nEnds = 0;
      for(unsigned int e=0; e<NUM_TET_FACE_EDGES; e++) {
	LooseEndMap &lem = looseEnds[e];
	for(LooseEndMap::const_iterator i=lem.begin(); i!=lem.end(); ++i) {
	  if((*i).second.start())
	    nStarts++;
	  else
	    nEnds++;
	}
      }
      if(nStarts != nEnds)
	throw ErrProgrammingError("Loose end mismatch!", __FILE__, __LINE__);
#endif // DEBUG
      
#ifdef CLEAN_UP_LOOSE_ENDS
      if(nStarts != nEnds) {
	// This can happen if a coincidence was resolved on one pixel
	// plane but not on another. In that case there can be two
	// starts (or ends) at nearly identical positions, one of
	// which should be removed.
#ifdef DEBUG
	if(verboseface) {
	  oofcerr << "HomogeneityTet::findFaceFacets:"
		  <<" resolving loose end mismatch" << std::endl;
	  oofcerr << "HomogeneityTet::findFaceFacets: looseEnds=" << std::endl;
	  OOFcerrIndent indent(2);
	  for(unsigned int e=0; e<looseEnds.size(); e++) {
	    for(auto lem=looseEnds[e].begin(); lem!=looseEnds[e].end(); ++lem) {
	      oofcerr << "HomogeneityTet:findFaceFacets: e=" << e
		      << " d=" << (*lem).first
		      << " " << (*lem).second << std::endl;
	    }
	  }
	}
#endif // DEBUG
	if(nStarts > nEnds) {
	  while(nStarts > nEnds) {
	    if(cleanUpLooseEnds(looseEnds, true))
	      --nStarts;
	    else {
	      oofcerr << "HomogeneityTet::findFaceFacets: "
		      << "failed to resolve loose end mismatch, cat=" << cat
		      << " face=" << face << std::endl;
	      throw ErrProgrammingError("HomogeneityTet::findFaceFacets: cleanUpLooseEnds failed! start=true",
					__FILE__, __LINE__);
	    }
	  } // end while nStarts > nEnds
	}   // end if nStarts > nEnds
	else  {
	  // nStarts < nEnds
	  while(nEnds > nStarts) {
	    if(cleanUpLooseEnds(looseEnds, false))
	      --nEnds;
	    else {
	      oofcerr << "HomogeneityTet::findFaceFacets: "
		      << "failed to resolve loose end mismatch, cat=" << cat
		      << " face=" << face << std::endl;
	      throw ErrProgrammingError("HomogeneityTet::findFaceFacets: cleanUpLooseEnds failed! start=false",
					__FILE__, __LINE__);
	    }
	  } // end while nEnds > nStarts
	} // end if nStarts < nEnds
      }	// end if nStarts != nEnds

#ifdef DEBUG
      if(verboseface) {
	oofcerr << "HomogeneityTet::findFaceFacets: after cleanUpLooseEnds, "
		<< "loose ends, face=" << face << ":" << std::endl;
	OOFcerrIndent indent(4);
	for(unsigned int i=0; i<NUM_TET_FACE_EDGES; i++) {
	  printLooseEnds(i, looseEnds[i]);
	}
      }
#endif // DEBUG
#endif // CLEAN_UP_LOOSE_ENDS
      
      // Create the missing segments. Missing segments start at a
      // loose end and end at a loose start.
#ifdef DEBUG
      if(verboseface) {
	oofcerr << "HomogeneityTet::findFaceFacets: creating missing segments"
		<< " on face " << face << std::endl;
      }
#endif // DEBUG
	
      // If the first intersection found is a start, it's stored in
      // firstStart.
      const FaceEdgeIntersection *firstStart = nullptr;
      // currentEnd is non-null if we've found an end are looking
      // for a start.
      const FaceEdgeIntersection *currentEnd = nullptr;
	
      for(unsigned int e=0; e<NUM_TET_FACE_EDGES; e++) {
	const LooseEndMap &lem = looseEnds[e];
	for(LooseEndMap::const_iterator le=00lem.begin(); le!=lem.end(); ++le) {
	  if(!(*le).second.start()) {
	    // This point is a loose end, so it's the start of a new
	    // segment.
	    if(currentEnd != nullptr) {
	      oofcerr << "HomogeneityTet::findFaceFacets: "
		      << "two consecutive ends on face " << face 
		      << " category=" << cat << std::endl;
	      oofcerr << "HomogeneityTet::findFaceFacets: currentEnd="
		      << *currentEnd << std::endl;
	      oofcerr << "HomogeneityTet::findFaceFacets: new point="
		      << (*le).second << std::endl;
	      throw ErrProgrammingError(
		"Loose end matching failed!  Found two consecutive ends.",
		__FILE__, __LINE__);
	    }
	    currentEnd = &(*le).second;
	  } // end if this is a loose end
	  else {
	    // This point is a loose start, so it's the end of a new segment.
	    if(currentEnd == nullptr) {
	      // We haven't seen the end for this start. Save it for later.
	      if(firstStart == nullptr)
		firstStart = &(*le).second;
	      else {
		oofcerr << "HomogeneityTet::findFaceFacets: "
			<< "two consecutive starts on face " << face 
			<< " category=" << cat << std::endl;
		oofcerr << "HomogeneityTet::findFaceFacets: firstStart="
			<< *firstStart << std::endl;
		oofcerr << "HomogeneityTet::findFaceFacets: new point="
			<< (*le).second << std::endl;
		throw ErrProgrammingError(
		  "Loose end matching failed!  Found two consecutive starts.",
		  __FILE__, __LINE__);
	      }
	    } // end if currentEnd is null
	    else {
	      facet.addFaceEdges(currentEnd, &(*le).second, this);
	      currentEnd = nullptr;
	    } // end if currentEnd is not null
	  }   // end if this point is a loose start

	} // end loop over loose ends on edge
      }   // end loop over edges e of the face

      // If we get here with a non-null currentEnd, we must have
      // started in the middle of a segment, and firstStart must also
      // be non-null.
      if(currentEnd != nullptr) {
	if(firstStart == nullptr)
	  throw ErrProgrammingError("Missing start!", __FILE__, __LINE__);
	facet.addFaceEdges(currentEnd, firstStart, this);
      }

      // Remove pairs of equal and opposite segments.
      facet.removeOpposingEdges();

#ifdef DEBUG
      if(verboseface)
	oofcerr << "HomogeneityTet::findFaceFacets: face=" << face
		<< " before fixNonPositiveArea, facet=" << facet << std::endl;
#endif // DEBUG
      
      // Fix situations that can cause the area to be zero or negative.
      facet.fixNonPositiveArea(this, cat);
      
#ifdef DEBUG
      if(verboseface) {
	oofcerr << "HomogeneityTet::findFaceFacets: face=" << face
		<< " after fixNonPositiveArea, facet=" << facet << std::endl;
      }
#endif	// DEBUG
      
    } // end if face is not coincident with a pixel plane
    // if(!verify())
    //   throw ErrProgrammingError("Verification failed!", __FILE__, __LINE__);
    
    // #ifdef DEBUG
    //       else {
    // 	if(verbosecategory)
    // 	  oofcerr << "HomogeneityTet::findFaceFacets: skipping face on pixel plane"
    // 		  << std::endl;
    //       }
    // #endif // DEBUG
#ifdef DEBUG
    verboseface = false;
#endif // DEBUG
  }   // end loop over faces

#ifdef DEBUG
  if(verbosecategory) {
    oofcerr << "HomogeneityTet::findFaceFacets: returning.  Face facets are:"
	    << std::endl;
    OOFcerrIndent indent(2);
    for(unsigned int face=0; face<NUM_TET_FACES; face++) {
      if(verboseFace_(verbosecategory, face)) {
	if(coincidentPixelPlanes[face] == nullptr) {
	  FaceFacet &facet = faceFacets[face];
	  oofcerr << "HomogeneityTet::findFaceFacets: " << facet << std::endl;
	  facet.dump("facefacet", cat);
	}
      }
    }
  }
#endif // DEBUG

#ifdef DEBUG
  verbosecategory = false;
#endif	// DEBUG
  return faceFacets;
} // HomogeneityTet::findFaceFacetsOLD

#endif // FINDFACEFACETS_OLD
