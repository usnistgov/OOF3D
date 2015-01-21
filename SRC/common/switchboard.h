// -*- C++ -*-
// $RCSfile: switchboard.h,v $
// $Revision: 1.11.2.1 $
// $Author: langer $
// $Date: 2012/12/05 20:31:55 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef SWITCHBOARD_H
#define SWITCHBOARD_H

#include <oofconfig.h>

#include <iostream>
#include <string>
#include <vector>

#include "common/pythonexportable.h"

class OOFMessage : public PythonExportable<OOFMessage> {
private:
  const std::string msgname;
  std::vector<PyObject*> args;
  static const std::string classname_;
  static const std::string modulename_;
public:
  OOFMessage(const std::string &msgname);
  const std::string &name() const;
  virtual const std::string &classname() const { return classname_; }
  virtual const std::string &modulename() const { return modulename_; }
  void addarg(const PythonExportableBase&);
  void addarg(const std::string &);
  void addarg(int);
  int nargs() const;
  PyObject *getarg(int) const;
};

void switchboard_notify(const std::string&);
void switchboard_notify(const OOFMessage&); // for more complicated messages

void init_switchboard_api(PyObject*); // called once, by switchboard module

#endif // SWITCHBOARD_H
