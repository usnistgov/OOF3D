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

#include "common/latticesystem.h"
#include "common/ooferror.h"
#include <map>

typedef std::map<std::string, LatticeSymmetry> LatticeSymmetryMap;

static LatticeSymmetryMap symMap;

void addLatticeSymmetryMatrix(const std::string &symbol,
			      const SmallMatrix *matrix)
{
  LatticeSymmetryMap::iterator iter = symMap.find(symbol);
  if(iter == symMap.end()) {
    // std::cerr << "addLatticeSymmetryMatrix: adding symbol " << symbol
    //  	      << std::endl;
    auto insert = symMap.emplace(symbol, LatticeSymmetry{});
    iter = insert.first;
  }
  LatticeSymmetry &ls = iter->second;
  // std::cerr << "addLatticeSymmetryMatrix: " << symbol << " "
  // 	    << *matrix << " det=" << matrix->determinant() << std::endl;
  ls.addMatrix(matrix);
}

const LatticeSymmetry *getLatticeSymmetry(const std::string &symbol) {
  LatticeSymmetryMap::const_iterator iter = symMap.find(symbol);
#ifdef DEBUG
  if(iter == symMap.end())
    std::cerr << "getLatticeSymmetry: failed to find symbol " << symbol
	      << std::endl;
#endif // DEBUG
  assert(iter != symMap.end());
  return &iter->second;
}

