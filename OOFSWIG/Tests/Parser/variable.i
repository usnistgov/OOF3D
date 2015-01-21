//
// variable.i
// Parser test of SWIG variable declarations

%module variable

// Test parsing of all basic datatypes

int               t_int;
short             t_short;
long              t_long;
unsigned int      t_uint;
unsigned short    t_ushort;
unsigned long     t_ulong;
signed int        t_sint;
signed short      t_sshort;
signed long       t_slong;
unsigned          t_u;
signed            t_s;
signed char       t_schar;
unsigned char     t_uchar;
char              t_char;
float             t_float;
double            t_double;
bool              t_bool;

/* A few pointer types */

int            *t_aint;
double         *t_adouble;
float          ***t_pfloat;

/* Complex datatypes */

struct Matrix1      t_struct;
class Matrix2       t_class;
union Matrix3       t_union;
Matrix4             t_user;
struct Matrix4     *t_pstruct;
class Matrix5      *t_pclass;
union Matrix6      *t_punion;
Matrix7            *t_puser;

// Multiple declarations on same line

int  a, *b, **c, ***d;

// "extern" variables

extern int               t_eint;
extern short             t_eshort;
extern long              t_elong;
extern unsigned int      t_euint;
extern unsigned short    t_eushort;
extern unsigned long     t_eulong;
extern signed int        t_esint;
extern signed short      t_esshort;
extern signed long       t_eslong;
extern unsigned          t_eu;
extern signed            t_es;
extern signed char       t_eschar;
extern unsigned char     t_euchar;
extern char              t_echar;
extern float             t_efloat;
extern double            t_edouble;
extern bool              t_ebool;
	
extern int  ea, *eb, **ec, ***ed;

// Array variables

char  aa[32];
int   ai[100];
Vector av[200];
