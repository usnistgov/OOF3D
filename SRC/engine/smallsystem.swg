// -*- C++ -*-
// $RCSfile: smallsystem.swg,v $
// $Revision: 1.3.6.1 $
// $Author: langer $
// $Date: 2013/11/08 20:44:50 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#ifndef SMALLSYSTEM_SWG
#define SMALLSYSTEM_SWG

%module smallsystem

%include "common/typemaps.swg"

%{
#include "engine/smallsystem.h"
%}

%extern "engine/fieldindex.swg"
%pragma(python) code="from ooflib.SWIG.engine.fieldindex import IteratorPPtr"
%pragma(python) code="from ooflib.SWIG.engine.fieldindex import IndexPPtr"
%pragma(python) code="from ooflib.SWIG.engine.flux import FluxPtr"
%pragma(python) code="from ooflib.SWIG.engine.flux import SymmetricTensorFluxPtr"
%pragma(python) code="from ooflib.SWIG.engine.flux import VectorFluxPtr"


class SmallSystem {
public:
  SmallSystem(int, int);
  ~SmallSystem();
  %addmethods {
    double get_stiffness_matrix_element(const IndexP &fluxIndex,
					const Field *field,
					const IndexP &fieldIndex,
					const ElementFuncNodeIterator &efi)
    {
      return self->stiffness_matrix_element(fluxIndex, field, fieldIndex, efi);
    }

    void add_stiffness_matrix_element(const IndexP &fluxIndex,
				      const Field *field,
				      const IndexP &fieldIndex,
				      const ElementFuncNodeIterator &efi,
				      double increment)
    {
      self->stiffness_matrix_element(fluxIndex, field, fieldIndex, efi)
	+= increment;
    }

    double get_force_deriv_matrix_element(const IndexP &forceIndex,
					  const Field *field,
					  const IndexP &fieldIndex,
					  const ElementFuncNodeIterator &efi)
    {
      return self->force_deriv_matrix_element(forceIndex, field, fieldIndex,
					      efi);
    }

    void add_force_deriv_matrix_element(const IndexP &forceIndex,
					const Field *field,
					const IndexP &fieldIndex,
					const ElementFuncNodeIterator &efi,
					double increment)
    {
      self->force_deriv_matrix_element(forceIndex, field, fieldIndex, efi)
	+= increment;
    }

    double get_damping_matrix_element(const IndexP &fluxIndex,
				      const Field *field,
				      const IndexP &fieldIndex,
				      const ElementFuncNodeIterator &efi)
    {
      return self->damping_matrix_element(fluxIndex, field, fieldIndex, efi);
    }

    void add_damping_matrix_element(const IndexP &fluxIndex,
				    const Field *field,
				    const IndexP &fieldIndex,
				    const ElementFuncNodeIterator &efi,
				    double increment)
    {
      self->damping_matrix_element(fluxIndex, field, fieldIndex, efi)
	+= increment;
    }

    double get_mass_matrix_element(const IndexP &fluxIndex,
				   const Field *field,
				   const IndexP &fieldIndex,
				   const ElementFuncNodeIterator &efi)
    {
      return self->mass_matrix_element(fluxIndex, field, fieldIndex, efi);
    }

    void add_mass_matrix_element(const IndexP &fluxIndex,
				 const Field *field,
				 const IndexP &fieldIndex,
				 const ElementFuncNodeIterator &efi,
				 double increment)
    {
      self->mass_matrix_element(fluxIndex, field, fieldIndex, efi)
	+= increment;
    }

    double get_force_vector_element(const IndexP &forceIndex)
    {
      return self->force_vector_element(forceIndex);
    }

    void add_force_vector_element(const IndexP &forceIndex, double increment)
    {
      self->force_vector_element(forceIndex) += increment;
    }

    double get_flux_vector_element(const IndexP &fluxIndex)
    {
      return self->flux_vector_element(fluxIndex);
    }

    void add_flux_vector_element(const IndexP &fluxIndex, double increment)
    {
      self->flux_vector_element(fluxIndex) += increment;
    }

    double get_offset_vector_element(const IndexP &offsetIndex)
    {
      return self->offset_vector_element(offsetIndex);
    }

    void add_offset_vector_element(const IndexP &offsetIndex, double increment)
    {
      self->offset_vector_element(offsetIndex) += increment;
    }
  }
};

#endif
