/* DEBUG : Language specific headers go here */

/* DEBUG : Pointer conversion function here */

/* DEBUG : Language specific code here */

#define   SWIG_init     swig_init

#define   SWIG_name    "swig"
WRAPPER : int  my_variable; 
WRAPPER : double sum(double ,double );

C++ CLASS DECLARATION : class Foo2
C++ CLASS DECLARATION : class Class
WRAPPER : Class *retClass();

C++ CLASS DECLARATION : class Foo3
C++ CLASS DECLARATION : class Foo4
C++ CLASS DECLARATION : class Bar
WRAPPER : void OldName(double );

WRAPPER : void SameName(int );

WRAPPER : int foo10(double );

WRAPPER : int old_name(double );

C++ CLASS DECLARATION : class C
C++ CLASS START : class Foo2  ========================================

        ATTRIBUTE     : double  var; 
        C++ STATIC VAR: double  static_var; 
        MEMBER FUNC   : int sum(int ,int );

        STATIC FUNC   : int mul(int ,int );
        C++ CONST     : (int ) lager = [None]
        C++ CONST     : (int ) ale = [None]
        C++ CONST     : (int ) stout = [None]
        C++ CONST     : (int ) pilsner = [None]
        MEMBER FUNC   : int foo(double ,double );

        MEMBER FUNC   : void foo(char *);

        STATIC FUNC   : int bar(double );
        STATIC FUNC   : void bar(char *);
        STATIC FUNC   : int bar(int );
C++ CLASS END ===================================================

C++ CLASS START : class Class  ========================================

        ATTRIBUTE     : int  member_data; 
        MEMBER FUNC   : double member_func();

        MEMBER FUNC   : void pointer(Class *);

        MEMBER FUNC   : Class *retptr();

C++ CLASS END ===================================================

C++ CLASS START : class Foo3  ========================================

inheriting from baseclass : Foo2
static void *SwigFoo3ToFoo2(void *ptr) {
    Foo3 *src;
    Foo2 *dest;
    src = (Foo3 *) ptr;
    dest = (Foo2 *) src;
    return (void *) dest;
}

        ATTRIBUTE     : double  var; 
        C++ STATIC VAR: double  static_var; 
        MEMBER FUNC   : int sum(int ,int );

        STATIC FUNC   : int mul(int ,int );
        C++ CONST     : (int ) lager = [None]
        C++ CONST     : (int ) ale = [None]
        C++ CONST     : (int ) stout = [None]
        C++ CONST     : (int ) pilsner = [None]
        MEMBER FUNC   : int foo(double ,double );

        MEMBER FUNC   : void foo(char *);

        STATIC FUNC   : int bar(double );
        STATIC FUNC   : void bar(char *);
C++ CLASS END ===================================================

C++ CLASS START : class Foo4  ========================================

inheriting from baseclass : Foo3
static void *SwigFoo4ToFoo3(void *ptr) {
    Foo4 *src;
    Foo3 *dest;
    src = (Foo4 *) ptr;
    dest = (Foo3 *) src;
    return (void *) dest;
}

static void *SwigFoo4ToFoo2(void *ptr) {
    Foo4 *src;
    Foo2 *dest;
    src = (Foo4 *) ptr;
    dest = (Foo2 *) src;
    return (void *) dest;
}

        ATTRIBUTE     : double  var; 
        C++ STATIC VAR: double  static_var; 
        MEMBER FUNC   : int sum(int ,int );

        STATIC FUNC   : int mul(int ,int );
        C++ CONST     : (int ) lager = [None]
        C++ CONST     : (int ) ale = [None]
        C++ CONST     : (int ) stout = [None]
        C++ CONST     : (int ) pilsner = [None]
        MEMBER FUNC   : int foo(double ,double );

        MEMBER FUNC   : void foo(char *);

        STATIC FUNC   : int bar(double );
        STATIC FUNC   : void bar(char *);
C++ CLASS END ===================================================

C++ CLASS START : class Bar  ========================================

inheriting from baseclass : Class
static void *SwigBarToClass(void *ptr) {
    Bar *src;
    Class *dest;
    src = (Bar *) ptr;
    dest = (Class *) src;
    return (void *) dest;
}

        ATTRIBUTE     : int  member_data; 
        MEMBER FUNC   : double member_func();

        MEMBER FUNC   : void pointer(Class *);

        MEMBER FUNC   : Class *retptr();

C++ CLASS END ===================================================

C++ CLASS START : class C  ========================================

        MEMBER FUNC   : int old_name(int );

C++ CLASS END ===================================================

SWIG POINTER-MAPPING TABLE

/*
 * This table is used by the pointer type-checker
 */
static struct { char *n1; char *n2; void *(*pcnv)(void *); } _swig_mapping[] = {
    { "_signed_long","_long",0},
    { "_class_C","_C",0},
    { "_long","_unsigned_long",0},
    { "_long","_signed_long",0},
    { "_Bar","_class_Bar",0},
    { "_class_Foo2","_class_Foo4",SwigFoo4ToFoo2},
    { "_class_Foo2","_Foo4",SwigFoo4ToFoo2},
    { "_class_Foo2","_class_Foo3",SwigFoo3ToFoo2},
    { "_class_Foo2","_Foo3",SwigFoo3ToFoo2},
    { "_class_Foo2","_Foo2",0},
    { "_class_Foo3","_class_Foo4",SwigFoo4ToFoo3},
    { "_class_Foo3","_Foo4",SwigFoo4ToFoo3},
    { "_class_Foo3","_Foo3",0},
    { "_Class","_class_Bar",SwigBarToClass},
    { "_Class","_Bar",SwigBarToClass},
    { "_Class","_class_Class",0},
    { "_class_Foo4","_Foo4",0},
    { "_class_Bar","_Bar",0},
    { "_unsigned_long","_long",0},
    { "_signed_int","_int",0},
    { "_unsigned_short","_short",0},
    { "_signed_short","_short",0},
    { "_unsigned_int","_int",0},
    { "_short","_unsigned_short",0},
    { "_short","_signed_short",0},
    { "_int","_unsigned_int",0},
    { "_int","_signed_int",0},
    { "_C","_class_C",0},
    { "_class_Class","_class_Bar",SwigBarToClass},
    { "_class_Class","_Bar",SwigBarToClass},
    { "_class_Class","_Class",0},
    { "_Foo2","_class_Foo4",SwigFoo4ToFoo2},
    { "_Foo2","_Foo4",SwigFoo4ToFoo2},
    { "_Foo2","_class_Foo3",SwigFoo3ToFoo2},
    { "_Foo2","_Foo3",SwigFoo3ToFoo2},
    { "_Foo2","_class_Foo2",0},
    { "_Foo3","_class_Foo4",SwigFoo4ToFoo3},
    { "_Foo3","_Foo4",SwigFoo4ToFoo3},
    { "_Foo3","_class_Foo3",0},
    { "_Foo4","_class_Foo4",0},
{0,0,0}};


/* MODULE INITIALIZATION */

void swig_init() {
     ADD VARIABLE   : new_variable --> int  my_variable; 
     ADD COMMAND    : add --> double sum(double ,double );
     ADD COMMAND    : retClass --> Class *retClass();
     ADD COMMAND    : NewName --> void OldName(double );
     ADD COMMAND    : SameName --> void SameName(int );
     ADD COMMAND    : foo10 --> int foo10(double );
     ADD COMMAND    : new_name --> int old_name(double );

     // C++ CLASS START : class Foo2
     ADD MEMBER     : new_var --> double  var; 
     ADD STATIC VAR : new_static_var --> double  static_var; 
     ADD MEMBER FUN : add --> int sum(int ,int );
     ADD STATIC FUNC: product --> int mul(int ,int );
     ADD C++ CONST  : LAGER --> (int ) = [None]
     ADD C++ CONST  : ALE --> (int ) = [None]
     ADD C++ CONST  : STOUT --> (int ) = [None]
     ADD C++ CONST  : PILSNER --> (int ) = [None]
     ADD MEMBER FUN : foo --> int foo(double ,double );
     ADD MEMBER FUN : foochar --> void foo(char *);
     ADD STATIC FUNC: bar --> int bar(double );
     ADD STATIC FUNC: barchar --> void bar(char *);
     ADD STATIC FUNC: bar --> int bar(int );
     // C++ CLASS END 


     // C++ CLASS START : class Class
     ADD MEMBER     : member_data --> int  member_data; 
     ADD MEMBER FUN : member_func --> double member_func();
     ADD MEMBER FUN : pointer --> void pointer(Class *);
     ADD MEMBER FUN : retptr --> Class *retptr();
     // C++ CLASS END 


     // C++ CLASS START : class Foo3
     ADD MEMBER     : new_var --> double  var; 
     ADD STATIC VAR : new_static_var --> double  static_var; 
     ADD MEMBER FUN : add --> int sum(int ,int );
     ADD STATIC FUNC: product --> int mul(int ,int );
     ADD C++ CONST  : LAGER --> (int ) = [None]
     ADD C++ CONST  : ALE --> (int ) = [None]
     ADD C++ CONST  : STOUT --> (int ) = [None]
     ADD C++ CONST  : PILSNER --> (int ) = [None]
     ADD MEMBER FUN : foo --> int foo(double ,double );
     ADD MEMBER FUN : foochar --> void foo(char *);
     ADD STATIC FUNC: bar --> int bar(double );
     ADD STATIC FUNC: barchar --> void bar(char *);
     // C++ CLASS END 


     // C++ CLASS START : class Foo4
     ADD MEMBER     : new_var --> double  var; 
     ADD STATIC VAR : new_static_var --> double  static_var; 
     ADD MEMBER FUN : add --> int sum(int ,int );
     ADD STATIC FUNC: product --> int mul(int ,int );
     ADD C++ CONST  : LAGER --> (int ) = [None]
     ADD C++ CONST  : ALE --> (int ) = [None]
     ADD C++ CONST  : STOUT --> (int ) = [None]
     ADD C++ CONST  : PILSNER --> (int ) = [None]
     ADD MEMBER FUN : foo --> int foo(double ,double );
     ADD MEMBER FUN : foochar --> void foo(char *);
     ADD STATIC FUNC: bar --> int bar(double );
     ADD STATIC FUNC: barchar --> void bar(char *);
     // C++ CLASS END 


     // C++ CLASS START : class Bar
     ADD MEMBER     : member_data --> int  member_data; 
     ADD MEMBER FUN : member_func --> double member_func();
     ADD MEMBER FUN : pointer --> void pointer(Class *);
     ADD MEMBER FUN : retptr --> Class *retptr();
     // C++ CLASS END 


     // C++ CLASS START : class C
     ADD MEMBER FUN : new_name --> int old_name(int );
     // C++ CLASS END 

}  /* END INIT */
{
   int i;
   for (i = 0; _swig_mapping[i].n1; i++)
        SWIG_RegisterMapping(_swig_mapping[i].n1,_swig_mapping[i].n2,_swig_mapping[i].pcnv);
}
