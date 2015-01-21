/* DEBUG : Language specific headers go here */

/* DEBUG : Pointer conversion function here */

/* DEBUG : Language specific code here */

#define   SWIG_init     swig_init

#define   SWIG_name    "swig"
WRAPPER : int misc1(int );

WRAPPER : int misc2(int ,int );

C++ CLASS DECLARATION : class Misc
C++ CLASS DECLARATION : class Foo
C++ CLASS START : class Misc  ========================================

        MEMBER FUNC   : int misc3(double );

        MEMBER FUNC   : double misc4(double ,float );

C++ CLASS END ===================================================

C++ CLASS START : class Foo  ========================================

        CONSTRUCTOR   : Foo *Foo(int ,int );
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
    { "_Misc","_class_Misc",0},
    { "_signed_int","_int",0},
    { "_unsigned_short","_short",0},
    { "_signed_short","_short",0},
    { "_unsigned_int","_int",0},
    { "_short","_unsigned_short",0},
    { "_short","_signed_short",0},
    { "_int","_unsigned_int",0},
    { "_int","_signed_int",0},
    { "_class_Misc","_Misc",0},
    { "_Foo","_class_Foo",0},
{0,0,0}};


/* MODULE INITIALIZATION */

void swig_init() {
     ADD COMMAND    : misc1 --> int misc1(int );
     ADD COMMAND    : misc2 --> int misc2(int ,int );

     // C++ CLASS START : class Misc
     ADD MEMBER FUN : misc3 --> int misc3(double );
     ADD MEMBER FUN : misc4 --> double misc4(double ,float );
     // C++ CLASS END 


     // C++ CLASS START : class Foo
     ADD CONSTRUCT  : Foo --> Foo *Foo(int ,int );
     // C++ CLASS END 

}  /* END INIT */
{
   int i;
   for (i = 0; _swig_mapping[i].n1; i++)
        SWIG_RegisterMapping(_swig_mapping[i].n1,_swig_mapping[i].n2,_swig_mapping[i].pcnv);
}
