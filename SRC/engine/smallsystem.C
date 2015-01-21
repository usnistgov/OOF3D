// -*- C++ -*-
// $RCSfile: smallsystem.C,v $
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

#include <oofconfig.h>
#include "common/vectormath.h"
#include "engine/smallsystem.h"
#include <vector>

// Default constructor clears all the objects.
SmallSystem::SmallSystem(int nr, int nc) :
  current_row(0), current_col(0),
  fluxVector_(nr, 0.0), forceVector_(nr, 0.0), offsetVector_(nr, 0.0),
  mMatrix(nr,nc), cMatrix(nr,nc), kMatrix(nr,nc), dfMatrix(nr,nc),
  m_clean(true), c_clean(true), k_clean(true), df_clean(true),
  flux_clean(true), force_clean(true), offset_clean(true)
{
  mMatrix.clear();
  cMatrix.clear();
  kMatrix.clear();
  dfMatrix.clear();
}

void SmallSystem::reset() {
  mMatrix.clear();
  cMatrix.clear();
  kMatrix.clear();
  dfMatrix.clear();
  zero(fluxVector_);
  zero(forceVector_);
  zero(offsetVector_);
  m_clean = true;
  c_clean = true;
  k_clean = true;
  df_clean = true;
  flux_clean = true;
  force_clean = true;
  offset_clean = true;
}

int SmallSystem::nrows() const {
  return mMatrix.rows();
}

int SmallSystem::ncols() const {
  return mMatrix.cols();
}

const DoubleVec &SmallSystem::fluxVector() const {
  return fluxVector_;
}

DoubleVec &SmallSystem::fluxVector() {
  flux_clean = false;
  return fluxVector_;
}

const DoubleVec &SmallSystem::forceVector() const {
  return forceVector_;
}

DoubleVec &SmallSystem::forceVector() {
  force_clean = false;
  return forceVector_;
}

const DoubleVec &SmallSystem::offsetVector() const {
  return offsetVector_;
}

DoubleVec &SmallSystem::offsetVector() {
  offset_clean = false;
  return offsetVector_;
}

// SmallSystem::_set_index is inlined, and is in the .h file.

double
&SmallSystem::stiffness_matrix_element (const FieldIndex &fi,
					const Field *field,
					const FieldIndex &fieldindex,
					const ElementFuncNodeIterator &efi)
{
  k_clean = false;
  _set_index(fi, field, fieldindex, efi);
  return kMatrix(current_row, current_col);
}

double
&SmallSystem::stiffness_matrix_element (const FieldIndex &fi,
					const Field *field,
					const ElementFuncNodeIterator &efi)
{
  k_clean = false;
  ScalarFieldIndex sfi;
  _set_index(fi, field, sfi, efi);
  return kMatrix(current_row, current_col);
}

const double
&SmallSystem::stiffness_matrix_element (const FieldIndex &fi,
					const Field *field,
					const FieldIndex &fieldindex,
					const ElementFuncNodeIterator &efi)
  const
{
  _set_index(fi, field, fieldindex, efi);
  return kMatrix(current_row, current_col);
}

const double
&SmallSystem::stiffness_matrix_element (const FieldIndex &fi,
					const Field *field,
					const ElementFuncNodeIterator &efi)
  const
{
  ScalarFieldIndex sfi;
  _set_index(fi, field, sfi, efi);
  return kMatrix(current_row, current_col);
}




double
&SmallSystem::force_deriv_matrix_element (const FieldIndex &fi,
					  const Field *field,
					  const FieldIndex &fieldindex,
					  const ElementFuncNodeIterator &efi)
{
  df_clean = false;
  _set_index(fi, field, fieldindex, efi);
  return dfMatrix(current_row, current_col);
}

double
&SmallSystem::force_deriv_matrix_element (const FieldIndex &fi,
					  const Field *field,
					  const ElementFuncNodeIterator &efi)

{
  df_clean = false;
  ScalarFieldIndex sfi;
  _set_index(fi, field, sfi, efi);
  return dfMatrix(current_row, current_col);
}

const double
&SmallSystem::force_deriv_matrix_element (const FieldIndex &fi,
					  const Field *field,
					  const FieldIndex &fieldindex,
					  const ElementFuncNodeIterator &efi)
                                          const
{
  _set_index(fi, field, fieldindex, efi);
  return dfMatrix(current_row, current_col);
}

const double
&SmallSystem::force_deriv_matrix_element (const FieldIndex &fi,
					  const Field *field,
					  const ElementFuncNodeIterator &efi)
  const
{
  ScalarFieldIndex sfi;
  _set_index(fi, field, sfi, efi);
  return dfMatrix(current_row, current_col);
}





double
&SmallSystem::damping_matrix_element (const FieldIndex &fi,
					const Field *field,
					const FieldIndex &fieldindex,
					const ElementFuncNodeIterator &efi)
{
  c_clean = false;
  _set_index(fi, field, fieldindex, efi);
  return cMatrix(current_row, current_col);
}

double
&SmallSystem::damping_matrix_element (const FieldIndex &fi,
					const Field *field,
					const ElementFuncNodeIterator &efi)
{
  c_clean = false;
  ScalarFieldIndex sfi;
  _set_index(fi, field, sfi, efi);
  return cMatrix(current_row, current_col);
}

const double
&SmallSystem::damping_matrix_element (const FieldIndex &fi,
					const Field *field,
					const FieldIndex &fieldindex,
					const ElementFuncNodeIterator &efi)
  const
{
  _set_index(fi, field, fieldindex, efi);
  return cMatrix(current_row, current_col);
}

const double
&SmallSystem::damping_matrix_element (const FieldIndex &fi,
					const Field *field,
					const ElementFuncNodeIterator &efi)
  const
{
  ScalarFieldIndex sfi;
  _set_index(fi, field, sfi, efi);
  return cMatrix(current_row, current_col);
}





double
&SmallSystem::mass_matrix_element (const FieldIndex &fi,
				   const Field *field,
				   const FieldIndex &fieldindex,
				   const ElementFuncNodeIterator &efi)
{
  m_clean = false;
  _set_index(fi, field, fieldindex, efi);
  return mMatrix(current_row, current_col);
}

double
&SmallSystem::mass_matrix_element (const FieldIndex &fi,
					const Field *field,
					const ElementFuncNodeIterator &efi)
{
  m_clean = false;
  ScalarFieldIndex sfi;
  _set_index(fi, field, sfi, efi);
  return mMatrix(current_row, current_col);
}

const double
&SmallSystem::mass_matrix_element (const FieldIndex &fi,
					const Field *field,
					const FieldIndex &fieldindex,
					const ElementFuncNodeIterator &efi)
  const
{
  _set_index(fi, field, fieldindex, efi);
  return mMatrix(current_row, current_col);
}

const double
&SmallSystem::mass_matrix_element (const FieldIndex &fi,
					const Field *field,
					const ElementFuncNodeIterator &efi)
  const
{
  ScalarFieldIndex sfi;
  _set_index(fi, field, sfi, efi);
  return mMatrix(current_row, current_col);
}



double
&SmallSystem::flux_vector_element (const FieldIndex &fi) {
  flux_clean = false;
  return fluxVector_[fi.integer()];
}

const double
&SmallSystem::flux_vector_element (const FieldIndex &fi) const {
  return fluxVector_[fi.integer()];
}

double
&SmallSystem::flux_vector_element (const int &fi) {
  flux_clean = false;
  return fluxVector_[fi];
}

const double
&SmallSystem::flux_vector_element (const int &fi) const {
  return fluxVector_[fi];
}



double
&SmallSystem::force_vector_element (const FieldIndex &fi) {
  force_clean = false;
  return forceVector_[fi.integer()];
}

const double
&SmallSystem::force_vector_element (const FieldIndex &fi) const {
  return forceVector_[fi.integer()];
}

double
&SmallSystem::force_vector_element (const int &fi) {
  force_clean = false;
  return forceVector_[fi];
}

const double
&SmallSystem::force_vector_element (const int &fi) const {
  return forceVector_[fi];
}



double
&SmallSystem::offset_vector_element (const FieldIndex &fi) {
  offset_clean = false;
  return offsetVector_[fi.integer()];
}

const double
&SmallSystem::offset_vector_element (const FieldIndex &fi) const {
  return offsetVector_[fi.integer()];
}

double
&SmallSystem::offset_vector_element (const int &fi) {
  offset_clean = false;
  return offsetVector_[fi];
}

const double
&SmallSystem::offset_vector_element (const int &fi) const {
  return offsetVector_[fi];
}


std::ostream& operator<<(std::ostream &os, const SmallSystem &ss) {
  os << ss.kMatrix;
  return os;
}

void SmallSystem::operator+=(const SmallSystem &other)
{
  mMatrix  += other.mMatrix;
  cMatrix  += other.cMatrix;
  kMatrix  += other.kMatrix;
  dfMatrix += other.dfMatrix;

  fluxVector_   += other.fluxVector_;
  forceVector_  += other.forceVector_;
  offsetVector_ += other.offsetVector_;

  m_clean  &= other.m_clean;
  c_clean  &= other.c_clean;
  k_clean  &= other.k_clean;
  df_clean &= other.df_clean;
  flux_clean   &= other.flux_clean;
  force_clean  &= other.force_clean;
  offset_clean &= other.offset_clean;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

SmallSparseMatrix::SmallSparseMatrix(int r, int c)
  : SmallMatrix(r, c),
    nonzero_(r*c, false)
{}

double &SmallSparseMatrix::operator()(int row, int col) {
  nonzero_[col*nrows+row] = true;
  return SmallMatrix::operator()(row, col);
}

const double &SmallSparseMatrix::operator()(int row, int col) const {
  return SmallMatrix::operator()(row, col);
}

bool SmallSparseMatrix::nonzero(int row, int col) const {
  return nonzero_[col*nrows + row];
}

void SmallSparseMatrix::operator+=(const SmallSparseMatrix &other) {
  data += other.data;
  for(unsigned int i=0; i<nonzero_.size(); i++)
    nonzero_[i] = nonzero_[i] || other.nonzero_[i];
}
