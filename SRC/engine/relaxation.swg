 // -*-  C++  -*-

#ifndef RELAXATION_SWG
#define RELAXATION_SWG



%module relaxation

%include "common/typemaps.swg"
%include "engine/typemaps.swg"
%extern "engine/cskeletonmodifier.swg"
%{
  #include <oofconfig.h>
  #include "engine/relaxation.h" 
%}

%pragma(python) include="engine/relaxation.spy"
   
%pragma(python) code="from ooflib.SWIG.engine.cskeletonmodifier import CSkeletonModifierPtr, CSkeletonModifierBasePtr"
   


class Relax : public CSkeletonModifier {
  public:
  Relax(double alpha, double gamma, int iterations, RescaleSettings* settings);
  double getAlpha();
  double getGamma();
  double getIterations();
  bool getRescaleAllowed();
  double getDisplacementScaleFactor();
  int getMaxRescales();
  int getRescaleCounter();
  double getDisplacementMultiplier();
  bool updateNodePositionsC(CDeputySkeleton* skeleton, FEMesh* mesh);
  
};

class RescaleSettings {
protected:
  bool rescaleEnabled;
public:
  RescaleSettings(bool canRescale) {}
  bool getRescaleEnabled();
};

class YesRescale : public RescaleSettings {
protected:
  const double rescaleRatio;
  const int maxRescales;
public:
  YesRescale(double ratio, int max);
  const double getRescaleRatio();
  const int getMaxRescales();
};

class NoRescale : public RescaleSettings {
public:
  NoRescale();
};



#endif //RELAXATION_SWG
