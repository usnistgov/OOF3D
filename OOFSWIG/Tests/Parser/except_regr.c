/* DEBUG : Language specific headers go here */

/* DEBUG : Pointer conversion function here */

/* DEBUG : Language specific code here */

#define   SWIG_init     swig_init

#define   SWIG_name    "swig"
WRAPPER : int f1(double );

WRAPPER : int f2(double );

WRAPPER : int f3(int );

C++ CLASS DECLARATION : class Foo
C++ CLASS START : class Foo  ========================================

        MEMBER FUNC   : int f1(double );

        MEMBER FUNC   : int f2(double );

        MEMBER FUNC   : int f3(double );

C++ CLASS END ===================================================

SWIG POINTER-MAPPING TABLE

/*
 * This table is used by the pointer type-checker
 */
static struct { char *n1; char *n2; void *(*pcnv)(void *); } _swig_mapping[] = {
    { "_signed_long","_long",0},
    { "_class_Foo","_Foo",0},
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
    { "_Foo","_class_Foo",0},
{0,0,0}};


/* MODULE INITIALIZATION */

void swig_init() {
     ADD COMMAND    : f1 --> int f1(double );
     ADD COMMAND    : f2 --> int f2(double );
     ADD COMMAND    : f3 --> int f3(int );

     // C++ CLASS START : class Foo
     ADD MEMBER FUN : f1 --> int f1(double );
     ADD MEMBER FUN : f2 --> int f2(double );
     ADD MEMBER FUN : f3 --> int f3(double );
     // C++ CLASS END 

}  /* END INIT */
{
   int i;
   for (i = 0; _swig_mapping[i].n1; i++)
        SWIG_RegisterMapping(_swig_mapping[i].n1,_swig_mapping[i].n2,_swig_mapping[i].pcnv);
}
