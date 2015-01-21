// -*- C++ -*-
// $RCSfile: findgauss.C,v $
// $Revision: 1.1 $
// $Author: roosen $
// $Date: 2001/11/30 19:59:09 $

// Find Gauss-Legendre integration points and weights
// Based on the Numerical Recipes routine gauleg

// compile with
// CC -o findgauss findgauss.C -LANG:std -lm

#include <iostream>
#include <vector>
#include <math.h>
#include <iomanip>
using namespace std;

#define EPS 3.e-13

struct GaussPoint {
  double x;
  double w;
};

vector<GaussPoint> gauleg(double x1, double x2, int n) {
  
  vector<GaussPoint> gp(n);

  int m = (n+1)/2;

  double xm = 0.5*(x1 + x2);
  double xl = 0.5*(x2 - x1);

  for(int i=0; i<m; i++) {	// Loop over desired roots
    double z = cos(M_PI*(i + 0.75)/(n + 0.5)); // approximate root
    double z1, pp;
    do {			// refine by Newton's method
      double p1 = 1.0;
      double p2 = 0.0;
      for(int j=1; j<=n; j++) {
	double p3 = p2;
	p2 = p1;
	p1 = ((2.0*j - 1.0)*z*p2 - (j-1.0)*p3)/j;
      }
      // p1 is the desired Legendre polynomial
      pp = n*(z*p1 - p2)/(z*z - 1.0);// derivative of Legendre polynomial
      z1 = z;
      z = z1 - p1/pp;		// Newton's method
    } while (fabs(z-z1) > EPS);
    gp[i].x = xm - xl*z;
    gp[n-i-1].x = xm + xl*z;
    gp[i].w = 2.0*xl/((1.0 - z*z)*pp*pp);
    gp[n-i-1].w = gp[i].w;
  }

  return gp;
}

int main(int argc, char *argv[]) {
  int nmin = atoi(argv[1]);
  int nmax = atoi(argv[2]);
  for(int n=nmin; n<=nmax; n++) {
    cout << "table.push_back(GaussPtTable1(" << n << ", " << n << "));" << endl;
    vector<GaussPoint> gp = gauleg(-1.0, 1.0, n);
    for(int i=0; i<n; i++)
      cout << "table[" << n << "].addpoint("
	   << setw(20) << setprecision(13) 
	   << gp[i].x << ", " << gp[i].w << ");" << endl;
    cout << endl;
  }
  return 0;
}
