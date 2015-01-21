/* DEBUG : Language specific headers go here */

/* DEBUG : Pointer conversion function here */

/* DEBUG : Language specific code here */

#define   SWIG_init     swig_init

#define   SWIG_name    "swig"
C++ CLASS DECLARATION : class Shape
C++ CLASS DECLARATION : class TwoD
C++ CLASS DECLARATION : class ThreeD
C++ CLASS DECLARATION : class Circle
C++ CLASS DECLARATION : class Square
C++ CLASS DECLARATION : class Sphere
C++ CLASS DECLARATION : class Cube
C++ CLASS DECLARATION : class ENUM
C++ CLASS DECLARATION : class ENUM1
C++ CLASS DECLARATION : class ROnlyBase
C++ CLASS DECLARATION : class ROnly
C++ CLASS START : class Shape  ========================================

        DESTRUCTOR    : ~Shape();
        CONSTRUCTOR   : Shape *Shape();
        MEMBER FUNC   : void ref();

        MEMBER FUNC   : void deref();

        MEMBER FUNC   : int get_ref();

        ATTRIBUTE     : int  color; 
        MEMBER FUNC   : void print();

        ATTRIBUTE     : char * name; 
C++ CLASS END ===================================================

C++ CLASS START : class TwoD  ========================================

inheriting from baseclass : Shape
static void *SwigTwoDToShape(void *ptr) {
    TwoD *src;
    Shape *dest;
    src = (TwoD *) ptr;
    dest = (Shape *) src;
    return (void *) dest;
}

        DESTRUCTOR    : ~TwoD();
        MEMBER FUNC   : void set_center(double ,double );

        MEMBER FUNC   : double area();

        MEMBER FUNC   : double perimeter();

        MEMBER FUNC   : void print();

        MEMBER FUNC   : void print_center();

        MEMBER FUNC   : void ref();

        MEMBER FUNC   : void deref();

        MEMBER FUNC   : int get_ref();

        ATTRIBUTE     : int  color; 
        ATTRIBUTE     : char * name; 
C++ CLASS END ===================================================

C++ CLASS START : class ThreeD  ========================================

inheriting from baseclass : Shape
static void *SwigThreeDToShape(void *ptr) {
    ThreeD *src;
    Shape *dest;
    src = (ThreeD *) ptr;
    dest = (Shape *) src;
    return (void *) dest;
}

        DESTRUCTOR    : ~ThreeD();
        MEMBER FUNC   : void set_center(double ,double ,double );

        MEMBER FUNC   : double volume();

        MEMBER FUNC   : double surface();

        MEMBER FUNC   : void print();

        MEMBER FUNC   : void print_center();

        MEMBER FUNC   : void ref();

        MEMBER FUNC   : void deref();

        MEMBER FUNC   : int get_ref();

        ATTRIBUTE     : int  color; 
        ATTRIBUTE     : char * name; 
C++ CLASS END ===================================================

C++ CLASS START : class Circle  ========================================

inheriting from baseclass : TwoD
static void *SwigCircleToTwoD(void *ptr) {
    Circle *src;
    TwoD *dest;
    src = (Circle *) ptr;
    dest = (TwoD *) src;
    return (void *) dest;
}

static void *SwigCircleToShape(void *ptr) {
    Circle *src;
    Shape *dest;
    src = (Circle *) ptr;
    dest = (Shape *) src;
    return (void *) dest;
}

        CONSTRUCTOR   : Circle *Circle(double );
        MEMBER FUNC   : double area();

        MEMBER FUNC   : double perimeter();

        MEMBER FUNC   : void print();

        MEMBER FUNC   : void set_center(double ,double );

        MEMBER FUNC   : void print_center();

        MEMBER FUNC   : void ref();

        MEMBER FUNC   : void deref();

        MEMBER FUNC   : int get_ref();

        ATTRIBUTE     : int  color; 
        ATTRIBUTE     : char * name; 
C++ CLASS END ===================================================

C++ CLASS START : class Square  ========================================

inheriting from baseclass : TwoD
static void *SwigSquareToTwoD(void *ptr) {
    Square *src;
    TwoD *dest;
    src = (Square *) ptr;
    dest = (TwoD *) src;
    return (void *) dest;
}

static void *SwigSquareToShape(void *ptr) {
    Square *src;
    Shape *dest;
    src = (Square *) ptr;
    dest = (Shape *) src;
    return (void *) dest;
}

        CONSTRUCTOR   : Square *Square(double );
        MEMBER FUNC   : double area();

        MEMBER FUNC   : double perimeter();

        MEMBER FUNC   : void print();

        MEMBER FUNC   : void set_center(double ,double );

        MEMBER FUNC   : void print_center();

        MEMBER FUNC   : void ref();

        MEMBER FUNC   : void deref();

        MEMBER FUNC   : int get_ref();

        ATTRIBUTE     : int  color; 
        ATTRIBUTE     : char * name; 
C++ CLASS END ===================================================

C++ CLASS START : class Sphere  ========================================

inheriting from baseclass : ThreeD
static void *SwigSphereToThreeD(void *ptr) {
    Sphere *src;
    ThreeD *dest;
    src = (Sphere *) ptr;
    dest = (ThreeD *) src;
    return (void *) dest;
}

static void *SwigSphereToShape(void *ptr) {
    Sphere *src;
    Shape *dest;
    src = (Sphere *) ptr;
    dest = (Shape *) src;
    return (void *) dest;
}

        CONSTRUCTOR   : Sphere *Sphere(double );
        MEMBER FUNC   : double volume();

        MEMBER FUNC   : double surface();

        MEMBER FUNC   : void print();

        MEMBER FUNC   : void set_center(double ,double ,double );

        MEMBER FUNC   : void print_center();

        MEMBER FUNC   : void ref();

        MEMBER FUNC   : void deref();

        MEMBER FUNC   : int get_ref();

        ATTRIBUTE     : int  color; 
        ATTRIBUTE     : char * name; 
C++ CLASS END ===================================================

C++ CLASS START : class Cube  ========================================

inheriting from baseclass : ThreeD
static void *SwigCubeToThreeD(void *ptr) {
    Cube *src;
    ThreeD *dest;
    src = (Cube *) ptr;
    dest = (ThreeD *) src;
    return (void *) dest;
}

static void *SwigCubeToShape(void *ptr) {
    Cube *src;
    Shape *dest;
    src = (Cube *) ptr;
    dest = (Shape *) src;
    return (void *) dest;
}

        CONSTRUCTOR   : Cube *Cube(double );
        MEMBER FUNC   : double volume();

        MEMBER FUNC   : double surface();

        MEMBER FUNC   : void print();

        MEMBER FUNC   : void set_center(double ,double ,double );

        MEMBER FUNC   : void print_center();

        MEMBER FUNC   : void ref();

        MEMBER FUNC   : void deref();

        MEMBER FUNC   : int get_ref();

        ATTRIBUTE     : int  color; 
        ATTRIBUTE     : char * name; 
C++ CLASS END ===================================================

C++ CLASS START : class ENUM  ========================================

        C++ CONST     : (int ) ALE = [None]
        C++ CONST     : (int ) LAGER = [None]
        C++ CONST     : (int ) STOUT = [None]
        C++ CONST     : (int ) PILSNER = [None]
        MEMBER FUNC   : void foo(ENUM::Enum1 );

        MEMBER FUNC   : ENUM::Real bar(ENUM::Real );

C++ CLASS END ===================================================

C++ CLASS START : class ENUM1  ========================================

inheriting from baseclass : ENUM
static void *SwigENUM1ToENUM(void *ptr) {
    ENUM1 *src;
    ENUM *dest;
    src = (ENUM1 *) ptr;
    dest = (ENUM *) src;
    return (void *) dest;
}

        MEMBER FUNC   : void foo2(ENUM::Enum1 );

        MEMBER FUNC   : ENUM::Real bar2(ENUM::Real );

        C++ CONST     : (int ) ALE = [None]
        C++ CONST     : (int ) LAGER = [None]
        C++ CONST     : (int ) STOUT = [None]
        C++ CONST     : (int ) PILSNER = [None]
        MEMBER FUNC   : void foo(ENUM::Enum1 );

        MEMBER FUNC   : ENUM::Real bar(ENUM::Real );

C++ CLASS END ===================================================

C++ CLASS START : class ROnlyBase  ========================================

        ATTRIBUTE     : int  x; 
        ATTRIBUTE     : int  y; 
C++ CLASS END ===================================================

C++ CLASS START : class ROnly  ========================================

inheriting from baseclass : ROnlyBase
static void *SwigROnlyToROnlyBase(void *ptr) {
    ROnly *src;
    ROnlyBase *dest;
    src = (ROnly *) ptr;
    dest = (ROnlyBase *) src;
    return (void *) dest;
}

        ATTRIBUTE     : int  x; 
        ATTRIBUTE     : int  y; 
C++ CLASS END ===================================================

SWIG POINTER-MAPPING TABLE

/*
 * This table is used by the pointer type-checker
 */
static struct { char *n1; char *n2; void *(*pcnv)(void *); } _swig_mapping[] = {
    { "_ROnly","_class_ROnly",0},
    { "_signed_long","_long",0},
    { "_double","_Real",0},
    { "_class_ROnlyBase","_class_ROnly",SwigROnlyToROnlyBase},
    { "_class_ROnlyBase","_ROnly",SwigROnlyToROnlyBase},
    { "_class_ROnlyBase","_ROnlyBase",0},
    { "_Real","_double",0},
    { "_Cube","_class_Cube",0},
    { "_long","_unsigned_long",0},
    { "_long","_signed_long",0},
    { "_class_Shape","_class_Cube",SwigCubeToShape},
    { "_class_Shape","_Cube",SwigCubeToShape},
    { "_class_Shape","_class_Sphere",SwigSphereToShape},
    { "_class_Shape","_Sphere",SwigSphereToShape},
    { "_class_Shape","_class_Square",SwigSquareToShape},
    { "_class_Shape","_Square",SwigSquareToShape},
    { "_class_Shape","_class_Circle",SwigCircleToShape},
    { "_class_Shape","_Circle",SwigCircleToShape},
    { "_class_Shape","_class_ThreeD",SwigThreeDToShape},
    { "_class_Shape","_ThreeD",SwigThreeDToShape},
    { "_class_Shape","_class_TwoD",SwigTwoDToShape},
    { "_class_Shape","_TwoD",SwigTwoDToShape},
    { "_class_Shape","_Shape",0},
    { "_ENUM1","_class_ENUM1",0},
    { "_TwoD","_class_Square",SwigSquareToTwoD},
    { "_TwoD","_Square",SwigSquareToTwoD},
    { "_TwoD","_class_Circle",SwigCircleToTwoD},
    { "_TwoD","_Circle",SwigCircleToTwoD},
    { "_TwoD","_class_TwoD",0},
    { "_class_Cube","_Cube",0},
    { "_unsigned_long","_long",0},
    { "_Sphere","_class_Sphere",0},
    { "_Square","_class_Square",0},
    { "_signed_int","_int",0},
    { "_unsigned_short","_short",0},
    { "_Shape","_class_Cube",SwigCubeToShape},
    { "_Shape","_Cube",SwigCubeToShape},
    { "_Shape","_class_Sphere",SwigSphereToShape},
    { "_Shape","_Sphere",SwigSphereToShape},
    { "_Shape","_class_Square",SwigSquareToShape},
    { "_Shape","_Square",SwigSquareToShape},
    { "_Shape","_class_Circle",SwigCircleToShape},
    { "_Shape","_Circle",SwigCircleToShape},
    { "_Shape","_class_ThreeD",SwigThreeDToShape},
    { "_Shape","_ThreeD",SwigThreeDToShape},
    { "_Shape","_class_TwoD",SwigTwoDToShape},
    { "_Shape","_TwoD",SwigTwoDToShape},
    { "_Shape","_class_Shape",0},
    { "_class_ROnly","_ROnly",0},
    { "_ThreeD","_class_Cube",SwigCubeToThreeD},
    { "_ThreeD","_Cube",SwigCubeToThreeD},
    { "_ThreeD","_class_Sphere",SwigSphereToThreeD},
    { "_ThreeD","_Sphere",SwigSphereToThreeD},
    { "_ThreeD","_class_ThreeD",0},
    { "_Circle","_class_Circle",0},
    { "_class_Sphere","_Sphere",0},
    { "_class_TwoD","_class_Square",SwigSquareToTwoD},
    { "_class_TwoD","_Square",SwigSquareToTwoD},
    { "_class_TwoD","_class_Circle",SwigCircleToTwoD},
    { "_class_TwoD","_Circle",SwigCircleToTwoD},
    { "_class_TwoD","_TwoD",0},
    { "_signed_short","_short",0},
    { "_class_Square","_Square",0},
    { "_ENUM","_class_ENUM1",SwigENUM1ToENUM},
    { "_ENUM","_ENUM1",SwigENUM1ToENUM},
    { "_ENUM","_class_ENUM",0},
    { "_unsigned_int","_int",0},
    { "_short","_unsigned_short",0},
    { "_short","_signed_short",0},
    { "_class_ThreeD","_class_Cube",SwigCubeToThreeD},
    { "_class_ThreeD","_Cube",SwigCubeToThreeD},
    { "_class_ThreeD","_class_Sphere",SwigSphereToThreeD},
    { "_class_ThreeD","_Sphere",SwigSphereToThreeD},
    { "_class_ThreeD","_ThreeD",0},
    { "_class_Circle","_Circle",0},
    { "_class_ENUM1","_ENUM1",0},
    { "_int","_unsigned_int",0},
    { "_int","_signed_int",0},
    { "_ROnlyBase","_class_ROnly",SwigROnlyToROnlyBase},
    { "_ROnlyBase","_ROnly",SwigROnlyToROnlyBase},
    { "_ROnlyBase","_class_ROnlyBase",0},
    { "_class_ENUM","_class_ENUM1",SwigENUM1ToENUM},
    { "_class_ENUM","_ENUM1",SwigENUM1ToENUM},
    { "_class_ENUM","_ENUM",0},
{0,0,0}};


/* MODULE INITIALIZATION */

void swig_init() {

     // C++ CLASS START : class Shape
     ADD DESTRUCT  : Shape --> ~Shape();
     ADD CONSTRUCT  : Shape --> Shape *Shape();
     ADD MEMBER FUN : ref --> void ref();
     ADD MEMBER FUN : deref --> void deref();
     ADD MEMBER FUN : get_ref --> int get_ref();
     ADD MEMBER     : color --> int  color; 
     ADD MEMBER FUN : print --> void print();
     ADD MEMBER     : name --> char * name; 
     // C++ CLASS END 


     // C++ CLASS START : class TwoD
     ADD DESTRUCT  : TwoD --> ~TwoD();
     ADD MEMBER FUN : set_center --> void set_center(double ,double );
     ADD MEMBER FUN : area --> double area();
     ADD MEMBER FUN : perimeter --> double perimeter();
     ADD MEMBER FUN : print --> void print();
     ADD MEMBER FUN : print_center --> void print_center();
     ADD MEMBER FUN : ref --> void ref();
     ADD MEMBER FUN : deref --> void deref();
     ADD MEMBER FUN : get_ref --> int get_ref();
     ADD MEMBER     : color --> int  color; 
     ADD MEMBER     : name --> char * name; 
     // C++ CLASS END 


     // C++ CLASS START : class ThreeD
     ADD DESTRUCT  : ThreeD --> ~ThreeD();
     ADD MEMBER FUN : set_center --> void set_center(double ,double ,double );
     ADD MEMBER FUN : volume --> double volume();
     ADD MEMBER FUN : surface --> double surface();
     ADD MEMBER FUN : print --> void print();
     ADD MEMBER FUN : print_center --> void print_center();
     ADD MEMBER FUN : ref --> void ref();
     ADD MEMBER FUN : deref --> void deref();
     ADD MEMBER FUN : get_ref --> int get_ref();
     ADD MEMBER     : color --> int  color; 
     ADD MEMBER     : name --> char * name; 
     // C++ CLASS END 


     // C++ CLASS START : class Circle
     ADD CONSTRUCT  : Circle --> Circle *Circle(double );
     ADD MEMBER FUN : area --> double area();
     ADD MEMBER FUN : perimeter --> double perimeter();
     ADD MEMBER FUN : print --> void print();
     ADD MEMBER FUN : set_center --> void set_center(double ,double );
     ADD MEMBER FUN : print_center --> void print_center();
     ADD MEMBER FUN : ref --> void ref();
     ADD MEMBER FUN : deref --> void deref();
     ADD MEMBER FUN : get_ref --> int get_ref();
     ADD MEMBER     : color --> int  color; 
     ADD MEMBER     : name --> char * name; 
     // C++ CLASS END 


     // C++ CLASS START : class Square
     ADD CONSTRUCT  : Square --> Square *Square(double );
     ADD MEMBER FUN : area --> double area();
     ADD MEMBER FUN : perimeter --> double perimeter();
     ADD MEMBER FUN : print --> void print();
     ADD MEMBER FUN : set_center --> void set_center(double ,double );
     ADD MEMBER FUN : print_center --> void print_center();
     ADD MEMBER FUN : ref --> void ref();
     ADD MEMBER FUN : deref --> void deref();
     ADD MEMBER FUN : get_ref --> int get_ref();
     ADD MEMBER     : color --> int  color; 
     ADD MEMBER     : name --> char * name; 
     // C++ CLASS END 


     // C++ CLASS START : class Sphere
     ADD CONSTRUCT  : Sphere --> Sphere *Sphere(double );
     ADD MEMBER FUN : volume --> double volume();
     ADD MEMBER FUN : surface --> double surface();
     ADD MEMBER FUN : print --> void print();
     ADD MEMBER FUN : set_center --> void set_center(double ,double ,double );
     ADD MEMBER FUN : print_center --> void print_center();
     ADD MEMBER FUN : ref --> void ref();
     ADD MEMBER FUN : deref --> void deref();
     ADD MEMBER FUN : get_ref --> int get_ref();
     ADD MEMBER     : color --> int  color; 
     ADD MEMBER     : name --> char * name; 
     // C++ CLASS END 


     // C++ CLASS START : class Cube
     ADD CONSTRUCT  : Cube --> Cube *Cube(double );
     ADD MEMBER FUN : volume --> double volume();
     ADD MEMBER FUN : surface --> double surface();
     ADD MEMBER FUN : print --> void print();
     ADD MEMBER FUN : set_center --> void set_center(double ,double ,double );
     ADD MEMBER FUN : print_center --> void print_center();
     ADD MEMBER FUN : ref --> void ref();
     ADD MEMBER FUN : deref --> void deref();
     ADD MEMBER FUN : get_ref --> int get_ref();
     ADD MEMBER     : color --> int  color; 
     ADD MEMBER     : name --> char * name; 
     // C++ CLASS END 


     // C++ CLASS START : class ENUM
     ADD C++ CONST  : ALE --> (int ) = [None]
     ADD C++ CONST  : LAGER --> (int ) = [None]
     ADD C++ CONST  : STOUT --> (int ) = [None]
     ADD C++ CONST  : PILSNER --> (int ) = [None]
     ADD MEMBER FUN : foo --> void foo(ENUM::Enum1 );
     ADD MEMBER FUN : bar --> ENUM::Real bar(ENUM::Real );
     // C++ CLASS END 


     // C++ CLASS START : class ENUM1
     ADD MEMBER FUN : foo2 --> void foo2(ENUM::Enum1 );
     ADD MEMBER FUN : bar2 --> ENUM::Real bar2(ENUM::Real );
     ADD C++ CONST  : ALE --> (int ) = [None]
     ADD C++ CONST  : LAGER --> (int ) = [None]
     ADD C++ CONST  : STOUT --> (int ) = [None]
     ADD C++ CONST  : PILSNER --> (int ) = [None]
     ADD MEMBER FUN : foo --> void foo(ENUM::Enum1 );
     ADD MEMBER FUN : bar --> ENUM::Real bar(ENUM::Real );
     // C++ CLASS END 


     // C++ CLASS START : class ROnlyBase
     ADD MEMBER     : x --> int  x; 
     ADD MEMBER     : y --> int  y; 
     // C++ CLASS END 


     // C++ CLASS START : class ROnly
     ADD MEMBER     : x --> int  x; 
     ADD MEMBER     : y --> int  y; 
     // C++ CLASS END 

}  /* END INIT */
{
   int i;
   for (i = 0; _swig_mapping[i].n1; i++)
        SWIG_RegisterMapping(_swig_mapping[i].n1,_swig_mapping[i].n2,_swig_mapping[i].pcnv);
}
