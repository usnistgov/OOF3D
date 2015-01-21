/* DEBUG : Language specific headers go here */

/* DEBUG : Pointer conversion function here */

/* DEBUG : Language specific code here */

#define   SWIG_init     swig_init

#define   SWIG_name    "swig"

/* Put C headers and code here */
#include <stdlib.h>
#include <time.h>

int fact(int n) {
	if (n <= 1) return 1;
	else return n*fact(n-1);
}
extern void print_hello();
extern void print_hello2();
extern int sum_int(int ,int );
extern short sum_short(short ,short );
extern long sum_long(long ,long );
extern unsigned int sum_uint(unsigned int ,unsigned int );
extern unsigned short sum_ushort(unsigned short ,unsigned short );
extern unsigned long sum_ulong(unsigned long ,unsigned long );
extern unsigned char sum_uchar(unsigned char ,unsigned char );
extern signed int sum_sint(signed int ,signed int );
extern signed short sum_sshort(signed short ,signed short );
extern signed long sum_slong(signed long ,signed long );
extern signed char sum_schar(signed char ,signed char );
extern float sum_float(float ,float );
extern double sum_double(double ,double );
extern void print_string(char *);
extern void print_char(char );
extern char get_char();
extern char *get_time();
extern int *sum_pint(int *,int *);
extern short *sum_pshort(int *,int *);
extern long *sum_plong(long *,long *);
extern unsigned int *sum_puint(unsigned int *,unsigned int *);
extern unsigned short *sum_pushort(unsigned short *,unsigned short *);
extern unsigned long *sum_pulong(unsigned long *,unsigned long *);
extern unsigned char *sum_puchar(unsigned char *,unsigned char *);
extern signed int *sum_psint(signed int *,signed int *);
extern signed short *sum_psshort(signed short *,signed short *);
extern signed long *sum_pslong(signed long *,signed long *);
extern signed char *sum_pschar(signed char *,signed char *);
extern float *sum_pfloat(float *,float *);
extern double *sum_pdouble(double *,double *);
extern void *incr_ptr(void *,int );
extern Vector *createv(double ,double ,double );
extern void printv(Vector *);
extern void sumv(Vector *,Vector *,Vector *);
extern void sumv_val(Vector ,Vector ,Vector *);
extern int sum_ref(int *,int *);
extern int  old_int; 
extern int old_func(int ,int );
extern int  v_int; 
extern short  v_short; 
extern long  v_long; 
extern unsigned int  v_uint; 
extern unsigned short  v_ushort; 
extern unsigned long  v_ulong; 
extern unsigned char  v_uchar; 
extern signed int  v_sint; 
extern signed short  v_sshort; 
extern signed long  v_slong; 
extern signed char  v_schar; 
extern float  v_float; 
extern double  v_double; 
extern char  v_char; 
extern char * v_string; 
extern int * p_int; 
extern short * p_short; 
extern long * p_long; 
extern unsigned int * p_uint; 
extern unsigned short * p_ushort; 
extern unsigned long * p_ulong; 
extern unsigned char * p_uchar; 
extern signed int * p_sint; 
extern signed short * p_sshort; 
extern signed long * p_slong; 
extern signed char * p_schar; 
extern float * p_float; 
extern double * p_double; 
extern Vector  v_vector; 
extern Vector * p_vector; 
extern size_t  v_size_t; 
extern size2_t  v_size2_t; 
extern time_t  v_time_t; 
extern int  l_int1; 
extern int  l_int2; 
extern int  l_int3; 
extern int  l_int4; 
extern int * p_int1; 
extern int * p_int2; 
extern int * p_int3; 
extern int * p_int4; 


/* This should insert a comment into the header/wrapper
   function part of the file */

WRAPPER : void print_hello();

WRAPPER : void print_hello2();

WRAPPER : int sum_int(int ,int );

WRAPPER : short sum_short(short ,short );

WRAPPER : long sum_long(long ,long );

WRAPPER : unsigned int sum_uint(unsigned int ,unsigned int );

WRAPPER : unsigned short sum_ushort(unsigned short ,unsigned short );

WRAPPER : unsigned long sum_ulong(unsigned long ,unsigned long );

WRAPPER : unsigned char sum_uchar(unsigned char ,unsigned char );

WRAPPER : signed int sum_sint(signed int ,signed int );

WRAPPER : signed short sum_sshort(signed short ,signed short );

WRAPPER : signed long sum_slong(signed long ,signed long );

WRAPPER : signed char sum_schar(signed char ,signed char );

WRAPPER : float sum_float(float ,float );

WRAPPER : double sum_double(double ,double );

WRAPPER : void print_string(char *);

WRAPPER : void print_char(char );

WRAPPER : char get_char();

WRAPPER : char *get_time();

WRAPPER : int *sum_pint(int *,int *);

WRAPPER : short *sum_pshort(int *,int *);

WRAPPER : long *sum_plong(long *,long *);

WRAPPER : unsigned int *sum_puint(unsigned int *,unsigned int *);

WRAPPER : unsigned short *sum_pushort(unsigned short *,unsigned short *);

WRAPPER : unsigned long *sum_pulong(unsigned long *,unsigned long *);

WRAPPER : unsigned char *sum_puchar(unsigned char *,unsigned char *);

WRAPPER : signed int *sum_psint(signed int *,signed int *);

WRAPPER : signed short *sum_psshort(signed short *,signed short *);

WRAPPER : signed long *sum_pslong(signed long *,signed long *);

WRAPPER : signed char *sum_pschar(signed char *,signed char *);

WRAPPER : float *sum_pfloat(float *,float *);

WRAPPER : double *sum_pdouble(double *,double *);

WRAPPER : void *incr_ptr(void *,int );

WRAPPER : Vector *createv(double ,double ,double );

WRAPPER : void printv(Vector *);

WRAPPER : void sumv(Vector *,Vector *,Vector *);

WRAPPER : void sumv_val(Vector ,Vector ,Vector *);

WRAPPER : Tm *gmtime(const Tm *);

WRAPPER : size_t fread(void *,size_t ,size_t ,FILE *);

WRAPPER : int write_data(Buffer ,size_t );

WRAPPER : int strcmp(const char *,const char *);

WRAPPER : struct tm *localtime(const time_t *);

WRAPPER : char *asctime(const struct tm *);

WRAPPER : int sum_ref(int *,int *);

WRAPPER : int  old_int; 
WRAPPER : int old_func(int ,int );

WRAPPER : int foo1(int );

WRAPPER : int foo2(int );

WRAPPER : int *foo3(int );

WRAPPER : int foo4(int );

WRAPPER : int bar(int ,signed int ,unsigned int ,short ,unsigned short ,signed short ,long ,unsigned long ,signed long ,double ,float ,char ,unsigned char ,signed char ,FILE *,int *,signed int *,unsigned int *,short *,unsigned short *,signed short *,long *,unsigned long *,signed long *,double *,float *,char *,unsigned char *,signed char *,time_t *,int *****);

WRAPPER : int  v_int; 
WRAPPER : short  v_short; 
WRAPPER : long  v_long; 
WRAPPER : unsigned int  v_uint; 
WRAPPER : unsigned short  v_ushort; 
WRAPPER : unsigned long  v_ulong; 
WRAPPER : unsigned char  v_uchar; 
WRAPPER : signed int  v_sint; 
WRAPPER : signed short  v_sshort; 
WRAPPER : signed long  v_slong; 
WRAPPER : signed char  v_schar; 
WRAPPER : float  v_float; 
WRAPPER : double  v_double; 
WRAPPER : char  v_char; 
WRAPPER : char * v_string; 
WRAPPER : int * p_int; 
WRAPPER : short * p_short; 
WRAPPER : long * p_long; 
WRAPPER : unsigned int * p_uint; 
WRAPPER : unsigned short * p_ushort; 
WRAPPER : unsigned long * p_ulong; 
WRAPPER : unsigned char * p_uchar; 
WRAPPER : signed int * p_sint; 
WRAPPER : signed short * p_sshort; 
WRAPPER : signed long * p_slong; 
WRAPPER : signed char * p_schar; 
WRAPPER : float * p_float; 
WRAPPER : double * p_double; 
WRAPPER : Vector  v_vector; 
WRAPPER : Vector * p_vector; 
WRAPPER : size_t  v_size_t; 
WRAPPER : size2_t  v_size2_t; 
WRAPPER : time_t  v_time_t; 
WRAPPER : int  l_int1; 
WRAPPER : int  l_int2; 
WRAPPER : int  l_int3; 
WRAPPER : int  l_int4; 
WRAPPER : int * p_int1; 
WRAPPER : int * p_int2; 
WRAPPER : int * p_int3; 
WRAPPER : int * p_int4; 
SWIG POINTER-MAPPING TABLE

/*
 * This table is used by the pointer type-checker
 */
static struct { char *n1; char *n2; void *(*pcnv)(void *); } _swig_mapping[] = {
    { "_signed_long","_long",0},
    { "_struct_tm","_Tm",0},
    { "_Buffer","_byte_p",0},
    { "_byte","_unsigned_char",0},
    { "_long","_time_t",0},
    { "_long","_unsigned_long",0},
    { "_long","_signed_long",0},
    { "_size_t","_size2_t",0},
    { "_size_t","_unsigned_int",0},
    { "_size_t","_int",0},
    { "_size2_t","_size_t",0},
    { "_size2_t","_int",0},
    { "_size2_t","_unsigned_int",0},
    { "_unsigned_long","_time_t",0},
    { "_unsigned_long","_long",0},
    { "_signed_int","_int",0},
    { "_unsigned_short","_short",0},
    { "_signed_short","_short",0},
    { "_unsigned_char","_byte",0},
    { "_unsigned_int","_size2_t",0},
    { "_unsigned_int","_size_t",0},
    { "_unsigned_int","_int",0},
    { "_short","_unsigned_short",0},
    { "_short","_signed_short",0},
    { "_int","_size2_t",0},
    { "_int","_size_t",0},
    { "_int","_unsigned_int",0},
    { "_int","_signed_int",0},
    { "_time_t","_unsigned_long",0},
    { "_time_t","_long",0},
    { "_Tm","_struct_tm",0},
    { "_byte_p","_Buffer",0},
{0,0,0}};


/* MODULE INITIALIZATION */

void swig_init() {
     ADD COMMAND    : print_hello --> void print_hello();
     ADD COMMAND    : print_hello2 --> void print_hello2();
     ADD COMMAND    : sum_int --> int sum_int(int ,int );
     ADD COMMAND    : sum_short --> short sum_short(short ,short );
     ADD COMMAND    : sum_long --> long sum_long(long ,long );
     ADD COMMAND    : sum_uint --> unsigned int sum_uint(unsigned int ,unsigned int );
     ADD COMMAND    : sum_ushort --> unsigned short sum_ushort(unsigned short ,unsigned short );
     ADD COMMAND    : sum_ulong --> unsigned long sum_ulong(unsigned long ,unsigned long );
     ADD COMMAND    : sum_uchar --> unsigned char sum_uchar(unsigned char ,unsigned char );
     ADD COMMAND    : sum_sint --> signed int sum_sint(signed int ,signed int );
     ADD COMMAND    : sum_sshort --> signed short sum_sshort(signed short ,signed short );
     ADD COMMAND    : sum_slong --> signed long sum_slong(signed long ,signed long );
     ADD COMMAND    : sum_schar --> signed char sum_schar(signed char ,signed char );
     ADD COMMAND    : sum_float --> float sum_float(float ,float );
     ADD COMMAND    : sum_double --> double sum_double(double ,double );
     ADD COMMAND    : print_string --> void print_string(char *);
     ADD COMMAND    : print_char --> void print_char(char );
     ADD COMMAND    : get_char --> char get_char();
     ADD COMMAND    : get_time --> char *get_time();
     ADD COMMAND    : sum_pint --> int *sum_pint(int *,int *);
     ADD COMMAND    : sum_pshort --> short *sum_pshort(int *,int *);
     ADD COMMAND    : sum_plong --> long *sum_plong(long *,long *);
     ADD COMMAND    : sum_puint --> unsigned int *sum_puint(unsigned int *,unsigned int *);
     ADD COMMAND    : sum_pushort --> unsigned short *sum_pushort(unsigned short *,unsigned short *);
     ADD COMMAND    : sum_pulong --> unsigned long *sum_pulong(unsigned long *,unsigned long *);
     ADD COMMAND    : sum_puchar --> unsigned char *sum_puchar(unsigned char *,unsigned char *);
     ADD COMMAND    : sum_psint --> signed int *sum_psint(signed int *,signed int *);
     ADD COMMAND    : sum_psshort --> signed short *sum_psshort(signed short *,signed short *);
     ADD COMMAND    : sum_pslong --> signed long *sum_pslong(signed long *,signed long *);
     ADD COMMAND    : sum_pschar --> signed char *sum_pschar(signed char *,signed char *);
     ADD COMMAND    : sum_pfloat --> float *sum_pfloat(float *,float *);
     ADD COMMAND    : sum_pdouble --> double *sum_pdouble(double *,double *);
     ADD COMMAND    : incr_ptr --> void *incr_ptr(void *,int );
     ADD COMMAND    : createv --> Vector *createv(double ,double ,double );
     ADD COMMAND    : printv --> void printv(Vector *);
     ADD COMMAND    : sumv --> void sumv(Vector *,Vector *,Vector *);
     ADD COMMAND    : sumv_val --> void sumv_val(Vector ,Vector ,Vector *);
     ADD COMMAND    : gmtime --> Tm *gmtime(const Tm *);
     ADD COMMAND    : fread --> size_t fread(void *,size_t ,size_t ,FILE *);
     ADD COMMAND    : write_data --> int write_data(Buffer ,size_t );
     ADD COMMAND    : strcmp --> int strcmp(const char *,const char *);
     ADD COMMAND    : localtime --> struct tm *localtime(const time_t *);
     ADD COMMAND    : asctime --> char *asctime(const struct tm *);
     ADD COMMAND    : sum_ref --> int sum_ref(int *,int *);
     ADD VARIABLE   : new_int --> int  old_int; 
     ADD COMMAND    : new_func --> int old_func(int ,int );
     ADD COMMAND    : foo1 --> int foo1(int );
     ADD COMMAND    : foo2 --> int foo2(int );
     ADD COMMAND    : foo3 --> int *foo3(int );
     ADD COMMAND    : foo4 --> int foo4(int );
     ADD COMMAND    : bar --> int bar(int ,signed int ,unsigned int ,short ,unsigned short ,signed short ,long ,unsigned long ,signed long ,double ,float ,char ,unsigned char ,signed char ,FILE *,int *,signed int *,unsigned int *,short *,unsigned short *,signed short *,long *,unsigned long *,signed long *,double *,float *,char *,unsigned char *,signed char *,time_t *,int *****);
     ADD VARIABLE   : v_int --> int  v_int; 
     ADD VARIABLE   : v_short --> short  v_short; 
     ADD VARIABLE   : v_long --> long  v_long; 
     ADD VARIABLE   : v_uint --> unsigned int  v_uint; 
     ADD VARIABLE   : v_ushort --> unsigned short  v_ushort; 
     ADD VARIABLE   : v_ulong --> unsigned long  v_ulong; 
     ADD VARIABLE   : v_uchar --> unsigned char  v_uchar; 
     ADD VARIABLE   : v_sint --> signed int  v_sint; 
     ADD VARIABLE   : v_sshort --> signed short  v_sshort; 
     ADD VARIABLE   : v_slong --> signed long  v_slong; 
     ADD VARIABLE   : v_schar --> signed char  v_schar; 
     ADD VARIABLE   : v_float --> float  v_float; 
     ADD VARIABLE   : v_double --> double  v_double; 
     ADD VARIABLE   : v_char --> char  v_char; 
     ADD VARIABLE   : v_string --> char * v_string; 
     ADD VARIABLE   : p_int --> int * p_int; 
     ADD VARIABLE   : p_short --> short * p_short; 
     ADD VARIABLE   : p_long --> long * p_long; 
     ADD VARIABLE   : p_uint --> unsigned int * p_uint; 
     ADD VARIABLE   : p_ushort --> unsigned short * p_ushort; 
     ADD VARIABLE   : p_ulong --> unsigned long * p_ulong; 
     ADD VARIABLE   : p_uchar --> unsigned char * p_uchar; 
     ADD VARIABLE   : p_sint --> signed int * p_sint; 
     ADD VARIABLE   : p_sshort --> signed short * p_sshort; 
     ADD VARIABLE   : p_slong --> signed long * p_slong; 
     ADD VARIABLE   : p_schar --> signed char * p_schar; 
     ADD VARIABLE   : p_float --> float * p_float; 
     ADD VARIABLE   : p_double --> double * p_double; 
     ADD VARIABLE   : v_vector --> Vector  v_vector; 
     ADD VARIABLE   : p_vector --> Vector * p_vector; 
     ADD VARIABLE   : v_size_t --> size_t  v_size_t; 
     ADD VARIABLE   : v_size2_t --> size2_t  v_size2_t; 
     ADD VARIABLE   : v_time_t --> time_t  v_time_t; 
     ADD VARIABLE   : l_int1 --> int  l_int1; 
     ADD VARIABLE   : l_int2 --> int  l_int2; 
     ADD VARIABLE   : l_int3 --> int  l_int3; 
     ADD VARIABLE   : l_int4 --> int  l_int4; 
     ADD VARIABLE   : p_int1 --> int * p_int1; 
     ADD VARIABLE   : p_int2 --> int * p_int2; 
     ADD VARIABLE   : p_int3 --> int * p_int3; 
     ADD VARIABLE   : p_int4 --> int * p_int4; 
     ADD CONSTANT   : (int ) ICON1 = 42
     ADD CONSTANT   : (int ) ICON2 = -13
     ADD CONSTANT   : (double ) FCON1 = 3.14159
     ADD CONSTANT   : (double ) FCON2 = 2.134e3
     ADD CONSTANT   : (double ) FCON3 = 2e3
     ADD CONSTANT   : (double ) FCON4 = 2e+3
     ADD CONSTANT   : (double ) FCON5 = 2e-3
     ADD CONSTANT   : (double ) FCON6 = -3e-7
     ADD CONSTANT   : (char *) CCON1 = a
     ADD CONSTANT   : (char *) SCON1 = hello world
     ADD CONSTANT   : (char *) CCON2 = \n
     ADD CONSTANT   : (char *) CCON3 = \123
     ADD CONSTANT   : (char *) CCON4 = \x13
     ADD CONSTANT   : (int ) SIZE_INT = sizeof(int)
     ADD CONSTANT   : (int ) IEXPR = 2+3
     ADD CONSTANT   : (int ) IEXPR2 = 2*3
     ADD CONSTANT   : (int ) IEXPR3 = 3-2
     ADD CONSTANT   : (int ) IEXPR4 = 3/2
     ADD CONSTANT   : (int ) IEXPR5 = (2+3)
     ADD CONSTANT   : (int ) IEXPR6 = (2+3*((2+3)))/4
     ADD CONSTANT   : (double ) FEXPR = 3.14159*2.3
     ADD CONSTANT   : (double ) FEXPR2 = (3.14159)/(2.134e3)
     ADD CONSTANT   : (double ) FEXPR3 = (2.1+3.5*7.4)*2.1
     ADD CONSTANT   : (double ) FEXPR4 = 3.14+2
     ADD CONSTANT   : (double ) FEXPR5 = 8.89+(2+3)
     ADD CONSTANT   : (int ) BCON1 = 0x3f&0x8
     ADD CONSTANT   : (int ) BCON2 = 0x3f|0x822
     ADD CONSTANT   : (int ) BCON3 = 0x3f^0x822
     ADD CONSTANT   : (int ) BCON4 = ~0x3f
     ADD CONSTANT   : (int ) BCON5 = 0x3f<<4
     ADD CONSTANT   : (int ) BCON6 = 0x3f>>4
     ADD CONSTANT   : (int ) BCON7 = (1<<8)|(1<<7)|(1<<6)
     ADD CONSTANT   : (int ) BCON8 = ((1<<8)|(1<<7)|(1<<6))&(0x3f>>4)


/* This should insert a comment into the SWIG initialization
   function

*/

}  /* END INIT */
{
   int i;
   for (i = 0; _swig_mapping[i].n1; i++)
        SWIG_RegisterMapping(_swig_mapping[i].n1,_swig_mapping[i].n2,_swig_mapping[i].pcnv);
}
