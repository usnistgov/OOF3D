/* DEBUG : Language specific headers go here */

/* DEBUG : Pointer conversion function here */

/* DEBUG : Language specific code here */

#define   SWIG_init     swig_init

#define   SWIG_name    "swig"
extern int  t_eint; 
extern short  t_eshort; 
extern long  t_elong; 
extern unsigned int  t_euint; 
extern unsigned short  t_eushort; 
extern unsigned long  t_eulong; 
extern signed int  t_esint; 
extern signed short  t_esshort; 
extern signed long  t_eslong; 
extern unsigned  t_eu; 
extern signed  t_es; 
extern signed char  t_eschar; 
extern unsigned char  t_euchar; 
extern char  t_echar; 
extern float  t_efloat; 
extern double  t_edouble; 
extern bool  t_ebool; 
extern int  ea; 
extern int * eb; 
extern int ** ec; 
extern int *** ed; 
WRAPPER : int  t_int; 
WRAPPER : short  t_short; 
WRAPPER : long  t_long; 
WRAPPER : unsigned int  t_uint; 
WRAPPER : unsigned short  t_ushort; 
WRAPPER : unsigned long  t_ulong; 
WRAPPER : signed int  t_sint; 
WRAPPER : signed short  t_sshort; 
WRAPPER : signed long  t_slong; 
WRAPPER : unsigned  t_u; 
WRAPPER : signed  t_s; 
WRAPPER : signed char  t_schar; 
WRAPPER : unsigned char  t_uchar; 
WRAPPER : char  t_char; 
WRAPPER : float  t_float; 
WRAPPER : double  t_double; 
WRAPPER : bool  t_bool; 
WRAPPER : int * t_aint; 
WRAPPER : double * t_adouble; 
WRAPPER : float *** t_pfloat; 
WRAPPER : struct Matrix1  t_struct; 
WRAPPER : class Matrix2  t_class; 
WRAPPER : union Matrix3  t_union; 
WRAPPER : Matrix4  t_user; 
WRAPPER : struct Matrix4 * t_pstruct; 
WRAPPER : class Matrix5 * t_pclass; 
WRAPPER : union Matrix6 * t_punion; 
WRAPPER : Matrix7 * t_puser; 
WRAPPER : int  a; 
WRAPPER : int * b; 
WRAPPER : int ** c; 
WRAPPER : int *** d; 
WRAPPER : int  t_eint; 
WRAPPER : short  t_eshort; 
WRAPPER : long  t_elong; 
WRAPPER : unsigned int  t_euint; 
WRAPPER : unsigned short  t_eushort; 
WRAPPER : unsigned long  t_eulong; 
WRAPPER : signed int  t_esint; 
WRAPPER : signed short  t_esshort; 
WRAPPER : signed long  t_eslong; 
WRAPPER : unsigned  t_eu; 
WRAPPER : signed  t_es; 
WRAPPER : signed char  t_eschar; 
WRAPPER : unsigned char  t_euchar; 
WRAPPER : char  t_echar; 
WRAPPER : float  t_efloat; 
WRAPPER : double  t_edouble; 
WRAPPER : bool  t_ebool; 
WRAPPER : int  ea; 
WRAPPER : int * eb; 
WRAPPER : int ** ec; 
WRAPPER : int *** ed; 
WRAPPER : char  aa[32]; 
WRAPPER : int  ai[100]; 
WRAPPER : Vector  av[200]; 
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
     ADD VARIABLE   : t_int --> int  t_int; 
     ADD VARIABLE   : t_short --> short  t_short; 
     ADD VARIABLE   : t_long --> long  t_long; 
     ADD VARIABLE   : t_uint --> unsigned int  t_uint; 
     ADD VARIABLE   : t_ushort --> unsigned short  t_ushort; 
     ADD VARIABLE   : t_ulong --> unsigned long  t_ulong; 
     ADD VARIABLE   : t_sint --> signed int  t_sint; 
     ADD VARIABLE   : t_sshort --> signed short  t_sshort; 
     ADD VARIABLE   : t_slong --> signed long  t_slong; 
     ADD VARIABLE   : t_u --> unsigned  t_u; 
     ADD VARIABLE   : t_s --> signed  t_s; 
     ADD VARIABLE   : t_schar --> signed char  t_schar; 
     ADD VARIABLE   : t_uchar --> unsigned char  t_uchar; 
     ADD VARIABLE   : t_char --> char  t_char; 
     ADD VARIABLE   : t_float --> float  t_float; 
     ADD VARIABLE   : t_double --> double  t_double; 
     ADD VARIABLE   : t_bool --> bool  t_bool; 
     ADD VARIABLE   : t_aint --> int * t_aint; 
     ADD VARIABLE   : t_adouble --> double * t_adouble; 
     ADD VARIABLE   : t_pfloat --> float *** t_pfloat; 
     ADD VARIABLE   : t_struct --> struct Matrix1  t_struct; 
     ADD VARIABLE   : t_class --> class Matrix2  t_class; 
     ADD VARIABLE   : t_union --> union Matrix3  t_union; 
     ADD VARIABLE   : t_user --> Matrix4  t_user; 
     ADD VARIABLE   : t_pstruct --> struct Matrix4 * t_pstruct; 
     ADD VARIABLE   : t_pclass --> class Matrix5 * t_pclass; 
     ADD VARIABLE   : t_punion --> union Matrix6 * t_punion; 
     ADD VARIABLE   : t_puser --> Matrix7 * t_puser; 
     ADD VARIABLE   : a --> int  a; 
     ADD VARIABLE   : b --> int * b; 
     ADD VARIABLE   : c --> int ** c; 
     ADD VARIABLE   : d --> int *** d; 
     ADD VARIABLE   : t_eint --> int  t_eint; 
     ADD VARIABLE   : t_eshort --> short  t_eshort; 
     ADD VARIABLE   : t_elong --> long  t_elong; 
     ADD VARIABLE   : t_euint --> unsigned int  t_euint; 
     ADD VARIABLE   : t_eushort --> unsigned short  t_eushort; 
     ADD VARIABLE   : t_eulong --> unsigned long  t_eulong; 
     ADD VARIABLE   : t_esint --> signed int  t_esint; 
     ADD VARIABLE   : t_esshort --> signed short  t_esshort; 
     ADD VARIABLE   : t_eslong --> signed long  t_eslong; 
     ADD VARIABLE   : t_eu --> unsigned  t_eu; 
     ADD VARIABLE   : t_es --> signed  t_es; 
     ADD VARIABLE   : t_eschar --> signed char  t_eschar; 
     ADD VARIABLE   : t_euchar --> unsigned char  t_euchar; 
     ADD VARIABLE   : t_echar --> char  t_echar; 
     ADD VARIABLE   : t_efloat --> float  t_efloat; 
     ADD VARIABLE   : t_edouble --> double  t_edouble; 
     ADD VARIABLE   : t_ebool --> bool  t_ebool; 
     ADD VARIABLE   : ea --> int  ea; 
     ADD VARIABLE   : eb --> int * eb; 
     ADD VARIABLE   : ec --> int ** ec; 
     ADD VARIABLE   : ed --> int *** ed; 
     ADD VARIABLE   : aa --> char  aa[32]; 
     ADD VARIABLE   : ai --> int  ai[100]; 
     ADD VARIABLE   : av --> Vector  av[200]; 
}  /* END INIT */
{
   int i;
   for (i = 0; _swig_mapping[i].n1; i++)
        SWIG_RegisterMapping(_swig_mapping[i].n1,_swig_mapping[i].n2,_swig_mapping[i].pcnv);
}
