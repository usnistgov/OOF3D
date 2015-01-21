//
// typedef.i
// This file tests SWIG's typedef facility
%module typedefs
%{

typedef double Real;
typedef Real   Double;
typedef double * Array;

double * new_Array(int size) {
	return (double *) malloc(size*sizeof(double));
}

Double get_n(Array a, int n) {
	return a[n];
}

Real set_n(Real *a, int n, Real value) {
	a[n] = value;
}

void print_Array(Array a, int n) {
	int i;
	for (i = 0; i < n; i++) 
	  printf("a[%d] = %g\n", i, a[i]);
}

%}
typedef double Real;
typedef Real   Double;
typedef double * Array;

Double *new_Array(int size);
double get_n(double *a, int n);
Real set_n(Real *a, int n, Real value);
void print_Array(Double *a, int n);
void free(void *);

//
// Should generate a warning about undefined datatype
typedef  GLfloat Myfloat;

// Should be okay

typedef Real GLdouble;
typedef GLdouble Mydouble;

// Test a bunch of equivalent types

typedef  int   int1;
typedef  int   int2;
typedef  int   int3;
typedef  int   int4;
typedef  int4  int5;
typedef  int5  int6;
typedef  int6  int7;
typedef  int3  int8;

// Do a typedef'd function pointer.

typedef int (*PFI)(int,double);
typedef double ***(*PFD)(double);

void set_callback(PFI if, PFD df);

// More complicated typedef

typedef struct Vector {
	double x;
	double y;
	double z;
} Vector;

typedef union Union {
	int a;
	double b;
	char   *c;
	Matrix m;
} Union;

typedef class Class {
public:
	int member_func();
	double member_data;
} MyClass;

// Test multiple typedef's

typedef double Float, *FloatPtr, **FloatPtrPtr;

typedef struct point {
	double x,y,z;
} Point, *PointPtr;

typedef struct {
	double x,y;
} Point2, *Point2Ptr;

typedef int IntArray[32];
typedef char String[100];
typedef char *Argv[20];
typedef float OP[4];


IntArray   iarray;
String     str;
Argv       argv;

typedef int *intptr;
intptr  iarray2;

struct Test {
	IntArray a;
	String   str;
	int      b,*c,d[20];
};

// Enum

typedef enum Foo Foo;

typedef enum Foo2 {A,B,C,D } Foo2;

