#include <oofconfig.h>


#ifndef RELAXATION_H
#define RELAXATION_H

#include "engine/cskeletonmodifier.h" 

//Forward declaration so that Relax constructor prototype can use this class
class RescaleSettings;


class Relax : public CSkeletonModifier {
protected:

  //set by user
  double alpha; //relative emphasis of shape or homogeneity
  double gamma; //node mobility
  int iterations; 
  RescaleSettings* settings; //options for automatic rescaling

  //set in constructor
  bool rescaleAllowed; //indirectly set by settings
  double displacementScaleFactor; //indirectly set by settings
  int maxRescales; //indirectly set by settings
  double displacementMultiplier; //initialized to 1
  int rescaleCounter; //how many rescales have occurred

  /*
  List of other Relax member variables that aren't declared here
  because they are only used in Python (relaxation.spy)
  
  materialName --- string, gets set to boneMarrow
  count --- int, how many iterations have occurred
  rescaleCounter --- int, how many rescales have occurred
  canRelaxFurther --- bool, can we continue relaxing?
  solverConverged --- bool, flag that indicates problems with the solver
  meshName --- string, gets a unique name based on thread and skeleton path
  
  skelRelRate --- copy of skeleton relaxation rate property
  stiffness --- copy of isotropic elasticity property
  leftBoundaryCondition --- DirichletBC
  rightBoundaryCondition --- DirichletBC
  topBoundaryCondition --- DirichletBC
  bottomBoundaryCondition --- DirichletBC
  frontBoundaryCondition --- DirichletBC
  backBoundaryCondition --- DirichletBC
  */
  
 public:
  //Creates an instance of the Relax object
  Relax(double alpha, double gamma, int iterations, RescaleSettings* settings);
  virtual ~Relax();

  //Creates and returns a deputy copy of the current skeleton
  CSkeletonBase* apply(CSkeletonBase* skeleton);

  //Core loop for updating the nodes based on the displacement data
  bool updateNodePositionsC(CDeputySkeleton* skeleton, FEMesh* mesh);

  //Getters so that python methods can access C++ member variables
  double getAlpha() {return alpha;}
  double getGamma() {return gamma;}
  int getIterations() {return iterations;}
  bool getRescaleAllowed() {return rescaleAllowed;}
  double getDisplacementScaleFactor() {return displacementScaleFactor;}
  int getMaxRescales() {return maxRescales;}
  int getRescaleCounter() {return rescaleCounter;}
  double getDisplacementMultiplier() {return displacementMultiplier;}
  
};



/******************************************************/
//Helper classes for presenting the rescaling options in the GUI

//Base class for rescale settings
class RescaleSettings {
 protected:
  bool rescaleEnabled;
 public:
 RescaleSettings(bool canRescale) : rescaleEnabled(canRescale) {}
  virtual ~RescaleSettings() {};
  bool getRescaleEnabled() const {return rescaleEnabled;}
};

//Class that represents enabling rescale
//Has additional member data for rescale ratio and max rescales
class YesRescale : public RescaleSettings {
 protected:
  double rescaleRatio;
  int maxRescales;
 public:
 YesRescale(double ratio, int max) : RescaleSettings(true),
    rescaleRatio(ratio), maxRescales(max) {}
  double getRescaleRatio() const {return rescaleRatio;}
  int getMaxRescales() const {return maxRescales;}
};

//Class that represents disabling rescale
class NoRescale : public RescaleSettings {
 public:
 NoRescale() : RescaleSettings(false) {}
};


#endif //RELAXATION_H
