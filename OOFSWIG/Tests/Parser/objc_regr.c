/* DEBUG : Language specific headers go here */

/* DEBUG : Pointer conversion function here */

/* DEBUG : Language specific code here */

#define   SWIG_init     swig_init

#define   SWIG_name    "swig"
C++ CLASS DECLARATION :  foo1
C++ CLASS DECLARATION :  foo2
C++ CLASS DECLARATION :  foo3
C++ CLASS DECLARATION :  inherit1
C++ CLASS DECLARATION :  rname
C++ CLASS DECLARATION :  added
C++ CLASS DECLARATION :  cls1
C++ CLASS DECLARATION :  cls2
C++ CLASS DECLARATION :  cls3
WRAPPER : void proto1(id< Proto1 > ,id< Proto2 > ,id< Proto3,Proto4,Proto5 > );

C++ CLASS START :  foo1  ========================================

inheriting from baseclass : Object
        MEMBER FUNC   : int bar1(double );

        STATIC FUNC   : void bar2();
        MEMBER FUNC   : id bar3();

        CONSTRUCTOR   : new *new();
        DESTRUCTOR    : ~free();
        MEMBER FUNC   : id private$member();

        MEMBER FUNC   : id spam1(int ,double ,char *);

        STATIC FUNC   : id spam2(int ,double ,char *);
        MEMBER FUNC   : id more1();

        MEMBER FUNC   : int more2(double );

        MEMBER FUNC   : double added2(double );

C++ CLASS END ===================================================

C++ CLASS START :  foo2  ========================================

        MEMBER FUNC   : int bar1(double );

C++ CLASS END ===================================================

C++ CLASS START :  foo3  ========================================

inheriting from baseclass : Object
        MEMBER FUNC   : int bar1(double );

C++ CLASS END ===================================================

C++ CLASS START :  inherit1  ========================================

inheriting from baseclass : foo1
        ATTRIBUTE     : int  a; 
        ATTRIBUTE     : int  c; 
        ATTRIBUTE     : int  b; 
        MEMBER FUNC   : int base1();

        MEMBER FUNC   : double base2(int );

        MEMBER FUNC   : int bar1(double );

        STATIC FUNC   : void bar2();
        MEMBER FUNC   : id bar3();

        MEMBER FUNC   : id private$member();

        MEMBER FUNC   : id spam1(int ,double ,char *);

        STATIC FUNC   : id spam2(int ,double ,char *);
        MEMBER FUNC   : id more1();

        MEMBER FUNC   : int more2(double );

        MEMBER FUNC   : double added2(double );

C++ CLASS END ===================================================

C++ CLASS START :  rname  ========================================

inheriting from baseclass : Object
        ATTRIBUTE     : int  a; 
        ATTRIBUTE     : int  c; 
        ATTRIBUTE     : int  b; 
        ATTRIBUTE     : double  d; 
        MEMBER FUNC   : int oldname(double ,int );

C++ CLASS END ===================================================

C++ CLASS START :  added  ========================================

inheriting from baseclass : Object
        MEMBER FUNC   : double added1(double ,double );

        STATIC FUNC   : int addi(int ,int );
C++ CLASS END ===================================================

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
    { "_foo1","_inherit1",0},
{0,0,0}};


/* MODULE INITIALIZATION */

void swig_init() {
     ADD COMMAND    : proto1 --> void proto1(id< Proto1 > ,id< Proto2 > ,id< Proto3,Proto4,Proto5 > );

     // C++ CLASS START :  foo1
     ADD MEMBER FUN : bar1 --> int bar1(double );
     ADD STATIC FUNC: bar2 --> void bar2();
     ADD MEMBER FUN : bar3 --> id bar3();
     ADD CONSTRUCT  : new --> new *new();
     ADD DESTRUCT  : free --> ~free();
     ADD MEMBER FUN : private_S_member --> id private$member();
     ADD MEMBER FUN : spam1 --> id spam1(int ,double ,char *);
     ADD STATIC FUNC: spam2 --> id spam2(int ,double ,char *);
     ADD MEMBER FUN : more1 --> id more1();
     ADD MEMBER FUN : more2 --> int more2(double );
     ADD MEMBER FUN : added2 --> double added2(double );
     // C++ CLASS END 


     // C++ CLASS START :  foo2
     ADD MEMBER FUN : bar1 --> int bar1(double );
     // C++ CLASS END 


     // C++ CLASS START :  foo3
     ADD MEMBER FUN : bar1 --> int bar1(double );
     // C++ CLASS END 


     // C++ CLASS START :  inherit1
     ADD MEMBER     : a --> int  a; 
     ADD MEMBER     : c --> int  c; 
     ADD MEMBER     : b --> int  b; 
     ADD MEMBER FUN : base1 --> int base1();
     ADD MEMBER FUN : base2 --> double base2(int );
     ADD MEMBER FUN : bar1 --> int bar1(double );
     ADD STATIC FUNC: bar2 --> void bar2();
     ADD MEMBER FUN : bar3 --> id bar3();
     ADD MEMBER FUN : private_S_member --> id private$member();
     ADD MEMBER FUN : spam1 --> id spam1(int ,double ,char *);
     ADD STATIC FUNC: spam2 --> id spam2(int ,double ,char *);
     ADD MEMBER FUN : more1 --> id more1();
     ADD MEMBER FUN : more2 --> int more2(double );
     ADD MEMBER FUN : added2 --> double added2(double );
     // C++ CLASS END 


     // C++ CLASS START :  rname
     ADD MEMBER     : a --> int  a; 
     ADD MEMBER     : c --> int  c; 
     ADD MEMBER     : b --> int  b; 
     ADD MEMBER     : myd --> double  d; 
     ADD MEMBER FUN : myname --> int oldname(double ,int );
     // C++ CLASS END 


     // C++ CLASS START :  added
     ADD MEMBER FUN : added1 --> double added1(double ,double );
     ADD STATIC FUNC: addi --> int addi(int ,int );
     // C++ CLASS END 

}  /* END INIT */
{
   int i;
   for (i = 0; _swig_mapping[i].n1; i++)
        SWIG_RegisterMapping(_swig_mapping[i].n1,_swig_mapping[i].n2,_swig_mapping[i].pcnv);
}
