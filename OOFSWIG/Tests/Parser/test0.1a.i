// SWIG Testing File
// This file is used for two purposes :
//     1.  Testing the SWIG parser
//     2.  Examples of valid SWIG declarations
//
// You can use it as a guide to see what's legal
// in SWIG.
//
// The entire contents of this file should parse.
// Some scripting languages will generate warning
// messages, but you should get no syntax errors or
// type errors.

%title "SWIG Examples"
%init   SWIG_Init

%{
/* Put C headers and code here */
#include <stdlib.h>
#include <time.h>

int fact(int n) {
	if (n <= 1) return 1;
	else return n*fact(n-1);
}
%}

%section "Functions"

// Void functions

extern  void print_hello(void);       // void-type, print's hello world
extern  void print_hello2();          // void-type, print's hello world again

// Functions involving the basic data types

extern     int               sum_int(int a, int b); 
extern     short             sum_short(short a, short b);
extern     long              sum_long(long a, long b);
extern     unsigned int      sum_uint(unsigned int a, unsigned int b);
extern     unsigned short    sum_ushort(unsigned short a, unsigned short b);
extern     unsigned long     sum_ulong(unsigned long a, unsigned long b);
extern     unsigned char     sum_uchar(unsigned char a, unsigned char b);
extern     signed int        sum_sint(signed int a, signed int b);
extern     signed short      sum_sshort(signed short a, signed short b);
extern     signed long       sum_slong(signed long a, signed long b);
extern     signed char       sum_schar(signed char a, signed char b);
extern     float             sum_float(float a, float b);
extern     double            sum_double(double a, double b);
extern     void              print_string(char *);
extern     void              print_char(char);
extern     char              get_char();
extern     char             *get_time();

//
// Functions involving pointers

extern     int              *sum_pint(int *a, int *b);
extern     short            *sum_pshort(int *a, int *b);
extern     long             *sum_plong(long *, long *b);
extern     unsigned int     *sum_puint(unsigned int *, unsigned int *);
extern     unsigned short   *sum_pushort(unsigned short *, unsigned short *);
extern     unsigned long    *sum_pulong(unsigned long *, unsigned long *);
extern     unsigned char    *sum_puchar(unsigned char *, unsigned char *);
extern     signed int       *sum_psint(signed int *, signed int *);
extern     signed short     *sum_psshort(signed short *, signed short *);
extern     signed long      *sum_pslong(signed long *, signed long *);
extern     signed char      *sum_pschar(signed char *, signed char *);
extern     float            *sum_pfloat(float *, float *);
extern     double           *sum_pdouble(double *, double *);
extern     void             *incr_ptr(void *, int incr);

//
// Functions involving complex data types

extern     Vector           *createv(double x, double y, double z);
extern     void              printv(Vector *v);
extern     void              sumv(Vector *a, Vector *b, Vector *c);
extern     void              sumv_val(Vector a, Vector b, Vector *c);

//
// Typedefs

typedef  unsigned char byte;
typedef  byte  *Buffer;
typedef  struct tm Tm;
typedef  unsigned long time_t;
typedef  unsigned int size_t;

Tm *gmtime(const Tm *tp);
size_t fread(void *, size_t size, size_t nobj, FILE *stream);
int  write_data(Buffer, size_t nbytes);

//
// Functions involving const and struct keywords

int strcmp(const char *s1, const char *s2);
struct tm *localtime(const time_t *tp);
char      *asctime(const struct tm *tp);

//
// Calling a function with pointer arguments by value

extern     int               sum_ref(%val int *a, %val int *b);

//
// Function renaming

%name(new_int) extern int old_int;
%name(new_func) extern int old_func(int a, int b); 

//
// Test multiple functions on same line

int   foo1(int), foo2(int), *foo3(int), foo4(int);

//
// Test a long parameter list

int   bar(int, signed int, unsigned int, short, unsigned short,
	  signed short, long, unsigned long, signed long,
	  double, float, char, unsigned char, signed char,
	  FILE *, int *, signed int *, unsigned int *, short *,
	  unsigned short *, signed short *, long *, unsigned long *,
	  signed long *, double *, float *, char *, unsigned char *,
	  signed char *, %val time_t *, int *****);

// Test variable linkage

%section "Variables"

extern       int              v_int;        // integer
extern       short            v_short;      // short
extern       long             v_long;       // long
extern       unsigned int     v_uint;       // unsigned int
extern       unsigned short   v_ushort;     // unsigned short
extern       unsigned long    v_ulong;      // unsigned long
extern       unsigned char    v_uchar;      // unsigned char
extern       signed int       v_sint;       // signed int
extern       signed short     v_sshort;     // signed short
extern       signed long      v_slong;      // signed long
extern       signed char      v_schar;      // signed char
extern       float            v_float;      // float
extern       double           v_double;     // double
extern       char             v_char;       // character
extern       char            *v_string;     // string

// Pointer types


extern       int              *p_int;       // integer pointer
extern       short            *p_short;     // short pointer
extern       long             *p_long;      // long pointer
extern       unsigned int     *p_uint;      // unsigned int pointer
extern       unsigned short   *p_ushort;    // unsigned short pointer
extern       unsigned long    *p_ulong;     // unsigned long pointer
extern       unsigned char    *p_uchar;     // unsigned char pointer
extern       signed int       *p_sint;      // signed int pointer
extern       signed short     *p_sshort;    // signed short pointer
extern       signed long      *p_slong;     // signed long pointer
extern       signed char      *p_schar;     // signed char pointer
extern       float            *p_float;     // float pointer
extern       double           *p_double;    // double pointer

// Complex datatypes

extern       Vector            v_vector;    // Should be an error
extern       Vector           *p_vector;    // Might be supported

// typedefs

typedef size_t size2_t;

extern      size_t             v_size_t;    // size_t (should be unsigned int)
extern      size2_t            v_size2_t;   // Still should be an unsigned int
extern      time_t             v_time_t;    // time_t

// This tests a declaration list

extern      int   l_int1, l_int2, l_int3, l_int4,
                 *p_int1, *p_int2, *p_int3, *p_int4;  

#define  ICON1     42
// Doc : ICON1
#define  ICON2     -13
// Doc : ICON2
#define  FCON1     3.14159
// Doc : FCON1
#define  FCON2     2.134e3
// Doc : FCON2
#define  FCON3     2e3
// Doc : FCON3
#define  FCON4     2e+3
#define  FCON5     2e-3
#define  FCON6     -3e-7
#define  CCON1     'a'
#define  SCON1     "hello world"
#define  CCON2     '\n'
#define  CCON3     '\123'
#define  CCON4     '\x13'

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
#define  BCON7      (1 << 8) \
                  | (1 << 7) \
                  | (1 << 6)

#define  BCON8      BCON7 & BCON6

// Miscellaneous

%{

/* This should insert a comment into the header/wrapper
   function part of the file */

%}

%init %{

/* This should insert a comment into the SWIG initialization
   function

*/

%}






