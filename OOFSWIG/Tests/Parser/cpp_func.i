//
// cpp_func.i
// This file tests the SWIG parser on C++ class member
// functions and other C++ style declarations.
// 
// This file is pretty ugly---but most parser tests
// probably are....

%module cppfunc

// Note : SWIG should ignore inline code with C++ declarations.

class Func {
public:
  Func(double v) { a = v;}
  ~Func() {};
  double add(double b) { return (a = a+b);}   // A typical member function
  double abs(void) const { return fabs(a); }  // A constant function
static double mul(double a, double b) { return a*b;} // A static function
  double sub(double &b) { return (a = a-b);}  // A function with a reference
  double &new_double(double v) {              // A function returning a reference
    double *a = new double;
    *a = v;
    return &(*a);
  }
};

//
// Try an out of class static function

double Func::div(double,double);

// Try a forward class reference

class Func4;

/* A class to exercise all (well, most) of the basic datatypes */
class Func2 {
public:
  int add_int(int a, int b) {return a+b;}
  short add_short(short a, short b) { return a+b;}
  long  add_long(long a, long b) {return a+b;}
  unsigned int add_uint(unsigned int a, unsigned int b) {return a+b;}
  unsigned short add_ushort(unsigned short a, unsigned short b) {return a+b;}
  unsigned long add_ulong(unsigned long a, unsigned long b) { return a+b;}
  unsigned char add_uchar(unsigned char a, unsigned char b) { return a+b;}
  signed char add_char(signed char a, signed char b) {return a+b;}
  float  add_float(float a, float b) { return a+b;}
  double add_double(double a, double b) {return a+b;}
  void   hello(void) { printf("Hello world.\n");}
  
  //
  // Some pointer arguments
  
  int *nothing_pint(int *a, int *b) {return a;}
  short *nothing_pshort(short *a, short *b) {return a;}
  long *nothing_plong(long *a, long *b) {return a;}
  unsigned int *nothing_puint(unsigned int *a, unsigned int *b) { return a;}
  unsigned short *nothing_pushort(unsigned short *a, unsigned short *b) { return a;}
  unsigned long *nothing_pulong(unsigned long *a, unsigned long *b) { return a;}
  unsigned char *nothing_puchar(unsigned char *a, unsigned char *b) {return a;}
  signed char *nothing_pschar(signed char *a, signed char *b) {return a};
  float *nothing_pfloat(float *a, float *b) {return a;}
  double *nothing_pdouble(double *a, double *b) {return b;}
  void print(char *s) {printf("%s\n", s);}

  //
  // Some references

  int &ref_int(int &a) { return a;}
  short &ref_short(short &a) { return a;}
  long  &ref_long(long &a) {return a;}
  unsigned int &ref_uint(unsigned int &a) {return a;}
  unsigned short &ref_ushort(unsigned short &a) {return a;}
  unsigned long &ref_ulong(unsigned long &a) {return a;}
  unsigned char &ref_uchar(unsigned char &a) {return a;}
  signed char &ref_schar(signed char &a) {return a;}
  float &ref_float(float &a) {return a;}
  double &ref_double(double &a) {return a;}
  char &ref_char(char &a) {return a;}
};









