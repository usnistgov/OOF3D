/* DEBUG : Language specific headers go here */

/* DEBUG : Pointer conversion function here */

/* DEBUG : Language specific code here */

#define   SWIG_init     swig_init

#define   SWIG_name    "swig"
C++ CLASS DECLARATION : class Func
WRAPPER : double Func::div(double ,double );

C++ CLASS DECLARATION : class Func4
C++ CLASS DECLARATION : class Func2
C++ CLASS START : class Func  ========================================

        CONSTRUCTOR   : Func *Func(double );
        DESTRUCTOR    : ~Func();
        MEMBER FUNC   : double add(double );

        MEMBER FUNC   : double abs();

        STATIC FUNC   : double mul(double ,double );
        MEMBER FUNC   : double sub(double &);

        MEMBER FUNC   : double &new_double(double );

C++ CLASS END ===================================================

C++ CLASS START : class Func2  ========================================

        MEMBER FUNC   : int add_int(int ,int );

        MEMBER FUNC   : short add_short(short ,short );

        MEMBER FUNC   : long add_long(long ,long );

        MEMBER FUNC   : unsigned int add_uint(unsigned int ,unsigned int );

        MEMBER FUNC   : unsigned short add_ushort(unsigned short ,unsigned short );

        MEMBER FUNC   : unsigned long add_ulong(unsigned long ,unsigned long );

        MEMBER FUNC   : unsigned char add_uchar(unsigned char ,unsigned char );

        MEMBER FUNC   : signed char add_char(signed char ,signed char );

        MEMBER FUNC   : float add_float(float ,float );

        MEMBER FUNC   : double add_double(double ,double );

        MEMBER FUNC   : void hello();

        MEMBER FUNC   : int *nothing_pint(int *,int *);

        MEMBER FUNC   : short *nothing_pshort(short *,short *);

        MEMBER FUNC   : long *nothing_plong(long *,long *);

        MEMBER FUNC   : unsigned int *nothing_puint(unsigned int *,unsigned int *);

        MEMBER FUNC   : unsigned short *nothing_pushort(unsigned short *,unsigned short *);

        MEMBER FUNC   : unsigned long *nothing_pulong(unsigned long *,unsigned long *);

        MEMBER FUNC   : unsigned char *nothing_puchar(unsigned char *,unsigned char *);

        MEMBER FUNC   : signed char *nothing_pschar(signed char *,signed char *);

        MEMBER FUNC   : float *nothing_pfloat(float *,float *);

        MEMBER FUNC   : double *nothing_pdouble(double *,double *);

        MEMBER FUNC   : void print(char *);

        MEMBER FUNC   : int &ref_int(int &);

        MEMBER FUNC   : short &ref_short(short &);

        MEMBER FUNC   : long &ref_long(long &);

        MEMBER FUNC   : unsigned int &ref_uint(unsigned int &);

        MEMBER FUNC   : unsigned short &ref_ushort(unsigned short &);

        MEMBER FUNC   : unsigned long &ref_ulong(unsigned long &);

        MEMBER FUNC   : unsigned char &ref_uchar(unsigned char &);

        MEMBER FUNC   : signed char &ref_schar(signed char &);

        MEMBER FUNC   : float &ref_float(float &);

        MEMBER FUNC   : double &ref_double(double &);

        MEMBER FUNC   : char &ref_char(char &);

C++ CLASS END ===================================================

SWIG POINTER-MAPPING TABLE

/*
 * This table is used by the pointer type-checker
 */
static struct { char *n1; char *n2; void *(*pcnv)(void *); } _swig_mapping[] = {
    { "_signed_long","_long",0},
    { "_long","_unsigned_long",0},
    { "_long","_signed_long",0},
    { "_Func","_class_Func",0},
    { "_unsigned_long","_long",0},
    { "_class_Func2","_Func2",0},
    { "_signed_int","_int",0},
    { "_unsigned_short","_short",0},
    { "_signed_short","_short",0},
    { "_unsigned_int","_int",0},
    { "_class_Func","_Func",0},
    { "_short","_unsigned_short",0},
    { "_short","_signed_short",0},
    { "_int","_unsigned_int",0},
    { "_int","_signed_int",0},
    { "_Func2","_class_Func2",0},
{0,0,0}};


/* MODULE INITIALIZATION */

void swig_init() {
     ADD COMMAND    : Func_div --> double Func::div(double ,double );

     // C++ CLASS START : class Func
     ADD CONSTRUCT  : Func --> Func *Func(double );
     ADD DESTRUCT  : Func --> ~Func();
     ADD MEMBER FUN : add --> double add(double );
     ADD MEMBER FUN : abs --> double abs();
     ADD STATIC FUNC: mul --> double mul(double ,double );
     ADD MEMBER FUN : sub --> double sub(double &);
     ADD MEMBER FUN : new_double --> double &new_double(double );
     // C++ CLASS END 


     // C++ CLASS START : class Func2
     ADD MEMBER FUN : add_int --> int add_int(int ,int );
     ADD MEMBER FUN : add_short --> short add_short(short ,short );
     ADD MEMBER FUN : add_long --> long add_long(long ,long );
     ADD MEMBER FUN : add_uint --> unsigned int add_uint(unsigned int ,unsigned int );
     ADD MEMBER FUN : add_ushort --> unsigned short add_ushort(unsigned short ,unsigned short );
     ADD MEMBER FUN : add_ulong --> unsigned long add_ulong(unsigned long ,unsigned long );
     ADD MEMBER FUN : add_uchar --> unsigned char add_uchar(unsigned char ,unsigned char );
     ADD MEMBER FUN : add_char --> signed char add_char(signed char ,signed char );
     ADD MEMBER FUN : add_float --> float add_float(float ,float );
     ADD MEMBER FUN : add_double --> double add_double(double ,double );
     ADD MEMBER FUN : hello --> void hello();
     ADD MEMBER FUN : nothing_pint --> int *nothing_pint(int *,int *);
     ADD MEMBER FUN : nothing_pshort --> short *nothing_pshort(short *,short *);
     ADD MEMBER FUN : nothing_plong --> long *nothing_plong(long *,long *);
     ADD MEMBER FUN : nothing_puint --> unsigned int *nothing_puint(unsigned int *,unsigned int *);
     ADD MEMBER FUN : nothing_pushort --> unsigned short *nothing_pushort(unsigned short *,unsigned short *);
     ADD MEMBER FUN : nothing_pulong --> unsigned long *nothing_pulong(unsigned long *,unsigned long *);
     ADD MEMBER FUN : nothing_puchar --> unsigned char *nothing_puchar(unsigned char *,unsigned char *);
     ADD MEMBER FUN : nothing_pschar --> signed char *nothing_pschar(signed char *,signed char *);
     ADD MEMBER FUN : nothing_pfloat --> float *nothing_pfloat(float *,float *);
     ADD MEMBER FUN : nothing_pdouble --> double *nothing_pdouble(double *,double *);
     ADD MEMBER FUN : print --> void print(char *);
     ADD MEMBER FUN : ref_int --> int &ref_int(int &);
     ADD MEMBER FUN : ref_short --> short &ref_short(short &);
     ADD MEMBER FUN : ref_long --> long &ref_long(long &);
     ADD MEMBER FUN : ref_uint --> unsigned int &ref_uint(unsigned int &);
     ADD MEMBER FUN : ref_ushort --> unsigned short &ref_ushort(unsigned short &);
     ADD MEMBER FUN : ref_ulong --> unsigned long &ref_ulong(unsigned long &);
     ADD MEMBER FUN : ref_uchar --> unsigned char &ref_uchar(unsigned char &);
     ADD MEMBER FUN : ref_schar --> signed char &ref_schar(signed char &);
     ADD MEMBER FUN : ref_float --> float &ref_float(float &);
     ADD MEMBER FUN : ref_double --> double &ref_double(double &);
     ADD MEMBER FUN : ref_char --> char &ref_char(char &);
     // C++ CLASS END 

}  /* END INIT */
{
   int i;
   for (i = 0; _swig_mapping[i].n1; i++)
        SWIG_RegisterMapping(_swig_mapping[i].n1,_swig_mapping[i].n2,_swig_mapping[i].pcnv);
}
