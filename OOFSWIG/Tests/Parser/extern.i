%module ex

// This tests SWIG's parsing of "extern" declarations.

extern int foo;                // Basic extern
extern int foo1,foo2;          // Multiple 
extern int bar(int);           // extern function
extern int bar1(int),bar2(double);
extern "C" int grok(int);      // C++ --> C extern
extern "C" {
int    flob(int);
}
extern double &foo3(double &, int &a);



