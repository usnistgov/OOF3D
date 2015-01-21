// -*- C++ -*-
// $RCSfile: meshdatacache.h,v $
// $Revision: 1.6.4.5 $
// $Author: langer $
// $Date: 2014/10/01 16:01:27 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef MESHDATACACHE_H
#define MESHDATACACHE_H

#include <oofconfig.h>
#include "common/doublevec.h"
#include <map>
#include <set>

class FEMesh;

class MeshDataCache {
private:
  DoubleVec times_;
  DoubleVec interpolant;
protected:
  FEMesh *mesh;
  void clear_times();
  void add_time(double);
  // latest stores original mesh dofs when cached data is installed
  DoubleVec *latest;
  double latesttime;
  void saveLatest();
  virtual DoubleVec &fetchOne(double) = 0;
  virtual bool checkTime(double) const = 0;
  virtual DoubleVec *allTimes() const = 0;
public:
  MeshDataCache() : mesh(0), latest(0) {}
  virtual ~MeshDataCache();
  void setMesh(FEMesh *mesh);
  virtual const DoubleVec *times() const { return &times_; }
  void restore(double);		// restore data to mesh, if needed
  bool interpolate(double);
  virtual void restoreLatest();
  virtual void restore_(double) = 0; // actually restore
  virtual void record() = 0;	     // save data from mesh
  virtual void clear() = 0;
  double latestTime() const;
  double earliestTime() const;
  // double latestCachedTime() const;
  void transfer(MeshDataCache*);
  int size() const { return times_.size(); }
  bool empty() const { return times_.empty(); }

  bool atLatest() const { 
    // If the data in the mesh is the most recent, then that data is
    // *not* stored in the cache.
    return latest == 0; 
  }

  bool atEarliest() const;
};

class MemoryDataCache : public MeshDataCache {
private:
  typedef std::map<double, DoubleVec> DataCache;
  DataCache cache;
  void storedofs(DoubleVec&); // get data from mesh
  virtual DoubleVec &fetchOne(double);
  virtual bool checkTime(double) const;
  virtual DoubleVec *allTimes() const;
public:
  MemoryDataCache();
  ~MemoryDataCache();
  virtual void restore_(double);
  virtual void record();
  virtual void clear();
};

class DiskDataCache : public MeshDataCache {
private:
  static int nCaches;
  struct lt {
    bool operator()(const DiskDataCache*, const DiskDataCache*) const;
  };
  static std::set<DiskDataCache*, lt> allCaches;

  static bool initialized;
  int cacheID;
  typedef std::map<double, std::string> FileDict;
  DoubleVec localdata;
  FileDict fileDict; // maps ints to file names
  void clear_(bool force);
  virtual DoubleVec &fetchOne(double);
  virtual bool checkTime(double) const;
  virtual DoubleVec *allTimes() const;
public:
  DiskDataCache();
  ~DiskDataCache();
  virtual void restore_(double);
  virtual void record();
  virtual void clear();
  friend void cleanUpDDcaches();
};

void cleanUpDDcaches();

#endif // MESHDATACACHE_H
