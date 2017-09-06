// -*- C++ -*-

#include "common/coord.h" 
#include "engine/femesh.h"
#include "engine/cskeleton2.h" 
#include "engine/cskeletonelement.h"
#include "engine/element.h" 
#include "engine/node.h"
#include "engine/relaxation.h" 


//Relax constructor
//Sets alpha, gamma, iterations, and settings based on user input
//Initializes rescaleCounter to 0 and displacementMultiplier to 1
Relax::Relax(double alpha, double gamma, int iterations,
	     RescaleSettings* settings)
  :alpha(alpha), gamma(gamma),
   iterations(iterations),
   settings(settings),
   displacementMultiplier(1),
   rescaleCounter(0)
{
  //If rescaling is allowed, set relevant settings to user input
  //Otherwise, set them to zero because they won't be used 
  if (settings->getRescaleEnabled()) {
    rescaleAllowed = true;
    YesRescale* yes = dynamic_cast<YesRescale*>(settings);
    displacementScaleFactor = yes->getRescaleRatio();
    maxRescales = yes->getMaxRescales();
  } else {
    rescaleAllowed = false;
    displacementScaleFactor = 0;
    maxRescales = 0;
  }

}

//Destructor
Relax::~Relax() {}

//Apply function that all skeleton modifiers need
CSkeletonBase* Relax::apply(CSkeletonBase *skeleton){
  CSkeletonBase *copy = skeleton->deputyCopy();
  return copy;
}

//This is the core loop for moving nodes based on displacement data
//If illegal elements are produced and we can rescale, we move
//the nodes partway back toward their previous positions.
//If we cannot rescale, the nodes move all the way back
//to their previous positions
bool Relax::updateNodePositionsC(CDeputySkeleton* skeleton, FEMesh* mesh) {
  
  Field* displacement = Field::getField("Displacement");
  int numNodes = skeleton->nnodes();
  for (int i = 0; i < numNodes; i++) {
    //gets a specific skeleton node by index
    CSkeletonNode* node = skeleton->getNode(i);
    //finds a skeleton element that the node is part of
    CSkeletonElementVector neighbors;
    node->getElements(skeleton, neighbors);
    CSkeletonElement* skelel = neighbors[0];
    //finds the corresponding mesh element, then node
    Element* realel = mesh->getElement(skelel->getIndex());
    PointData* realnode =
      realel->getCornerFuncNode(skelel->getNodeIndexIntoList(node));
    //finds out how much the mesh node has been displaced
    double dx = displacement->value(mesh, realnode, 0);
    double dy = displacement->value(mesh, realnode, 1);
    double dz = displacement->value(mesh, realnode, 2);
    //moves skeleton node to match the displacement of the mesh node,
    //but includes a scaling factor if rescaling is enabled and nodes moved
    //too far on a previous iteration
    skeleton->moveNodeBy(node, displacementMultiplier*Coord(dx, dy, dz));
  }


  //Checking for and handling illegal elements that have formed

  //flag that tells wrapper function whether the skeleton became illegal
  bool skelBecameIllegal = false;
  //Repeat this process until the skeleton becomes legal
  //or we can no longer rescale
  skeleton->checkIllegality();
  while (skeleton->illegal()) {
    //If we cannot rescale, revert the nodes to previous positions and return
    //false to notify wrapper function that the skeleton became illegal
    if (!rescaleAllowed || rescaleCounter >= maxRescales) {
        for (int i = 0; i < numNodes; i++) {
	CSkeletonNode* node = skeleton->getNode(i);
	node->moveBack();
      }
      rescaleCounter++;
      return false;
    }

    //The rest of this function executes only if we can rescale

    //Set flag so that wrapper function knows that the skeleton became illegal
    skelBecameIllegal = true;   
    //Adjust displacement multiplier by the user-given ratio
    displacementMultiplier *= displacementScaleFactor;
    //Move back every node partway toward its prevous position
    for (int i = 0; i < numNodes; i++) {
      CSkeletonNode* node = skeleton->getNode(i);
      //This is equivalent to reverting the node to its previous position
      //and then doing
      //skeleton->moveNodeBy(node, displacementMultiplier*Coord(dx, dy, dz))
      node->moveBackScaled(1 - displacementScaleFactor);
    }
    rescaleCounter++;
    skeleton->checkIllegality();
  }

  //Returns true if skeleton was legal after the first node movement loop
  //Returns false if adjustments were needed to make the skeleton legal again
  return (!skelBecameIllegal);
   
}

