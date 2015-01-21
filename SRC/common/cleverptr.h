// -*- C++ -*-
// $RCSfile: cleverptr.h,v $
// $Revision: 1.1.2.2 $
// $Author: langer $
// $Date: 2013/08/22 19:50:11 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>
#include <iostream>


template <class T>
class CleverPtr {
private:
  T *val;
  CleverPtr(const CleverPtr<T>&); // Unimplemented private copy constructor.
public:
  CleverPtr(T *x) : val(x) {}
  ~CleverPtr() { delete val; }
  T* operator->() const { return val; }
  // "value" returns the enclosed pointer, whereas "*" dereferences
  // the enclosed pointer.
  T* value() const { return val; }
  T& operator*() const { return *val; }
};

// The CleverPtr class is a special container that contains a pointer
// to an object, and supports pointer semantics, with the special
// additional feature that it deletes the pointed-to object when it
// goes out of scope.  It doesn't actually do reference-counting, and
// so does not qualify to be an actual smart pointer. It was created
// for the ElementFuncNodeIterators, but may be useful for other
// things.  The comment block below shows a usage example.

// class A {
// private:
//   int x;
// public:
//   A(int x) : x(x) {}
//   ~A() {
//     std::cout << "Deleting " << x << std::endl;
//   }
//   void print() { std::cerr << "Print: " << x << std::endl; }
// };

// int main(int, char**) {
//   std::cout << "Hello" << std::endl;
//   {
//     A *a = new A(3);
//     CleverPtr<A> aptr(a);
//     aptr->print();
//     std::cerr << "Value: "; aptr.value()->print();
//   }
//   std::cout << "Goodbye" << std::endl;
// }
