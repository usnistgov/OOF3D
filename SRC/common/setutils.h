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

#ifndef SETUTILS_H
#define SETUTILS_H

// Function for finding the first shared entry in a pair of std::sets.

template <class SET>
typename SET::const_iterator sharedEntry(const SET &a, const SET &b)
{
  if(a.empty() || b.empty())
    return a.end();
  typename SET::const_iterator i0 = a.begin();
  typename SET::const_iterator i1 = b.begin();
  auto lessthan = typename SET::key_compare();
  do {
    bool lt01 = lessthan(*i0, *i1);
    bool lt10 = lessthan(*i1, *i0);
    if(!lt01 && !lt10)
      return i0;
    if(lt01)
      ++i0;
    else
      ++i1;
  } while(i0 != a.end() && i1 != b.end());
  return a.end();
}

template <class SET>
typename SET::iterator sharedEntry(SET &a, SET &b)
{
  if(a.empty() || b.empty())
    return a.end();
  typename SET::iterator i0 = a.begin();
  typename SET::iterator i1 = b.begin();
  auto lessthan = typename SET::key_compare();
  do {
    bool lt01 = lessthan(*i0, *i1);
    bool lt10 = lessthan(*i1, *i0);
    if(!lt01 && !lt10)
      return i0;
    if(lt01)
      ++i0;
    else
      ++i1;
  } while(i0 != a.end() && i1 != b.end());
  return a.end();
}

// These two versions of sharedEntry won't return the entry "exclude",
// if it's in the sets.

template <class SET>
typename SET::const_iterator sharedEntry(
				       const SET &a, const SET &b,
				       const typename SET::key_type &exclude)
{
  if(a.empty() || b.empty())
    return a.end();
  typename SET::const_iterator i0 = a.begin();
  typename SET::const_iterator i1 = b.begin();
  auto lessthan = typename SET::key_compare();
  do {
    if(*i0 == exclude) {
      ++i0;
      continue;
    }
    if(*i1 == exclude) {
      ++i1;
      continue;
    }
    bool lt01 = lessthan(*i0, *i1);
    bool lt10 = lessthan(*i1, *i0);
    if(!lt01 && !lt10)
      return i0;
    if(lt01)
      ++i0;
    else
      ++i1;
  } while(i0 != a.end() && i1 != b.end());
  return a.end();
}

template <class SET>
typename SET::iterator sharedEntry(SET &a, SET &b,
				   const typename SET::key_type &exclude)
{
  if(a.empty() || b.empty())
    return a.end();
  typename SET::iterator i0 = a.begin();
  typename SET::iterator i1 = b.begin();
  auto lessthan = typename SET::key_compare();
  do {
    if(*i0 == exclude) {
      ++i0;
      continue;
    }
    if(*i1 == exclude) {
      ++i1;
      continue;
    }
    bool lt01 = lessthan(*i0, *i1);
    bool lt10 = lessthan(*i1, *i0);
    if(!lt01 && !lt10)
      return i0;
    if(lt01)
      ++i0;
    else
      ++i1;
  } while(i0 != a.end() && i1 != b.end());
  return a.end();
}

// Slightly different version for maps.  It returns an iterator
// pointing to an entry in the first map which has a matching key in
// the second map.

template <class MAP>
typename MAP::const_iterator sharedMapEntry(const MAP &a, const MAP &b)
{
  if(a.empty() || b.empty())
    return a.end();
  typename MAP::const_iterator i0 = a.begin();
  typename MAP::const_iterator i1 = b.begin();
  auto lessthan = typename MAP::key_compare();
  do {
    bool lt01 = lessthan((*i0).first, (*i1).first);
    bool lt10 = lessthan((*i1).first, (*i0).first);
    if(!lt01 && !lt10)
      return i0;
    if(lt01)
      ++i0;
    else
      ++i1;
  } while(i0 != a.end() && i1 != b.end());
  return a.end();
}


// Call the given function for each member of set a that's also a
// member of set b. "data" is passed as an extra argument to the
// callback function, which should return "true" to stop the
// iteration.

template <class SET>
void foreachShared(const SET &a, const SET &b,
		   bool (*f)(const typename SET::value_type&, void*),
		   void *data)
{
  if(a.empty() || b.empty())
    return;
  typename SET::const_iterator i0 = a.begin();
  typename SET::const_iterator i1 = b.begin();
  auto lessthan = typename SET::key_compare();
  do {
    bool lt01 = lessthan(*i0, *i1);
    bool lt10 = lessthan(*i1, *i0);
    if(!lt01 && !lt10)  {
      if(f(*i0, data))
	return;
      ++i0;
      ++i1;
    }
    else if(lt01)
      ++i0;
    else
      ++i1;
  } while(i0 != a.end() && i1 != b.end());
}

// Template for looping over two sets which contain pointers to
// objects with a common base class.  Use it with a range based
// iterator:
//   std::set<A*> a;
//   std::set<B*> b;
//   for(BASE *obj : TwoSetIterator<BASE, std::set<A*>, std::set<B*>>(a, b)):
//       etc.

// If you must use a regular for loop, make sure you don't create two
// TwoSetIterators.  This is ok:
//   TwoSetIterator<BASE, std::set<A*>, std::set<B*>> iter(a, b);
//   for(auto i=iter.begin(); i!=iter.end(); ++i)
//     etc.
// This is not ok:
//  for(auto i=TwoSetIterator<BASE, std::set<A*>, set::set<B*>>(a,b).begin();
//           i!=TwoSetIterator<BASE, std::set<A*>, std::set<B*>>(a,b).end(); ++i)
//     etc.

// TODO: Can this be done without copying the sets?  Copying seems dumb.

template <class BASE, class SETA, class SETB>
class TwoSetIterator {
private:
  std::vector<BASE*> combo;
public:
  TwoSetIterator(const SETA &a, const SETB &b) {
    combo.reserve(a.size() + b.size());
    combo.insert(combo.end(), a.begin(), a.end());
    combo.insert(combo.end(), b.begin(), b.end());
  }
  typename std::vector<BASE*>::iterator begin() {
    return combo.begin();
  }
  typename std::vector<BASE*>::iterator end() {
    return combo.end();
  }
  typename std::vector<BASE*>::const_iterator begin() const {
    return combo.begin();
  }
  typename std::vector<BASE*>::const_iterator end() const {
    return combo.end();
  }
};


#endif // SETUTILS_H
