/* DEBUG : Language specific headers go here */

/* DEBUG : Pointer conversion function here */

/* DEBUG : Language specific code here */

#define   SWIG_init     swig_init

#define   SWIG_name    "swig"
WRAPPER : char *getenv(char *);

WRAPPER : void hello();

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

WRAPPER : void prints(char *);

WRAPPER : void printc(char );

WRAPPER : int *sum_pint(int *,int *);

WRAPPER : short *sum_pshort(short *,short *);

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

WRAPPER : Vector *new_Vector(double ,double ,double );

WRAPPER : void print_Vector(Vector *);

WRAPPER : Vector addv(Vector ,Vector );

WRAPPER : int *new_int(int );

WRAPPER : short *new_short(short );

WRAPPER : long *new_long(long );

WRAPPER : unsigned int *new_uint(unsigned int );

WRAPPER : unsigned short *new_ushort(unsigned short );

WRAPPER : unsigned long *new_ulong(unsigned long );

WRAPPER : unsigned char *new_uchar(unsigned char );

WRAPPER : signed int *new_sint(signed int );

WRAPPER : signed short *new_sshort(signed short );

WRAPPER : signed long *new_slong(signed long );

WRAPPER : signed char *new_schar(signed char );

WRAPPER : float *new_float(float );

WRAPPER : double *new_double(double );

WRAPPER : void *malloc(int );

WRAPPER : struct Foo func(struct Foo );

WRAPPER : class Bar func1(class Bar *);

WRAPPER : union Grok func2(union Grok *);

WRAPPER : enum Enum func3(enum Enum2 );

SWIG POINTER-MAPPING TABLE

/*
 * This table is used by the pointer type-checker
 */
static struct { char *n1; char *n2; void *(*pcnv)(void *); } _swig_mapping[] = {
    { "_signed_long","_long",0},
    { "_long","_unsigned_long",0},
    { "_long","_signed_long",0},
    { "_unsigned_long","_long",0},
    { "_signed_int","_int",0},
    { "_unsigned_short","_short",0},
    { "_signed_short","_short",0},
    { "_unsigned_int","_int",0},
    { "_short","_unsigned_short",0},
    { "_short","_signed_short",0},
    { "_int","_unsigned_int",0},
    { "_int","_signed_int",0},
{0,0,0}};


/* MODULE INITIALIZATION */

void swig_init() {
     ADD COMMAND    : getenv --> char *getenv(char *);
     ADD COMMAND    : hello --> void hello();
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
     ADD COMMAND    : prints --> void prints(char *);
     ADD COMMAND    : printc --> void printc(char );
     ADD COMMAND    : sum_pint --> int *sum_pint(int *,int *);
     ADD COMMAND    : sum_pshort --> short *sum_pshort(short *,short *);
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
     ADD COMMAND    : new_Vector --> Vector *new_Vector(double ,double ,double );
     ADD COMMAND    : print_Vector --> void print_Vector(Vector *);
     ADD COMMAND    : addv --> Vector addv(Vector ,Vector );
     ADD COMMAND    : new_int --> int *new_int(int );
     ADD COMMAND    : new_short --> short *new_short(short );
     ADD COMMAND    : new_long --> long *new_long(long );
     ADD COMMAND    : new_uint --> unsigned int *new_uint(unsigned int );
     ADD COMMAND    : new_ushort --> unsigned short *new_ushort(unsigned short );
     ADD COMMAND    : new_ulong --> unsigned long *new_ulong(unsigned long );
     ADD COMMAND    : new_uchar --> unsigned char *new_uchar(unsigned char );
     ADD COMMAND    : new_sint --> signed int *new_sint(signed int );
     ADD COMMAND    : new_sshort --> signed short *new_sshort(signed short );
     ADD COMMAND    : new_slong --> signed long *new_slong(signed long );
     ADD COMMAND    : new_schar --> signed char *new_schar(signed char );
     ADD COMMAND    : new_float --> float *new_float(float );
     ADD COMMAND    : new_double --> double *new_double(double );
     ADD COMMAND    : malloc --> void *malloc(int );
     ADD COMMAND    : func --> struct Foo func(struct Foo );
     ADD COMMAND    : func1 --> class Bar func1(class Bar *);
     ADD COMMAND    : func2 --> union Grok func2(union Grok *);
     ADD COMMAND    : func3 --> enum Enum func3(enum Enum2 );
}  /* END INIT */
{
   int i;
   for (i = 0; _swig_mapping[i].n1; i++)
        SWIG_RegisterMapping(_swig_mapping[i].n1,_swig_mapping[i].n2,_swig_mapping[i].pcnv);
}
