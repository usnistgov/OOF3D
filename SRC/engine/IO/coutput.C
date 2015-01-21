// -*- C++ -*-
// $RCSfile: coutput.C,v $
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

#include "engine/IO/coutput.h"

std::string COutput::modulename_("ooflib.SWIG.engine.IO.coutput");

COutput::COutput(const std::string &name)
  : name_:name
{}

COutput::~COutput() {
  for(COutputDict::iterator i=inputs.begin(); i<inputs.end(); ++i)
    delete i->second();
}

void COutput::connect(const std::string &name, COutput *output) {
  std::pair<COutputDict::iterator, bool> p
    = inputs.insert(COutputDict::value_type(name, output));
  assert(p.second());		// Check that insertion succeeded
				// (ie, name is unique).
}

void COutput::evaluate(FEMesh *mesh,
		       std::vector<Element*> elements,
		       std::vector<PositionSet> *positions,
		       OutputValVec *output)
  const 
{
  // Evaluate all inputs, storing their results in locally allocated
  // vectors in a dict keyed by input name.
  OutputValSet inputvals;
  for(COutputDict::const_iterator i=inputs.begin(); i<inputs.end(); ++i) {
    OutputValVec *ov = new OutputValVec;
    inputvals[i->first()] = ovv;
    ovv->reserve(output->size());
    i->second()->evaluate(mesh, elements, positions, ovv);
  }
  
  // Compute this COutput, storing results in output.
  evaluate(mesh, elements, positions, inputvals, output);
  
  // Delete vectors allocated in step 1.
  for(OutputValSet::iterator i=inputvals.begin(); i<inputvals.end(); ++i) {
    delete i->second();
  }
}
