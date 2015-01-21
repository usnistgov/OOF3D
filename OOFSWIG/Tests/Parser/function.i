//
// function.i
// SWIG interface file to test basic C function declarations
//
%module function

char           *getenv(char *envvar);
void           hello(void);
int            sum_int(int a, int b);
short          sum_short(short a, short b);
long           sum_long(long a, long b);
unsigned int   sum_uint(unsigned int a, unsigned int b);
unsigned short sum_ushort(unsigned short a, unsigned short b);
unsigned long  sum_ulong(unsigned long a, unsigned long b);
unsigned char  sum_uchar(unsigned char a, unsigned char b);
signed int     sum_sint(signed int a, signed int b);
signed short   sum_sshort(signed short a, signed short b);
signed long    sum_slong(signed long a, signed long b);
signed char    sum_schar(signed char a, signed char b);
float          sum_float(float a, float b);
double         sum_double(double a, double b);

void prints(char *s);
void printc(char c);

/* Now some pointer variables to test */

int              *sum_pint(int *a, int *b);
short            *sum_pshort(short *a, short *b);
long             *sum_plong(long *, long *b);
unsigned int     *sum_puint(unsigned int *a, unsigned int *b);
unsigned short   *sum_pushort(unsigned short *a, unsigned short *b);
unsigned long    *sum_pulong(unsigned long *a, unsigned long *b);
unsigned char    *sum_puchar(unsigned char *a, unsigned char *b);
signed int       *sum_psint(signed int *a, signed int *b);
signed short     *sum_psshort(signed short *a, signed short *b);
signed long      *sum_pslong(signed long *a, signed long *b);
signed char      *sum_pschar(signed char *a, signed char *b);
float            *sum_pfloat(float *a, float *b);
double           *sum_pdouble(double *a, double *b);
void             *incr_ptr(void *a, int incr);

Vector *  new_Vector(double x, double y, double z);
void      print_Vector(Vector *v);
Vector    addv(Vector v1, Vector v2);
int       *new_int(int a);
short     *new_short(short a);
long *new_long(long a);
unsigned int *new_uint(unsigned int a);
unsigned short *new_ushort(unsigned short a);
unsigned long *new_ulong(unsigned long a);
unsigned char *new_uchar(unsigned char a);
signed int *new_sint(signed int a);
signed short *new_sshort(signed short a);
signed long *new_slong(signed long a);
signed char *new_schar(signed char a);

float *new_float(float a);
double *new_double(double a);
void *malloc(int);

// Test some complex datatypes

struct Foo func(struct Foo);
class Bar func1(class Bar *);
union Grok func2(union Grok *);

enum Enum func3(enum Enum2);

