/* DEBUG : Language specific headers go here */

/* DEBUG : Pointer conversion function here */

/* DEBUG : Language specific code here */

#define   SWIG_init     swig_init

#define   SWIG_name    "swig"

extern Vector add(Vector ,Vector );
extern Vector sub(Vector ,Vector );
extern Vector cross(Vector ,Vector );
extern double dot(Vector ,Vector );
extern Vector mul(double ,Vector );
C++ CLASS DECLARATION : struct Vector
WRAPPER : Vector add(Vector ,Vector );

WRAPPER : Vector sub(Vector ,Vector );

WRAPPER : Vector cross(Vector ,Vector );

WRAPPER : double dot(Vector ,Vector );

WRAPPER : Vector mul(double ,Vector );

C++ CLASS DECLARATION : class Vector2
C++ CLASS START : class Vector2  ========================================

inheriting from baseclass : Vector
static void *SwigVector2ToVector(void *ptr) {
    Vector2 *src;
    Vector *dest;
    src = (Vector2 *) ptr;
    dest = (Vector *) src;
    return (void *) dest;
}

        ATTRIBUTE     : double  w; 
        ATTRIBUTE     : Real  x; 
        ATTRIBUTE     : Real  y; 
        ATTRIBUTE     : Real  z; 
        MEMBER FUNC   : Vector *next();

        MEMBER FUNC   : Vector *get(int );

        MEMBER FUNC   : void __setitem__(int ,Vector *);

        MEMBER FUNC   : char *__str__();

C++ CLASS END ===================================================

SWIG POINTER-MAPPING TABLE

/*
 * This table is used by the pointer type-checker
 */
static struct { char *n1; char *n2; void *(*pcnv)(void *); } _swig_mapping[] = {
    { "_signed_long","_long",0},
    { "_double","_Real",0},
    { "_Vector","_class_Vector2",SwigVector2ToVector},
    { "_Vector","_Vector2",SwigVector2ToVector},
    { "_Vector","_struct_Vector",0},
    { "_Real","_double",0},
    { "_long","_unsigned_long",0},
    { "_long","_signed_long",0},
    { "_class_Vector2","_Vector2",0},
    { "_unsigned_long","_long",0},
    { "_signed_int","_int",0},
    { "_unsigned_short","_short",0},
    { "_signed_short","_short",0},
    { "_unsigned_int","_int",0},
    { "_short","_unsigned_short",0},
    { "_short","_signed_short",0},
    { "_int","_unsigned_int",0},
    { "_int","_signed_int",0},
    { "_struct_Vector","_class_Vector2",SwigVector2ToVector},
    { "_struct_Vector","_Vector2",SwigVector2ToVector},
    { "_struct_Vector","_Vector",0},
    { "_Vector2","_class_Vector2",0},
{0,0,0}};


/* MODULE INITIALIZATION */

void swig_init() {
     ADD COMMAND    : add --> Vector add(Vector ,Vector );
     ADD COMMAND    : sub --> Vector sub(Vector ,Vector );
     ADD COMMAND    : cross --> Vector cross(Vector ,Vector );
     ADD COMMAND    : dot --> double dot(Vector ,Vector );
     ADD COMMAND    : mul --> Vector mul(double ,Vector );

     // C++ CLASS START : class Vector2
     ADD MEMBER     : w --> double  w; 
     ADD MEMBER     : x --> Real  x; 
     ADD MEMBER     : y --> Real  y; 
     ADD MEMBER     : z --> Real  z; 
     ADD MEMBER FUN : next --> Vector *next();
     ADD MEMBER FUN : __getitem__ --> Vector *get(int );
     ADD MEMBER FUN : __setitem__ --> void __setitem__(int ,Vector *);
     ADD MEMBER FUN : __str__ --> char *__str__();
     // C++ CLASS END 

}  /* END INIT */
{
   int i;
   for (i = 0; _swig_mapping[i].n1; i++)
        SWIG_RegisterMapping(_swig_mapping[i].n1,_swig_mapping[i].n2,_swig_mapping[i].pcnv);
}
