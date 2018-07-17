// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

// Simple system for holding element-specific data during flux and
// equation computations.  Has SmallMatrix slots for the various time
// derivatives.  It's in its own file because both fluxes and
// equations need it.  If it stays small and trivial, it could be
// moved.

// TODO 3.1: Have two derived classes, one for fluxes and one for
// equations.  Some data is only used for one or the other, but not
// both.

#include <oofconfig.h>
#include "common/doublevec.h"
#include "common/smallmatrix.h"
#include "engine/elementnodeiterator.h"
#include "engine/field.h"
#include "engine/fieldindex.h"

#include <vector>

class SmallSparseMatrix : public SmallMatrix {
  // SmallSparseMatrix doesn't bother storing its values in a sparse
  // data structure, because it's small.  What it does do is to keep
  // track of which values have been used, so that when it's used to
  // build a large sparse matrix only the nonzeros will contribute.
private:
  std::vector<bool> nonzero_;

public:
  SmallSparseMatrix(int, int);

  virtual double &operator()(int row, int col);
  virtual const double &operator()(int row, int col) const;
  void operator+=(const SmallSparseMatrix&);

  bool nonzero(int, int) const;
};


class SmallSystem {

private:
  mutable int current_row, current_col;
  void _set_index(const FieldIndex&,
		  const Field*,
		  const FieldIndex&,
		  const ElementFuncNodeIterator&) const;
  DoubleVec fluxVector_, forceVector_, offsetVector_;
  SmallSystem(const SmallSystem&); // prohibited!
public:

  // TODO 3.1: Make these private, and add accessors like fluxVector_'s.
  SmallSparseMatrix mMatrix, cMatrix, kMatrix, dfMatrix;

  // These booleans keep track of whether or not the various matrices
  // in the smallsystem have been written to.  They're true at
  // construction time, and are set false if any non-const element
  // retrieval function is ever run.
  bool m_clean, c_clean, k_clean, df_clean;
  bool flux_clean, force_clean, offset_clean;

  SmallSystem(int nr,int nc);

  int nrows() const;
  int ncols() const;

  void reset();

  const DoubleVec &fluxVector() const;
  DoubleVec &fluxVector();

  const DoubleVec &forceVector() const;
  DoubleVec &forceVector();

  const DoubleVec &offsetVector() const;
  DoubleVec &offsetVector();

  double &stiffness_matrix_element(const FieldIndex&,
				   const Field*,
				   const FieldIndex&,
				   const ElementFuncNodeIterator&
				   );
  double &stiffness_matrix_element(const FieldIndex&,
				   const Field*,
				   const ElementFuncNodeIterator&
				   );
  const double &stiffness_matrix_element(const FieldIndex&,
					 const Field*,
					 const FieldIndex&,
					 const ElementFuncNodeIterator&
					 ) const;
  const double &stiffness_matrix_element(const FieldIndex&,
					 const Field*,
					 const ElementFuncNodeIterator&
					 ) const;

  double &force_deriv_matrix_element(const FieldIndex&,
				     const Field*,
				     const FieldIndex&,
				     const ElementFuncNodeIterator&
                                     );
  double &force_deriv_matrix_element(const FieldIndex&,
				     const Field*,
				     const ElementFuncNodeIterator&
                                     );
  const double &force_deriv_matrix_element(const FieldIndex&,
					   const Field*,
					   const FieldIndex&,
					   const ElementFuncNodeIterator&
                                           ) const;
  const double &force_deriv_matrix_element(const FieldIndex&,
					   const Field*,
					   const ElementFuncNodeIterator&
                                           ) const;

  double &damping_matrix_element(const FieldIndex&,
				 const Field*,
				 const FieldIndex&,
				 const ElementFuncNodeIterator&
				 );
  double &damping_matrix_element(const FieldIndex&,
				 const Field*,
				 const ElementFuncNodeIterator&
				 );
  const double &damping_matrix_element(const FieldIndex&,
				       const Field*,
				       const FieldIndex&,
				       const ElementFuncNodeIterator&
				       ) const;
  const double &damping_matrix_element(const FieldIndex&,
				       const Field*,
				       const ElementFuncNodeIterator&
                                       ) const;

  double &mass_matrix_element(const FieldIndex&,
			      const Field*,
			      const FieldIndex&,
			      const ElementFuncNodeIterator&
                              );
  double &mass_matrix_element(const FieldIndex&,
			      const Field*,
			      const ElementFuncNodeIterator&
			      );
  const double &mass_matrix_element(const FieldIndex&,
				    const Field*,
				    const FieldIndex&,
				    const ElementFuncNodeIterator&
			            ) const;
  const double &mass_matrix_element(const FieldIndex&,
				    const Field*,
				    const ElementFuncNodeIterator&
				    ) const;

  double &flux_vector_element(const FieldIndex&);

  double &flux_vector_element(const int&);

  const double &flux_vector_element(const FieldIndex&) const;

  const double &flux_vector_element(const int&) const;

  double &force_vector_element(const FieldIndex&);

  double &force_vector_element(const int&);

  const double &force_vector_element(const FieldIndex&) const;

  const double &force_vector_element(const int&) const;

  double &offset_vector_element(const FieldIndex&);

  double &offset_vector_element(const int&);

  const double &offset_vector_element(const FieldIndex&) const;

  const double &offset_vector_element(const int&) const;

  friend std::ostream& operator<<(std::ostream &,
				  const SmallSystem&);

  void operator+=(const SmallSystem&);

};


inline void SmallSystem::_set_index(const FieldIndex &fluxindex,
				    const Field *field,
				    const FieldIndex &fieldindex,
				    const ElementFuncNodeIterator &efi)

  const {
  // TODO OPT: Compute and cache the global index for the
  // field/node/component combo that you can see here.
  current_row = fluxindex.integer();
  current_col = efi.localindex(*field, &fieldindex);
  // TODO OPT: Bounds check?  Or is that too slow?
}


