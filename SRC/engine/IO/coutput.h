// -*- C++ -*-
// $RCSfile: coutput.h,v $
// $Revision: 1.1.2.1 $
// $Author: langer $
// $Date: 2011/08/15 20:01:00 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef COUTPUT_H
#define COUTPUT_H

class Coutput;
class PositionSet;

#include "common/pythonexportable.h"
#include "engine/outputval.h"

#include <map>
#include <vector>

typedef std::vector<MasterCoord> PositionSet;
typedef std::map<const std::string, Coutput*> COutputDict;
typedef std::vector<OutputValue> OutputValVec;
typedef std::map<const std::string, OutputValVec*> OutputValSet;

class COutput : public PythonExportable<COutput> {
private:
  const std::string &name_;
  COutputDict inputs;
  static std::string modulename_;
public:
  COutput(const std::string &name);
  virtual ~COutput();
  
  void connect(const std::string &name, COutput* output);
  

  void evaluate(FEMesh *mesh,
		const std::vector<Element*> elements,
		const std::vector<PositionSet> *positions,
		OutputValVec *output) const;

  virtual void evaluate(FEMesh *mesh,
			const std::vector<Element*> elements,
			const std::vector<PositionSet> *positions,
			const OutputValSet &inputs,
			OutputValVec *output) const = 0;
};

#endif	// COUTPUT_H
