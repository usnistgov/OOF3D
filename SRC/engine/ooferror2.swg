// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef ENGINE_OOFERROR_SWG
#define ENGINE_OOFERROR_SWG

// This file is called ooferror2.swg instead of ooferror.swg because
// if it were called "ooferror.swg", the swig-generated python code
// would start with "import ooferrorc", which would import
// SWIG/common/ooferrorcmodule, since that one has already been
// loaded.

%module ooferror2

// When adding Error subclasses here, add them to engine/ooferror.spy
// as well.


%include "common/typemaps.swg"
%extern "common/ooferror.swg"
%{
#include "engine/ooferror.h"
%}

%pragma(python) code="from ooflib.SWIG.common.ooferror import *"
%pragma(python) include="ooferror2.spy"

class ErrNoSuchField : public ErrError {
public:
  ErrNoSuchField(char *m);
  ~ErrNoSuchField();
  %addmethods {
    %new const string *__repr__() {
      return self->summary();
    }
  }
};

class ErrDuplicateField : public ErrError {
public:
  ErrDuplicateField(char*, char*, char*);
  ~ErrDuplicateField();
  %addmethods {
    %new const string *__repr__() {
      return self->summary();
    }
  }
};

class ErrNoSuchProperty : public ErrError {
public:
  ErrNoSuchProperty(char*, char*);
  ~ErrNoSuchProperty();
  %addmethods {
    %new const string *__repr__() {
      return self->summary();
    }
  }
};

class ErrPropertyMissing : public ErrError {
public:
  ErrPropertyMissing(char*, char*, char*);
  ~ErrPropertyMissing();
  %addmethods {
    %new const string *__repr__() {
      return self->summary();
    }
  }
};

class ErrBadMaterial : public ErrError {
public:
  ErrBadMaterial(char*);
  ~ErrBadMaterial();
  %addmethods {
    %new const string *__repr__() {
      return self->summary();
    }
  }
  const string &materialName();
};

class ErrRedundantProperty : public ErrError {
public:
  ErrRedundantProperty(char*);
  ~ErrRedundantProperty();
  const string &get_tag();
  %addmethods {
    %new const string *__repr__() {
      return self->summary();
    }
  }
};

class ErrConvergenceFailure : public ErrError {
public:
  ErrConvergenceFailure(char*, int);
  ~ErrConvergenceFailure();
  %addmethods {
    %new const string *__repr__() {
      return self->summary();
    }
  }
};

class ErrTimeStepTooSmall : public ErrError {
public:
  ErrTimeStepTooSmall(double);
  ~ErrTimeStepTooSmall();
  %addmethods {
    %new const string *__repr__() {
      return self->summary();
    }
  }
}

class ErrInvalidDestination : public ErrError {
public:
  ErrInvalidDestination();
  ~ErrInvalidDestination();
  %addmethods {
    %new const string *__repr__() {
      return self->summary();
    }
  }
};

class ErrInstabilityError : public ErrError {
public:
  ErrInstabilityError(char*);
  ~ErrInstabilityError();
  %addmethods {
    %new const string *__repr__() {
      return self->summary();
    }
  }
};

class ErrHomogeneityNotCalculable : public ErrError {
public:
  ErrHomogeneityNotCalculable();
  ~ErrHomogeneityNotCalculable();
  %addmethods {
    %new const string *__repr__() {
      return self-> summary();
    }
  }
};


// class ErrSearchFailure : public ErrError {
// public:
//   ErrSearchFailure();
//   ~ErrSearchFailure();
//   %addmethods {
//     %new const string *__repr__() {
//       return self->summary();
//     }
//   }
// };

#endif // ENGINE_OOFERROR_SWG
