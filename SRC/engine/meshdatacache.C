// -*- C++ -*-
// $RCSfile: meshdatacache.C,v $
// $Revision: 1.10.4.11 $
// $Author: langer $
// $Date: 2014/10/15 20:53:46 $

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
#include "common/tostring.h"
#include "common/IO/oofcerr.h"
#include "engine/femesh.h"
#include "engine/meshdatacache.h"
#include "engine/ooferror.h"
#include <limits>               // for std::numeric_limits.
#include <stdio.h>
#include <stdlib.h>		// for atexit
#include <string.h> 		// for memcpy, strerror_r
#include <sys/stat.h>
#include <unistd.h>		// for mkstemp, unlink, access
extern int errno;

MeshDataCache::~MeshDataCache() {
  restoreLatest();
}

void MeshDataCache::clear_times() {
  times_.clear();
}

void MeshDataCache::setMesh(FEMesh *newmesh) {
  assert(times_.empty());
  mesh = newmesh;
}

void MeshDataCache::add_time(double time) {
  // If the time isn't greater than the last time recorded, it's an error.
  if(!times_.empty() && time <= times_.back()) {
    throw ErrProgrammingError("Non-sequential times in MeshDataCache!",
			      __FILE__, __LINE__);
  }
  times_.push_back(time);
}

void MeshDataCache::restore(double time) {
  if(mesh->getCurrentTime() != time) {
    restore_(time);
    interpolant.resize(0);
  }
}

void MeshDataCache::restoreLatest() {
  if(latest != 0) {
    mesh->dofvalues = latest;
    mesh->setCurrentTime(latesttime);
    latest = 0;
    interpolant.resize(0);
  }
}

bool MeshDataCache::interpolate(double time) {
  if(latest && time==latesttime) {
    restoreLatest();
    return true;
  }
  // If the given time is in the cache, just restore its data, and
  // don't interpolate.
  if(checkTime(time)) {
    restore(time);
    return true;
  }
  // Find the cached times before and after the given time.  This
  // doesn't assume that the times returned by allTimes are sorted.
  // It would probably be faster to do something clever with a sorted
  // list of times, but it's probably not worth the effort.
  double larger = std::numeric_limits<double>::max();
  double smaller = -larger;
  DoubleVec *times = allTimes();
  for(DoubleVec::iterator i=times->begin(); i<times->end(); ++i) {
    if(*i > smaller && *i < time)
      smaller = *i;
    if(*i < larger and *i > time) 
      larger = *i;
  }
  delete times;

  // Fail if the initial time was out of bounds.
  if(larger == std::numeric_limits<double>::max() ||
     smaller == -std::numeric_limits<double>::max())
    return false;
  
  DoubleVec &data0 = fetchOne(smaller); // retrieve from cache
  DoubleVec &data1 = fetchOne(larger);  // retrieve from cache
  if(data0.size() < data1.size())
    data0.resize(data1.size(), 0.0);
  double frac = (time - smaller)/(larger - smaller);
  interpolant = (1.-frac)*data0 + frac*data1;

  saveLatest();
  mesh->dofvalues = &interpolant;
  mesh->setCurrentTime(time);
  return true;
}

void MeshDataCache::saveLatest() {
  // saveLatest() is called when restoring data from the cache.  If
  // latest is non-zero, the latest mesh data has already been saved,
  // and the mesh contains cached data, which we don't need to save
  // again.
  if(latest == 0) {
    latest = mesh->dofvalues;
    latesttime = mesh->getCurrentTime();
  }
}

double MeshDataCache::latestTime() const {
  if(atLatest()) {
    return mesh->getCurrentTime();
  }
  return latesttime;
}

double MeshDataCache::earliestTime() const {
  if(times_.empty())
    return mesh->getCurrentTime();
  else
    return times_[0];
}

bool MeshDataCache::atEarliest() const {
  return mesh->getCurrentTime() == earliestTime();
}

// double MeshDataCache::latestCachedTime() const {
//   if(times_.empty())
//     throw ErrBoundsError("");
//   return times_.back();
// }

void MeshDataCache::transfer(MeshDataCache *other) {
  // Copy data into this cache from another one.  This is done via the
  // caches' save and restore mechanisms, so it changes data in the
  // mesh.  We have to be sure to restore the state of the mesh.
  latest = other->latest;
  latesttime = other->latesttime;
  // If latest==0, the caches aren't storing the mesh's latest time,
  // which means that the mesh is storing it; ie, the mesh is set to
  // its latest time.  After calling restore_ and record, the mesh
  // won't be at its latest time, and latest will be non-zero.
  bool atlatest = (latest == 0);
  double time = mesh->getCurrentTime();
  clear();
  const DoubleVec *othertimes = other->times();
  if(!othertimes->empty()) {
    for(DoubleVec::const_iterator t=othertimes->begin(); 
	t<othertimes->end(); ++t)
      {
	other->restore_(*t);	// read from other cache
	record();		// save to this cache
      }
    if(atlatest)
      restoreLatest();
    else
      restore_(time);
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

MemoryDataCache::MemoryDataCache() {}

MemoryDataCache::~MemoryDataCache() {}

bool MemoryDataCache::checkTime(double time) const {
  DataCache::const_iterator i = cache.find(time);
  return (i != cache.end());
}

DoubleVec *MemoryDataCache::allTimes() const {
  DoubleVec *times = new DoubleVec;
  for(DataCache::const_iterator i=cache.begin(); i!= cache.end(); ++i)
    times->push_back((*i).first);
  return times;
}

DoubleVec &MemoryDataCache::fetchOne(double time) {
  DataCache::iterator i = cache.find(time);
  if(i == cache.end())
    throw ErrProgrammingError(
		     "Attempt to restore nonexistent time! " + to_string(time),
		     __FILE__, __LINE__);
  return (*i).second;
}

void MemoryDataCache::restore_(double time) {
  DoubleVec &dofs = fetchOne(time);
  unsigned int n = mesh->dofvalues->size();
  if(n < dofs.size())
    // Fields have been deleted since this data was cached.  We can't
    // load it.  This should never happen -- the cache should be
    // cleared when fields are deleted.
    throw ErrProgrammingError("Attempt to set wrong number of values: expected "
			      + to_string(n) + ", got "
			      + to_string(dofs.size()), __FILE__, __LINE__);
  if(n > dofs.size())
    // Fields have been added since this data was cached.  New dofs
    // are added at the end of the list, so just assume their value is
    // zero.
    dofs.resize(n, 0.0);
  saveLatest();
  mesh->setCurrentTime(time);
  mesh->dofvalues = &dofs;
}

void MemoryDataCache::record() {
  double time = mesh->getCurrentTime();
  // This checks to see if we already have data for the current time.
  // If the cache is cleared properly in the Solve menu item, there
  // should never be pre-existing data. But it probably doesn't hurt
  // to check.
  DataCache::iterator i = cache.find(time);
  if(i == cache.end()) {
    cache[time] = DoubleVec();
    storedofs(cache[time]);
    add_time(time);
  }
  else {			// time has been recorded before
    storedofs((*i).second);
  }
}

void MemoryDataCache::storedofs(DoubleVec& dofs) {
  // Copy data out of mesh and into the given vector.
  unsigned int n = mesh->dofvalues->size();
  dofs.resize(n);
  memcpy(&dofs[0], &(*mesh->dofvalues)[0], n*sizeof(double));
}

void MemoryDataCache::clear() {
  restoreLatest();
  cache.clear();
  clear_times();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// nCaches is the total number of DiskDataCaches ever created. It
// doesn't have to be decremented when they are destroyed.
int DiskDataCache::nCaches = 0;

bool DiskDataCache::lt::operator()(const DiskDataCache *a,
				   const DiskDataCache *b)
  const
{
  return a->cacheID < b->cacheID;
}

std::set<DiskDataCache*, DiskDataCache::lt> DiskDataCache::allCaches;
bool DiskDataCache::initialized = false;

DiskDataCache::DiskDataCache()
  : cacheID(nCaches++)
{
  if(!initialized) {
    initialized = true;
    atexit(cleanUpDDcaches);
  }
  allCaches.insert(this);
}

void cleanUpDDcaches() {
  // Called at exit to make sure no temp files remain.
  for(std::set<DiskDataCache*>::iterator i=DiskDataCache::allCaches.begin();
      i!=DiskDataCache::allCaches.end(); ++i)
    {
      (*i)->clear_(true);	// true ==> forcibly remove files, error or not
    }
}

DiskDataCache::~DiskDataCache() {
  clear();
  allCaches.erase(this);
}

void DiskDataCache::clear() {
  restoreLatest();
  clear_(false);		// false ==> stop on error
}

void DiskDataCache::clear_(bool force) {
  for(FileDict::iterator i=fileDict.begin(); i!=fileDict.end(); ++i) {
    if(unlink((*i).second.c_str())) {	// removes file
      // Error removing file.  Ignore it if force==true.
      if(!force) {
	char buf[1000];
	(void) strerror_r(errno, buf, sizeof(buf));
	throw ErrProgrammingError(buf, __FILE__, __LINE__);
      }
    }
  }
  fileDict.clear();
  clear_times();
}

bool DiskDataCache::checkTime(double time) const {
  FileDict::const_iterator i = fileDict.find(time);
  return (i != fileDict.end());
}

DoubleVec *DiskDataCache::allTimes() const {
  DoubleVec *times = new DoubleVec;
  for(FileDict::const_iterator i = fileDict.begin(); i != fileDict.end(); ++i)
    times->push_back((*i).first);
  return times;
}

DoubleVec& DiskDataCache::fetchOne(double time) {
  unsigned int n = mesh->dofvalues->size();
  // Find the name of the file storing data for this time.
  FileDict::const_iterator i = fileDict.find(time);
  if(i == fileDict.end()) 
    throw ErrProgrammingError("Attempt to restore nonexistent time!",
			      __FILE__, __LINE__);
  // Open the file for reading
  FILE *file = fopen((*i).second.c_str(), "r");
  if(!file) {
    char buf[1000];
    (void) strerror_r(errno, buf, sizeof(buf));
    throw ErrProgrammingError(buf, __FILE__, __LINE__);
  }
  // Read the number of dof values from the file
  unsigned int nfile;
  if(fread(&nfile, sizeof(int), 1, file) != 1)
    throw ErrProgrammingError("Can't read size of cache file!",
			      __FILE__, __LINE__);
  if(n < nfile) 
    // Fields have been deleted from the mesh since this data was
    // cached.  We can't load it.  This shouldn't happen: the cache
    // should have been cleared when fields were deleted.
    throw ErrProgrammingError("Attempt to set wrong number of values",
			       __FILE__, __LINE__);
    
  localdata.clear();
  // If nfile < dofvalues->size(), then new fields have been defined since
  // this data was cached.  The new fields are at the end of the list,
  // so we just fill the list with zeros.
  if(n > nfile)
    localdata.resize(n, 0.0);
  // Read data
  if(fread(&localdata[0], sizeof(double), nfile, file) != nfile) {
    if(feof(file))
      throw ErrProgrammingError("Unexpected EOF in file " + (*i).second,
				__FILE__,  __LINE__);
    throw ErrProgrammingError("Error reading file " + (*i).second,
			      __FILE__, __LINE__);
  }
  fclose(file);
  return localdata;
}

void DiskDataCache::restore_(double time) {
  (void) fetchOne(time);	// loads localdata
  saveLatest();
  mesh->dofvalues = &localdata;
  mesh->setCurrentTime(time);
}

// Get the name of the temp directory.  This routine is used in
// DiskDataCache::record.  It's compatible with python's
// tempfile.mkstemp function, except that it uses the OOFTMP
// environment variable before the ones used by python's mkstemp.

// Environment variables that might contain a temp dir path, in the
// order checked by tempfile.mkstemp.
const char *envvars[] = {"OOFTMP", "TMPDIR", "TEMP", "TMP"};
// Directories checked by tempfile.mkstemp.
const char *tmpdirs[] = {"/tmp", "/var/tmp", "/usr/tmp"};

static std::string tempdirname() {
  for(size_t i=0; i<sizeof(envvars)/sizeof(char*); i++) {
    char *envvar = getenv(envvars[i]);
    if(envvar && !access(envvar, W_OK))
      return envvar;
  }
  struct stat statinfo;
  for(size_t i=0; i<sizeof(tmpdirs)/sizeof(char*); i++) {
    if(stat(tmpdirs[i], &statinfo) == 0) {
      if(statinfo.st_mode & S_IFDIR && !access(tmpdirs[i], W_OK))
	return tmpdirs[i];
    }
  }
  throw ErrResourceShortage(
	    "Unable to locate a writable temp directory! Try setting OOFTMP.");
}

void DiskDataCache::record() {
  double time = mesh->getCurrentTime();
  FileDict::iterator i = fileDict.find(time);
  if(i != fileDict.end()) {
    // This time has been saved before.  Delete the old file.  This
    // might never happen, but it probably doesn't hurt to check.
    if(unlink((*i).second.c_str())) {
      char buf[1000];
      (void) strerror_r(errno, buf, sizeof(buf));
      throw ErrProgrammingError(buf, __FILE__, __LINE__);
      fileDict.erase(i);
    }
  }
  else {
    add_time(time);
  }

  char filename[100];
  sprintf(filename, "%s/oof2-cache%d-XXXXXXX", tempdirname().c_str(), cacheID);
  int fd = mkstemp(filename); // get new file
  fileDict[time] = filename;
  FILE *file = fdopen(fd, "w");
  unsigned int n = mesh->dofvalues->size();
  fwrite(&n, sizeof(int), 1, file);
  if(fwrite(&(*mesh->dofvalues)[0], sizeof(double), n, file) != n) {
    throw ErrProgrammingError("Error writing cache file!", __FILE__, __LINE__);
  }
  fclose(file);
#ifdef DEBUG
  char command[200];
  sprintf(command, "wc -c %s", filename);
  FILE *ff = popen(command, "r");
  char buf[100];
  char *c = fgets(buf, sizeof(buf), ff);
  int nchars = atoi(c);
  oofcerr << "DiskDataCache::record: wrote " << nchars << " bytes ("
	  << n << " doubles) to "
	  << filename << std::endl;
#endif // DEBUG
}


