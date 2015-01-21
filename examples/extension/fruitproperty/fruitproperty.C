// -*- C++ -*-
// $RCSfile: fruitproperty.C,v $
// $Revision: 1.8.8.1 $
// $Author: langer $
// $Date: 2014/09/27 22:35:14 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include "fruitproperty.h"
#include "engine/element.h"
#include "engine/elementnodeiterator.h"
#include "engine/flux.h"
#include "engine/field.h"
#include "engine/flux.h"
#include "engine/mastercoord.h"
#include "engine/material.h"
#include "engine/property/orientation/orientation.h"


// The FruitProperty constructor must pass the registration and name
// on to the base class Property constructor, and store the values of
// the property's parameters.  It can also do some precomputation --
// such as fetching the pointers to the Field and Flux that it uses.

FruitProperty::FruitProperty(PyObject *registration, const std::string &name,
			     const SymmMatrix3 &modulus, double coupling)
  : Property(name, registration),
    modulus(modulus),
    coupling(coupling)
{
  // Field::getField() takes the name of a Field and returns a pointer
  // to a Field base class object.
  strawberryField = dynamic_cast<ScalarField*>(Field::getField("Strawberry"));
  // Flux::getFlux() does the same for a Flux.
  jamFlux = dynamic_cast<VectorFlux*>(Flux::getFlux("Strawberry_Jam"));
}

// cross_reference is called after all Properties have been added to a
// Material.  Material::fetchProperty is called to find another
// Property of the same Material with a given property type.  In this
// case, the FruitProperty needs to know the Material's orientation.
// (If there were quantities that depended on the element geometry but
// not on the node, they could be computed in the begin_element
// function.  We don't have any such quantities in this example.)

void FruitProperty::cross_reference(Material *mat) {
  orientation = dynamic_cast<OrientationProp*>
    (mat->fetchProperty("Orientation"));
}

// precompute is called after cross-referencing is complete, but
// before stiffness matrix construction begins.  It's a place to
// compute quantities that don't depend on element geometry or field
// values.  Here, it's used to rotate the modulus tensor from crystal
// coordinates to lab coordinates.

void FruitProperty::precompute(FEMesh *mesh) {
  if(orientation->constant_in_space())
    lab_modulus = modulus.transform(orientation->orientation());
}

// integration_order returns the polynomial order the Property's
// contribution to the stiffness matrix integrand, taking into account
// the shape function factors and any other variable terms.  Since
// fluxmatrix computes a constant times a shape function derivative,
// integration_order returns the degree of the shape function
// derivative.  However, if there are out-of-plane contributions to
// fluxmatrix, they are multiplied by the shape function (not its
// derivative). In that case, integration_order returns the degree of
// the shape function, because it's larger.

int FruitProperty::integration_order(const FEMesh *mesh, const Element *el)
  const
{
  if(strawberryField->in_plane(mesh))
    return el->dshapefun_degree();
  return el->shapefun_degree();
}

// The flux matrix multiplies the vector containing the degrees of
// freedom of an element (ie, field values at the nodes) to produce a
// vector containing the components of the given flux.  Only the
// contribution from the shape functions at one node are computed on
// each call.  If i is a flux component index, j is a Field component
// index, nu is a node, and A is the flux matrix, then

// Flux[i] = (integral over the element) A[ij nu] u[j nu] (summed over j and nu)

// The job of the fluxmatrix function is to compute A, given nu.

//  The arguments are:

// mesh: a pointer to the finite element mesh.  It must be passed
// through to other functions, but is not used directly.

// element: a pointer to the current finite element.  It might be
// used, for example, if a Property has a spatially dependent modulus
// (since the element geometry comes into the position
// computation). It's not used in this example.

// nu: the current node, in the form of an ElementFuncNodeIterator.
// All of the necessary data about the node are available from the
// iterator.  Don't let the fact that it's an iterator confuse you.
// The fluxmatrix function isn't allowed to increment the iterator;
// the iterator's just a convenient way of getting the node data.

// flux: A pointer to the flux whose flux matrix is being computed.
// One Property can contribute to more than one flux, so it's
// important to check the value of this variable.

// fluxdata: A pointer to a FluxData object which holds the computed
// flux matrix.  The matrix isn't stored in the Flux object itself,
// because it's possible that different execution threads are working
// on the same Flux.  

// x: The position in the element's master coordinate space at which
// the calculation is taking place.  Often this will be an integration
// gauss point, but it doesn't have to be.

void FruitProperty::fluxmatrix(const FEMesh *mesh, const Element *element,
			       const ElementFuncNodeIterator &nu,
			       const Flux *flux,
			       FluxData *fluxdata,
			       const MasterPosition &x) const
{
  // First, we check that the flux we're given is the expected one.
  // If the PropertyRegistration is set up correctly, we should never
  // get an unexpected Flux here.  If this Property made contributions
  // to more than one Flux, we'd do different things depending on
  // which flux we received.
  if(*flux != *jamFlux)
    throw ErrProgrammingError("Unexpected flux!", __FILE__, __LINE__);

  // The flux is the negative of the modulus times the gradient of the
  // field, and the gradient of the field is the gradient of the
  // shapefunction times the field values at the node.  

  // Evaluate the shapefunction of node nu and its derivatives at
  // point x in master coordinate space.
  double sf = nu.shapefunction(x); // shapefunction
  double dsf0 = nu.dshapefunction(0, x); // x component of its gradient
  double dsf1 = nu.dshapefunction(1, x); // y component of its gradient

  // If the orientation isn't constant in space, the lab-frame modulus
  // wasn't computed in precompute().  Do it here, now that we can
  // compute the local orientation.
  SymmMatrix3 local_modulus;
  if(!orientation->constant_in_space())
    local_modulus = modulus.transform(
			     orientation->orientation(mesh, element, x));
  else
    local_modulus = lab_modulus;

  // Loop over the flux components, even the out-of-plane ones.  Even
  // if a plane-flux equation is applied to this flux, we need to
  // compute the out-of-plane components of the flux matrix in order
  // to construct the out-of-plane constraint equation.  This same
  // method can be used to iterate over the components of all kinds of
  // Fluxes and Fields in OOF2.
  for(IteratorP iter=flux->iterator(ALL_INDICES); !iter.end(); ++iter) {
    // Subtract the modulus times the derivative of the shape function
    // from the flux matrix.  Use -= instead of direct assignment,
    // because other Properties may already have made contributions.
    fluxdata->matrix_element(iter, strawberryField, nu) -=
      // The sum over field components (j) is written out explicitly
      // here to save time.  This only includes the *in-plane*
      // components of the Field, because they're the ones that are
      // stored in the nodes.

      // The modulus is stored in a matrix type that doesn't
      // understand an IteratorP, but IteratorP has a method that
      // returns the correct integer index of a Flux or Field
      // component.
      local_modulus(iter.integer(), 0) * dsf0 + // j = 0 (x)
      local_modulus(iter.integer(), 1) * dsf1;  // j = 1 (y)

    // If the Field has an out-of-plane derivative, it's stored as a
    // separate degree of freedom, and makes a contribution to the
    // flux matrix.  Because its already a derivative, the flux matrix
    // contribution uses the shapefunction directly, and not the
    // derivative.  See the manual for a better explanation.
    if(!strawberryField->in_plane(mesh)) {
      fluxdata->matrix_element(iter, strawberryField->out_of_plane(), nu)
	-= local_modulus(iter.integer(), 2) *sf;
    }
  }
}
