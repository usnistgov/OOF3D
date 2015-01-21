/* DEBUG : Language specific headers go here */

/* DEBUG : Pointer conversion function here */

/* DEBUG : Language specific code here */

#define   SWIG_init     swig_init

#define   SWIG_name    "swig"
C++ CLASS DECLARATION : class Foo
C++ CLASS START : class Foo  ========================================

        C++ CONST     : (int ) JAN = [None]
        C++ CONST     : (int ) FEB = [None]
        C++ CONST     : (int ) MAR = [None]
        C++ CONST     : (int ) APR = [None]
        C++ CONST     : (int ) MAY = [None]
        C++ CONST     : (int ) JUN = [None]
        C++ CONST     : (int ) JUL = [None]
        C++ CONST     : (int ) AUG = [None]
        C++ CONST     : (int ) SEP = [None]
        C++ CONST     : (int ) OCT = [None]
        C++ CONST     : (int ) NOV = [None]
        C++ CONST     : (int ) DEC = [None]
        C++ CONST     : (int ) PEAR = [None]
        C++ CONST     : (int ) APPLE = [None]
        C++ CONST     : (int ) BANANA = [None]
        C++ CONST     : (int ) PEACH = [None]
        C++ CONST     : (int ) VAL1 = [None]
        C++ CONST     : (int ) VAL2 = [None]
        C++ CONST     : (int ) VAL3 = [None]
        C++ CONST     : (double ) MAX = 50
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
     ADD CONSTANT   : (int ) PEAR = PEAR
     ADD CONSTANT   : (int ) APPLE = APPLE
     ADD CONSTANT   : (double ) PI = 3.141592654
     ADD CONSTANT   : (int ) N = 1000
     ADD CONSTANT   : (char *) VERSION = 1.0

     // C++ CLASS START : class Foo
     ADD C++ CONST  : JAN --> (int ) = [None]
     ADD C++ CONST  : FEB --> (int ) = [None]
     ADD C++ CONST  : MAR --> (int ) = [None]
     ADD C++ CONST  : APR --> (int ) = [None]
     ADD C++ CONST  : MAY --> (int ) = [None]
     ADD C++ CONST  : JUN --> (int ) = [None]
     ADD C++ CONST  : JUL --> (int ) = [None]
     ADD C++ CONST  : AUG --> (int ) = [None]
     ADD C++ CONST  : SEP --> (int ) = [None]
     ADD C++ CONST  : OCT --> (int ) = [None]
     ADD C++ CONST  : NOV --> (int ) = [None]
     ADD C++ CONST  : DEC --> (int ) = [None]
     ADD C++ CONST  : PEAR --> (int ) = [None]
     ADD C++ CONST  : APPLE --> (int ) = [None]
     ADD C++ CONST  : BANANA --> (int ) = [None]
     ADD C++ CONST  : PEACH --> (int ) = [None]
     ADD C++ CONST  : VAL1 --> (int ) = [None]
     ADD C++ CONST  : VAL2 --> (int ) = [None]
     ADD C++ CONST  : VAL3 --> (int ) = [None]
     ADD C++ CONST  : MAX --> (double ) = 50
     // C++ CLASS END 

}  /* END INIT */
{
   int i;
   for (i = 0; _swig_mapping[i].n1; i++)
        SWIG_RegisterMapping(_swig_mapping[i].n1,_swig_mapping[i].n2,_swig_mapping[i].pcnv);
}
