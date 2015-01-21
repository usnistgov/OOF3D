// -*- C++ -*-
// $RCSfile: removeitem.h,v $
// $Revision: 1.4.18.1 $
// $Author: langer $
// $Date: 2014/09/27 22:33:55 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef REMOVEITEM_H
#define REMOVEITEM_H

// This might be provided in the STL, but I can't find it... It
// removes the first occurence of item from a container.

template <class CONTAINER, class ITEM>
void remove_item(CONTAINER &container, const ITEM &item) {
  for(typename CONTAINER::iterator i = container.begin();
      i != container.end(); ++i) {
    if(*i == item) {
      container.erase(i);
      return;
    }
  }
}

#endif
