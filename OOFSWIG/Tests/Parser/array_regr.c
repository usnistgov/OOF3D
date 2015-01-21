/* DEBUG : Language specific headers go here */

/* DEBUG : Pointer conversion function here */

/* DEBUG : Language specific code here */

#define   SWIG_init     swig_init

#define   SWIG_name    "swig"


extern int foo(int [4],int [4][4],int [4][4][3]);
extern int func(int ,char *[]);
extern float matrix(MATRIX4 );
extern float matrixofmatrix(MATRIX4 [4]);
WRAPPER : int foo(int [4],int [4][4],int [4][4][3]);

WRAPPER : int func(int ,char *[]);

WRAPPER : float matrix(MATRIX4 );

WRAPPER : float matrixofmatrix(MATRIX4 [4]);

SWIG POINTER-MAPPING TABLE

/*
 * This table is used by the pointer type-checker
 */
static struct { char *n1; char *n2; void *(*pcnv)(void *); } _swig_mapping[] = {
    { "_signed_long","_long",0},
    { "_long","_unsigned_long",0},
    { "_long","_signed_long",0},
    { "_MATRIX4","_float_p",0},
    { "_float_p","_MATRIX4",0},
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
     ADD COMMAND    : foo --> int foo(int [4],int [4][4],int [4][4][3]);
     ADD COMMAND    : func --> int func(int ,char *[]);
     ADD COMMAND    : matrix --> float matrix(MATRIX4 );
     ADD COMMAND    : matrixofmatrix --> float matrixofmatrix(MATRIX4 [4]);
}  /* END INIT */
{
   int i;
   for (i = 0; _swig_mapping[i].n1; i++)
        SWIG_RegisterMapping(_swig_mapping[i].n1,_swig_mapping[i].n2,_swig_mapping[i].pcnv);
}
