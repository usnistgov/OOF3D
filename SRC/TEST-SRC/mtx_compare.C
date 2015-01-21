// -*- C++ -*-
// $RCSfile: mtx_compare.C,v $
// $Revision: 1.3.142.1 $
// $Author: langer $
// $Date: 2014/09/27 22:33:38 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

// Read two matrix files and compare them. The files should contain
// sparse matrices in coord format (i j m_ij).

#include <oofconfig.h>

#include "sparselink.h"
#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <unistd.h>
#ifdef HAVE_SSTREAM
#include <sstream>
#else  // !HAVE_SSTREAM
#include <strstream.h>
#endif // HAVE_SSTREAM
#include <string>
#include <ctype.h>
#include <math.h>

using namespace std;

double tolerance = 0;

SparseLinkMatrix<double> *readmtx(istream &is) {
  SparseLinkMatrix<double> *mat = new SparseLinkMatrix<double>;
  string line;
  while(is) {
    getline(is, line);
    if(!is) return mat;
    if(isalpha(line[0])) continue;
#ifdef HAVE_SSTREAM
    istringstream iss(line);
#else  // !HAVE_SSTREAM
    istrstream iss(line.c_str());
#endif // HAVE_SSTREAM
    int i, j;
    double x;
    iss >> i >> j >> x;
    if(iss)
      (*mat)(i, j) = x;
  }
  return mat;
}

void usage() {
  cerr << "Usage: mtx_compare [-t tolerance] file1 file2" << endl;
}

bool compare(const SparseLinkMatrix<double> &mat1,
	     const SparseLinkMatrix<double> &mat2)
{
  bool ok = true;
  for(SparseLinkMatrix<double>::const_iterator iter=mat1.begin();
      iter<mat1.end(); ++iter)
    {
    //  while(iter1(i, j, x)) {
      int i = iter.row();
      int j = iter.col();
      double x1 = *iter;
      double x2 = mat2(i, j);
      double diff = fabs(x1-x2);
      double max = (fabs(x1) > fabs(x2) ? fabs(x1) : fabs(x2));
      if(diff > 0 && diff > tolerance && diff/max > tolerance) {
	cout << i << " " << j << " " << mat1(i, j)
	     << " != " << mat2(i, j) << endl;
	ok = false;
    }
  }
  return ok;
}

int main(int argc, char *argv[]) {
  extern char *optarg;
  extern int optind;
  int c;
  while((c = getopt(argc, argv, "t:")) != -1) {
    switch(c) {
    case 't':
      tolerance = atof(optarg);
      break;
    case '?':
      usage();
      exit(1);
    }
  }

  if(optind != argc - 2) {
    usage();
    exit(-1);
  }

  SparseLinkMatrix<double> *mat1, *mat2;

  string file1 = argv[argc-2];
  if(file1 == "-") {
    mat1 = readmtx(cin);
  }
  else {
    ifstream f1(file1.c_str());
    if(!f1) {
      cerr << "Can't open file " << file1 << "!" << endl;
      exit(-1);
    }
    mat1 = readmtx(f1);
  }

  string file2 = argv[argc-1];
  if(file2 == "-" && file1 != "-") {
    mat2 = readmtx(cin);
  }
  else {
    ifstream f2(file2.c_str());
    if(!f2) {
      cerr << "Can't open file " << file2 << "!" << endl;
      exit(-1);
    }
    mat2 = readmtx(f2);
  }

  // have to compare twice, since compare() only looks at entries that
  // are non-zero in its first argument.
  if(compare(*mat1, *mat2) && compare(*mat2, *mat1)) {
    cerr << "ok" << endl;
    return 1;
  }
  cerr << "not ok" << endl;
  return 0;
}
