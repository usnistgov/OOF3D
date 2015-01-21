/* DEBUG : Language specific headers go here */

/* DEBUG : Pointer conversion function here */

/* DEBUG : Language specific code here */

#define   SWIG_init     swig_init

#define   SWIG_name    "swig"
C++ CLASS DECLARATION : class Data
C++ CLASS START : class Data  ========================================

        ATTRIBUTE     : int  d_int; 
        ATTRIBUTE     : short  d_short; 
        ATTRIBUTE     : long  d_long; 
        ATTRIBUTE     : unsigned int  d_uint; 
        ATTRIBUTE     : unsigned short  d_ushort; 
        ATTRIBUTE     : unsigned long  d_ulong; 
        ATTRIBUTE     : unsigned char  d_uchar; 
        ATTRIBUTE     : signed char  d_schar; 
        ATTRIBUTE     : float  d_float; 
        ATTRIBUTE     : double  d_double; 
        ATTRIBUTE     : char * d_string; 
        ATTRIBUTE     : char  d_char; 
        ATTRIBUTE     : int * p_int; 
        ATTRIBUTE     : short * p_short; 
        ATTRIBUTE     : long * p_long; 
        ATTRIBUTE     : unsigned int * p_uint; 
        ATTRIBUTE     : unsigned short * p_ushort; 
        ATTRIBUTE     : unsigned long * p_ulong; 
        ATTRIBUTE     : unsigned char * p_uchar; 
        ATTRIBUTE     : signed char * p_schar; 
        ATTRIBUTE     : float * p_float; 
        ATTRIBUTE     : double * p_double; 
        C++ STATIC VAR: int  s_int; 
        C++ STATIC VAR: short  s_short; 
        C++ STATIC VAR: long  s_long; 
        C++ STATIC VAR: float  s_float; 
        C++ STATIC VAR: double  s_double; 
        C++ STATIC VAR: char * s_string; 
        ATTRIBUTE     : Vector  vec; 
        ATTRIBUTE     : Vector & rvec; 
C++ CLASS END ===================================================

SWIG POINTER-MAPPING TABLE

/*
 * This table is used by the pointer type-checker
 */
static struct { char *n1; char *n2; void *(*pcnv)(void *); } _swig_mapping[] = {
    { "_signed_long","_long",0},
    { "_long","_unsigned_long",0},
    { "_long","_signed_long",0},
    { "_class_Data","_Data",0},
    { "_unsigned_long","_long",0},
    { "_signed_int","_int",0},
    { "_unsigned_short","_short",0},
    { "_signed_short","_short",0},
    { "_unsigned_int","_int",0},
    { "_short","_unsigned_short",0},
    { "_short","_signed_short",0},
    { "_int","_unsigned_int",0},
    { "_int","_signed_int",0},
    { "_Data","_class_Data",0},
{0,0,0}};


/* MODULE INITIALIZATION */

void swig_init() {

     // C++ CLASS START : class Data
     ADD MEMBER     : d_int --> int  d_int; 
     ADD MEMBER     : d_short --> short  d_short; 
     ADD MEMBER     : d_long --> long  d_long; 
     ADD MEMBER     : d_uint --> unsigned int  d_uint; 
     ADD MEMBER     : d_ushort --> unsigned short  d_ushort; 
     ADD MEMBER     : d_ulong --> unsigned long  d_ulong; 
     ADD MEMBER     : d_uchar --> unsigned char  d_uchar; 
     ADD MEMBER     : d_schar --> signed char  d_schar; 
     ADD MEMBER     : d_float --> float  d_float; 
     ADD MEMBER     : d_double --> double  d_double; 
     ADD MEMBER     : d_string --> char * d_string; 
     ADD MEMBER     : d_char --> char  d_char; 
     ADD MEMBER     : p_int --> int * p_int; 
     ADD MEMBER     : p_short --> short * p_short; 
     ADD MEMBER     : p_long --> long * p_long; 
     ADD MEMBER     : p_uint --> unsigned int * p_uint; 
     ADD MEMBER     : p_ushort --> unsigned short * p_ushort; 
     ADD MEMBER     : p_ulong --> unsigned long * p_ulong; 
     ADD MEMBER     : p_uchar --> unsigned char * p_uchar; 
     ADD MEMBER     : p_schar --> signed char * p_schar; 
     ADD MEMBER     : p_float --> float * p_float; 
     ADD MEMBER     : p_double --> double * p_double; 
     ADD STATIC VAR : s_int --> int  s_int; 
     ADD STATIC VAR : s_short --> short  s_short; 
     ADD STATIC VAR : s_long --> long  s_long; 
     ADD STATIC VAR : s_float --> float  s_float; 
     ADD STATIC VAR : s_double --> double  s_double; 
     ADD STATIC VAR : s_string --> char * s_string; 
     ADD MEMBER     : vec --> Vector  vec; 
     ADD MEMBER     : rvec --> Vector & rvec; 
     // C++ CLASS END 

}  /* END INIT */
{
   int i;
   for (i = 0; _swig_mapping[i].n1; i++)
        SWIG_RegisterMapping(_swig_mapping[i].n1,_swig_mapping[i].n2,_swig_mapping[i].pcnv);
}
