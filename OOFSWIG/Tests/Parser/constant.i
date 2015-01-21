//
// This file tests SWIG's ability to handle constants
// and enums.
//
%module constant
%{

enum months {JAN, FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC};
#define test_value 4

typedef struct Vector {
	double x,y,z;
} Vector;	

Vector v1;

int const_foo(int a, int b) {
	return a + b;
};

typedef int (*PFOO)(int, int);

%}

// Hammer on #define a little bit....

#define  ICON1     42
#define  ICON2     -13
#define  FCON1     3.14159
#define  FCON2     2.134e3
#define  FCON3     2e3
#define  FCON4     2e+3
#define  FCON5     2e-3
#define  FCON6     -3e-7
#define  CCON1     'a'
#define  SCON1     "hello world"
#define  CCON2     '\n'
#define  CCON3     '\123'
#define  CCON4     '\x13'
#define  FCON65    .53
//
// Now try some more complicated constants

#define  SIZE_INT   sizeof(int)
#define  IEXPR      2+3
#define  IEXPR2     2*3
#define  IEXPR3     3-2
#define  IEXPR4     3/2
#define  IEXPR5     (2+3)
#define  IEXPR6     (2+3*(IEXPR))/4

#define  FEXPR      3.14159*2.3
#define  FEXPR2     FCON1/FCON2
#define  FEXPR3     (2.1+3.5*7.4)*2.1

#define  FEXPR4     3.14+2
#define  FEXPR5     8.89 + IEXPR

// Now do some bit twiddling

#define  BCON1      0x3f & 0x8
#define  BCON2      0x3f | 0x822
#define  BCON3      0x3f ^ 0x822
#define  BCON4      ~0x3f
#define  BCON5      0x3f << 4
#define  BCON6      0x3f >> 4
#define  BCON7      (1 << 8) | (1 << 7) | (1 << 6)
#define  BCON8      BCON7 & BCON6

// Now do some enums

enum months {JAN, FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC};
enum flags {READ = 0x1, WRITE = 0x2, USER = 0x4, SUPER = 0x8};
enum expr {ECON1 = 4, ECON2 = ECON1 + 2, ECON3 = ECON1 | ECON2};

// Now do some C++ style constants

const int cpp_int = 6;
const double cpp_double = 3.14159;
const int test_value;
const char *cpp_char = "Hello world";

// Test out constant suffixes

#define  UINT   2400000000U
#define  LONG   2100000000L
#define  ULONG  4000000000UL
#define  ULONG2 4100000000LU
#define  FCON7  4f
#define  FCON8  4.76F
#define  FCON9  5e-34F
#define  FCON10 7.88234E+3L

#define  UINT2   2400U + 2300U - 14U

// Test the creation of a callback function

typedef int (*PFOO)(int, int);

const PFOO FOO_CALLBACK = const_foo;
const Vector *vecaddr = &v1;

// Test type casts in expressions

#define  CAST1   (int)4
#define  CAST2   (double)4
#define  CAST3   ((float) 3.14159)

typedef double Real;

typedef double FooBar;

#define  CAST4   (Real) 2.71828
#define  CAST5   (FooBar) 2.66

// Test casts in expressions

#define  CAST6   (3 + (short) 2)
#define  CAST7   (13 + (int) 3.82930)

const int CAST8 = (FooBar) 7.8;

// Test cases in other expressions

enum cast {
	ECAST1 = 3,
	ECAST2 = (short) 4,
	ECAST3 = (signed char) 2,
	ECAST4 = (long) -7,
	ECAST8 = (int) ((FooBar) 5)
};

// Test constants with comments

#define COMMENT1    1      // A Constant
#define COMMENT2    "foo"  // A Constant


