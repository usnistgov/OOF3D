// Test SWIG's type-mapping support

%typemap(tcl,in) double {
	.. get a double ..
}

%typemap(tcl,out) double {
	.. set a double ..
}

%typemap(tcl,in) char ** {
	.. get a char ** ..
}

%typemap(tcl,out) char ** {
	.. set a char ** ..
}

%typemap(tcl,in) Vector & {
	.. get a vector reference ..
}

%typemap(tcl,out) Vector & {
	.. set a vector reference ..
}

%typemap(tcl,in) char **argv {
 	.. get an argv ..
}

%typemap(tcl,out) char **argv {
	.. set an argv ..
}

/* Now do some tests */

int foobar(double a, double b);
int parse_args(int argc, char **argv);
int parse_charpp(int argc, char **);

/* A C++ test */

class Foo {
public:
	double dmember(double);
	void   charpp(char **);
	Vector& get_vector();
	void set_vector(Vector&);
}

%typemap(tcl,in) double {
 get a double for class Bar
}

class Bar {
public:
       double dmember2(double);
}

// Delete double typemaps
%typemap(tcl,in) double;

void no_typemap(double);

// Some matrix typemaps

%typemap(tcl,in) double [4] {
	... get a double[4] ...
}

%typemap(tcl,in) double [4][4] {
	... get a double [4][4] ...
}

%typemap(memberin) double [4] {
	... set a double [4] member ...
}

%typemap(memberin) double [4][4] {
	... set a double [4][4] member ...

}

void atest1(double a[4]);
void atest2(double a[4][4]);
struct atest3 {
	double a[4];
	double b[4][4];
};

// Now some typemaps that match any array dimension

%typemap(tcl,in) double [ANY] {
	... getting a double [$dim0] ...

}

%typemap(tcl,in) double [ANY][8] {
	... getting a double [$dim0][8] ...
}

%typemap(tcl,in) double [7][ANY] {
	... getting a double [7][$dim1] ...
}

%typemap(memberin) double [ANY][ANY] {
	... setting a double [$dim0][$dim1] member ...
}

void atest4(double a[6]);
void atest5(double a[13][8]);
void atest6(double a[7][17]);
struct atest7 {
	double a[5][6];
	double b[10][];
};

// Try a parameterized typemap

%typemap(tcl,in) double *indouble(double temp) {
	$target = &temp;
}

void local1(double *indouble);
void local2(double *indouble, double *indouble);
void local3(double *indouble, double *indouble, double *indouble, double *indouble);

typedef double Real;

// Try out our new %apply and %clear directives
// 
// This applies all typemaps associated with double *indouble to the datatypes
// in the list.

// This applies the typemaps for double *indouble to 'double *in' and 'Real *in1'

%apply double *indouble {double *in, Real *in1};

%typemap(in) void * {
	// Get a void pointer 
}

%apply void * {Matrix *};

void apply1(double *in);
void apply2(double *in, Real *in1);
void apply3(double *in, double *in1);
void apply4(Matrix *m);

%clear double *in, double *in1;

void apply5(double *in, Real *in1, double *in2);

%apply double [4] { double *mat };

void apply6(double *mat);

// Test locals involving arrays

%typemap(in) double [4](double temp[4]) {
	... get a double [4] ...
	temp[0] = 0;
}

double array1(double a[4]);

// Make sure we get the local substitution right
double array2(double a[4], double b[4], double c[4]);


// A local variable that is a structure

%typemap(in) Vector *(Vector v) {
	$target = &v;
}

void vector1(Vector *v);

// This should set a default input method.  It will be applied to 
// all integer datatypes that don't have another typemap specified

%typemap(in) int SWIG_DEFAULT_TYPE {
	$target = get an integer from $source (DEFAULT ***)
};

typedef int Integer;
typedef Integer INT32;
void int1(int );
void int2(int a, int b);
void int3(Integer);        
void int4(Integer a, Integer b, INT32 c);

%typemap(in) INT32 {
	$target = get an INT32 from $source
}

void int5(Integer a, INT32 b);

// Try some default pointer types

%typemap(in) Pointer * SWIG_DEFAULT_TYPE {
	$target = get any pointer from $source (DEFAULT ***)
};

%typemap(in) USER SWIG_DEFAULT_TYPE {
	$target = get any user-defined type from $source (DEFAULT ***)
};

%typemap(in) int SWIG_DEFAULT_TYPE[ANY] {
	$target = get an int[$dim0] from $source (DEFAULT ***)
}

void user1(int *);
void user2(double **a);
void user3(FloatMatrix *m);
void user4(FloatMatrix);
void user5(char *);
void user6(int a[4]);
void user7(double **b[]);

// Test out creation of locals

%typemap(in) double *TEST(double temp) {
	... store a double in temp ...
}

%typemap(in) int [4](int temp[4]) {
	... store ints in temp[4] ...
}


void test1(double *TEST, int a[4], int b[4], double *TEST);

%typemap(in) Vector *a($type temp) {
	... store a vector in temp ...
}

%typemap(in) Vector *b($basetype temp) {
	... store a vector in temp ...
}

void test2(Vector *a, Vector *b);


// Test variable substitutions

%typemap(in) double a {
// in method :
	source    = $source
	target    = $target
	type      = $type
        mangle    = $mangle
        basetype  = $basetype
        name      = $name
        arg       = $arg
        argnum    = $argnum
	value     = $value
	cleanup   = $cleanup
}        

double vars1(double a);

%typemap(out) double vars2 {
// out method :
	source    = $source
	target    = $target
	type      = $type
        mangle    = $mangle
        basetype  = $basetype
        name      = $name
        arg       = $arg
        argnum    = $argnum
	value     = $value
	cleanup   = $cleanup
}        

double vars2(double);

%typemap(ret) double vars3 {
// ret method :
	source    = $source
	target    = $target
	type      = $type
        mangle    = $mangle
        basetype  = $basetype
        name      = $name
        arg       = $arg
        argnum    = $argnum
	value     = $value
	cleanup   = $cleanup
}        

double vars3(double);

%typemap(freearg) double b {
// freearg method :
	source    = $source
	target    = $target
	type      = $type
        mangle    = $mangle
        basetype  = $basetype
        name      = $name
        arg       = $arg
        argnum    = $argnum
	value     = $value
	cleanup   = $cleanup
}        

double vars4(double b);

%typemap(argout) double c {
// argout method :
	source    = $source
	target    = $target
	type      = $type
        mangle    = $mangle
        basetype  = $basetype
        name      = $name
        arg       = $arg
        argnum    = $argnum
	value     = $value
	cleanup   = $cleanup
}        

double vars5(double c);

%typemap(check) double d {
// check method :
	source    = $source
	target    = $target
	type      = $type
        mangle    = $mangle
        basetype  = $basetype
        name      = $name
        arg       = $arg
        argnum    = $argnum
	value     = $value
	cleanup   = $cleanup
}        

double vars6(double d);

%typemap(varin) double vars7 {
// varin method :
	source    = $source
	target    = $target
	type      = $type
        mangle    = $mangle
        basetype  = $basetype
        name      = $name
        arg       = $arg
        argnum    = $argnum
	value     = $value
	cleanup   = $cleanup
}        


%typemap(varout) double {
// varout method :
	source    = $source
	target    = $target
	type      = $type
        mangle    = $mangle
        basetype  = $basetype
        name      = $name
        arg       = $arg
        argnum    = $argnum
	value     = $value
	cleanup   = $cleanup
}        

double vars7;

%typemap(const) double {
// const method :
	source    = $source
	target    = $target
	type      = $type
        mangle    = $mangle
        basetype  = $basetype
        name      = $name
        arg       = $arg
        argnum    = $argnum
	value     = $value
	cleanup   = $cleanup
}        

const double vars8 = 10;

%typemap(memberin) double {
// memberin method :
	source    = $source
	target    = $target
	type      = $type
        mangle    = $mangle
        basetype  = $basetype
        name      = $name
        arg       = $arg
        argnum    = $argnum
	value     = $value
	cleanup   = $cleanup
}        

%typemap(memberout) double {
// memberout method :
	source    = $source
	target    = $target
	type      = $type
        mangle    = $mangle
        basetype  = $basetype
        name      = $name
        arg       = $arg
        argnum    = $argnum
	value     = $value
	cleanup   = $cleanup
}        


struct varstruct {
	double b;
};



%typemap(default) double e {
// default method :
	source    = $source
	target    = $target
	type      = $type
        mangle    = $mangle
        basetype  = $basetype
        name      = $name
        arg       = $arg
        argnum    = $argnum
	value     = $value
	cleanup   = $cleanup
}        

double vars9(double e);

%typemap(ignore) double f {
// ignore method :
	source    = $source
	target    = $target
	type      = $type
        mangle    = $mangle
        basetype  = $basetype
        name      = $name
        arg       = $arg
        argnum    = $argnum
	value     = $value
	cleanup   = $cleanup
}        


double vars10(double f);

