// -*- C++ -*-
// $RCSfile: random.C,v $
// $Revision: 1.3.18.17 $
// $Author: langer $
// $Date: 2014/01/18 20:36:26 $


/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

// random number generator.

// This uses the stateful version of the stdlib random() function.
// Using the stateful version means that we get the same random
// sequence even if a third party library (we're talking to you,
// fontconfig!) makes uncontrolled calls to random().

#include "common/lock.h"
#include "common/random.h"
#include <algorithm>
#include <iostream>
#include <math.h>
#include <stdlib.h>

static const long BIGGEST = 2147483647; // 2^31-1

#define STATE_SIZE 128
static char randomstate[STATE_SIZE];
static char *state = 0;
static void initrndm();
static SLock rndmlock;

// initrndm is called if the random number generator hasn't been
// seeded.  Its only purpose is to set the initial value of 'state'.

static void initrndm() {
  // Get the default state by switching to a dummy state.
  char dummystate[STATE_SIZE];
  state = initstate(0, dummystate, STATE_SIZE);
  // Restore the default state.
  (void) setstate(state);
}

static int irndm_nolock() {
  if(state == 0)
    initrndm();
  char *oldstate = setstate(state);
  int x = random();
  state = setstate(oldstate);
  return x;
}

int irndm() {
  rndmlock.acquire();
  int x = irndm_nolock();
  rndmlock.release();
  return x;
}

double rndm() {
  return irndm()/(BIGGEST+1.0);
}

static double rndm_nolock() {
  return irndm_nolock()/(BIGGEST+1.0);
}

// gaussian deviates, copied from numerical recipes

static bool saved = false;	// for gasdev
static double save_me;		// for gasdev

static void reset_gasdev() {
  saved = false;
}

double gasdev() {
  double v1, v2, rsq;
  rndmlock.acquire();
  if(!saved) {
    do {
      v1 = 2.0*rndm_nolock() - 1.0;
      v2 = 2.0*rndm_nolock() - 1.0;
      rsq = v1*v1 + v2*v2;
    } while(rsq >= 1.0 || rsq == 0);
    
    double fac = sqrt(-2.0*log(rsq)/rsq);
    save_me = v1*fac;
    saved = true;
    rndmlock.release();
    return v2*fac;
  }
  saved = false;
  rndmlock.release();
  return save_me;
}

int OOFRandomNumberGenerator::operator() (int aRange) {
  int x = irndm() % aRange;
  return x;
}

void rndmseed(int seed) {
#ifdef DEBUG
  std::cerr << "******** SETTING RANDOM SEED " << seed << std::endl;
#endif // DEBUG
  rndmlock.acquire();
  char *oldstate = initstate(seed, randomstate, STATE_SIZE);
  state = setstate(oldstate);
  reset_gasdev();
  rndmlock.release();
}

// For debugging std::random_shuffle, which behaves differently on OS X 10.9. 
std::vector<int> *randomInts(int n) {
  std::vector<int> *vec = new std::vector<int>(n);
  for(int i=0; i<n; i++)
    (*vec)[i] = i;
  OOFRandomNumberGenerator rand;
  //std::random_shuffle(vec->begin(), vec->end(), rand);
  oofshuffle(vec->begin(), vec->end(), rand);
  return vec;
}
