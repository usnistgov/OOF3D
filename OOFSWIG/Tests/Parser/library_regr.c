/* DEBUG : Language specific headers go here */

/* DEBUG : Pointer conversion function here */

/* DEBUG : Language specific code here */

#define   SWIG_init     swig_init

#define   SWIG_name    "swig"


extern int  t_eint; 
extern short  t_eshort; 
extern long  t_elong; 
extern unsigned int  t_euint; 
extern unsigned short  t_eushort; 
extern unsigned long  t_eulong; 
extern signed int  t_esint; 
extern signed short  t_esshort; 
extern signed long  t_eslong; 
extern unsigned  t_eu; 
extern signed  t_es; 
extern signed char  t_eschar; 
extern unsigned char  t_euchar; 
extern char  t_echar; 
extern float  t_efloat; 
extern double  t_edouble; 
extern bool  t_ebool; 
extern int  ea; 
extern int * eb; 
extern int ** ec; 
extern int *** ed; 


enum months {JAN, FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC};
#define test_value 4

typedef struct Vector {
	double x,y,z;
} Vector;	

Vector v1;

int const_foo(int a, int b) {
	return a + b;
};

typedef int (*PFOO)(int, int);



WRAPPER : char *getenv(char *);

WRAPPER : void hello();

WRAPPER : int sum_int(int ,int );

WRAPPER : short sum_short(short ,short );

WRAPPER : long sum_long(long ,long );

WRAPPER : unsigned int sum_uint(unsigned int ,unsigned int );

WRAPPER : unsigned short sum_ushort(unsigned short ,unsigned short );

WRAPPER : unsigned long sum_ulong(unsigned long ,unsigned long );

WRAPPER : unsigned char sum_uchar(unsigned char ,unsigned char );

WRAPPER : signed int sum_sint(signed int ,signed int );

WRAPPER : signed short sum_sshort(signed short ,signed short );

WRAPPER : signed long sum_slong(signed long ,signed long );

WRAPPER : signed char sum_schar(signed char ,signed char );

WRAPPER : float sum_float(float ,float );

WRAPPER : double sum_double(double ,double );

WRAPPER : void prints(char *);

WRAPPER : void printc(char );

WRAPPER : int *sum_pint(int *,int *);

WRAPPER : short *sum_pshort(short *,short *);

WRAPPER : long *sum_plong(long *,long *);

WRAPPER : unsigned int *sum_puint(unsigned int *,unsigned int *);

WRAPPER : unsigned short *sum_pushort(unsigned short *,unsigned short *);

WRAPPER : unsigned long *sum_pulong(unsigned long *,unsigned long *);

WRAPPER : unsigned char *sum_puchar(unsigned char *,unsigned char *);

WRAPPER : signed int *sum_psint(signed int *,signed int *);

WRAPPER : signed short *sum_psshort(signed short *,signed short *);

WRAPPER : signed long *sum_pslong(signed long *,signed long *);

WRAPPER : signed char *sum_pschar(signed char *,signed char *);

WRAPPER : float *sum_pfloat(float *,float *);

WRAPPER : double *sum_pdouble(double *,double *);

WRAPPER : void *incr_ptr(void *,int );

WRAPPER : Vector *new_Vector(double ,double ,double );

WRAPPER : void print_Vector(Vector *);

WRAPPER : Vector addv(Vector ,Vector );

WRAPPER : int *new_int(int );

WRAPPER : short *new_short(short );

WRAPPER : long *new_long(long );

WRAPPER : unsigned int *new_uint(unsigned int );

WRAPPER : unsigned short *new_ushort(unsigned short );

WRAPPER : unsigned long *new_ulong(unsigned long );

WRAPPER : unsigned char *new_uchar(unsigned char );

WRAPPER : signed int *new_sint(signed int );

WRAPPER : signed short *new_sshort(signed short );

WRAPPER : signed long *new_slong(signed long );

WRAPPER : signed char *new_schar(signed char );

WRAPPER : float *new_float(float );

WRAPPER : double *new_double(double );

WRAPPER : void *malloc(int );

WRAPPER : struct Foo func(struct Foo );

WRAPPER : class Bar func1(class Bar *);

WRAPPER : union Grok func2(union Grok *);

WRAPPER : enum Enum func3(enum Enum2 );

WRAPPER : int  t_int; 
WRAPPER : short  t_short; 
WRAPPER : long  t_long; 
WRAPPER : unsigned int  t_uint; 
WRAPPER : unsigned short  t_ushort; 
WRAPPER : unsigned long  t_ulong; 
WRAPPER : signed int  t_sint; 
WRAPPER : signed short  t_sshort; 
WRAPPER : signed long  t_slong; 
WRAPPER : unsigned  t_u; 
WRAPPER : signed  t_s; 
WRAPPER : signed char  t_schar; 
WRAPPER : unsigned char  t_uchar; 
WRAPPER : char  t_char; 
WRAPPER : float  t_float; 
WRAPPER : double  t_double; 
WRAPPER : bool  t_bool; 
WRAPPER : int * t_aint; 
WRAPPER : double * t_adouble; 
WRAPPER : float *** t_pfloat; 
WRAPPER : struct Matrix1  t_struct; 
WRAPPER : class Matrix2  t_class; 
WRAPPER : union Matrix3  t_union; 
WRAPPER : Matrix4  t_user; 
WRAPPER : struct Matrix4 * t_pstruct; 
WRAPPER : class Matrix5 * t_pclass; 
WRAPPER : union Matrix6 * t_punion; 
WRAPPER : Matrix7 * t_puser; 
WRAPPER : int  a; 
WRAPPER : int * b; 
WRAPPER : int ** c; 
WRAPPER : int *** d; 
WRAPPER : int  t_eint; 
WRAPPER : short  t_eshort; 
WRAPPER : long  t_elong; 
WRAPPER : unsigned int  t_euint; 
WRAPPER : unsigned short  t_eushort; 
WRAPPER : unsigned long  t_eulong; 
WRAPPER : signed int  t_esint; 
WRAPPER : signed short  t_esshort; 
WRAPPER : signed long  t_eslong; 
WRAPPER : unsigned  t_eu; 
WRAPPER : signed  t_es; 
WRAPPER : signed char  t_eschar; 
WRAPPER : unsigned char  t_euchar; 
WRAPPER : char  t_echar; 
WRAPPER : float  t_efloat; 
WRAPPER : double  t_edouble; 
WRAPPER : bool  t_ebool; 
WRAPPER : int  ea; 
WRAPPER : int * eb; 
WRAPPER : int ** ec; 
WRAPPER : int *** ed; 
WRAPPER : char  aa[32]; 
WRAPPER : int  ai[100]; 
WRAPPER : Vector  av[200]; 
C++ CLASS DECLARATION : class Func
WRAPPER : double Func::div(double ,double );

C++ CLASS DECLARATION : class Func4
C++ CLASS DECLARATION : class Func2
C++ CLASS DECLARATION : class Data
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
C++ CLASS DECLARATION : class Foo
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
C++ CLASS START : class Func  ========================================

        CONSTRUCTOR   : Func *Func(double );
        DESTRUCTOR    : ~Func();
        MEMBER FUNC   : double add(double );

        MEMBER FUNC   : double abs();

        STATIC FUNC   : double mul(double ,double );
        MEMBER FUNC   : double sub(double &);

        MEMBER FUNC   : double &new_double(double );

C++ CLASS END ===================================================

C++ CLASS START : class Func2  ========================================

        MEMBER FUNC   : int add_int(int ,int );

        MEMBER FUNC   : short add_short(short ,short );

        MEMBER FUNC   : long add_long(long ,long );

        MEMBER FUNC   : unsigned int add_uint(unsigned int ,unsigned int );

        MEMBER FUNC   : unsigned short add_ushort(unsigned short ,unsigned short );

        MEMBER FUNC   : unsigned long add_ulong(unsigned long ,unsigned long );

        MEMBER FUNC   : unsigned char add_uchar(unsigned char ,unsigned char );

        MEMBER FUNC   : signed char add_char(signed char ,signed char );

        MEMBER FUNC   : float add_float(float ,float );

        MEMBER FUNC   : double add_double(double ,double );

        MEMBER FUNC   : void hello();

        MEMBER FUNC   : int *nothing_pint(int *,int *);

        MEMBER FUNC   : short *nothing_pshort(short *,short *);

        MEMBER FUNC   : long *nothing_plong(long *,long *);

        MEMBER FUNC   : unsigned int *nothing_puint(unsigned int *,unsigned int *);

        MEMBER FUNC   : unsigned short *nothing_pushort(unsigned short *,unsigned short *);

        MEMBER FUNC   : unsigned long *nothing_pulong(unsigned long *,unsigned long *);

        MEMBER FUNC   : unsigned char *nothing_puchar(unsigned char *,unsigned char *);

        MEMBER FUNC   : signed char *nothing_pschar(signed char *,signed char *);

        MEMBER FUNC   : float *nothing_pfloat(float *,float *);

        MEMBER FUNC   : double *nothing_pdouble(double *,double *);

        MEMBER FUNC   : void print(char *);

        MEMBER FUNC   : int &ref_int(int &);

        MEMBER FUNC   : short &ref_short(short &);

        MEMBER FUNC   : long &ref_long(long &);

        MEMBER FUNC   : unsigned int &ref_uint(unsigned int &);

        MEMBER FUNC   : unsigned short &ref_ushort(unsigned short &);

        MEMBER FUNC   : unsigned long &ref_ulong(unsigned long &);

        MEMBER FUNC   : unsigned char &ref_uchar(unsigned char &);

        MEMBER FUNC   : signed char &ref_schar(signed char &);

        MEMBER FUNC   : float &ref_float(float &);

        MEMBER FUNC   : double &ref_double(double &);

        MEMBER FUNC   : char &ref_char(char &);

C++ CLASS END ===================================================

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
    { "_ROnly","_class_ROnly",0},
    { "_signed_long","_long",0},
    { "_double","_FooBar",0},
    { "_double","_Real",0},
    { "_class_ROnlyBase","_class_ROnly",SwigROnlyToROnlyBase},
    { "_class_ROnlyBase","_ROnly",SwigROnlyToROnlyBase},
    { "_class_ROnlyBase","_ROnlyBase",0},
    { "_class_C","_C",0},
    { "_class_Foo","_Foo",0},
    { "_Real","_FooBar",0},
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
    { "_Bar","_class_Bar",0},
    { "_class_Data","_Data",0},
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
    { "_TwoD","_class_Square",SwigSquareToTwoD},
    { "_TwoD","_Square",SwigSquareToTwoD},
    { "_TwoD","_class_Circle",SwigCircleToTwoD},
    { "_TwoD","_Circle",SwigCircleToTwoD},
    { "_TwoD","_class_TwoD",0},
    { "_class_Bar","_Bar",0},
    { "_Func","_class_Func",0},
    { "_class_Cube","_Cube",0},
    { "_unsigned_long","_long",0},
    { "_Sphere","_class_Sphere",0},
    { "_FooBar","_double",0},
    { "_FooBar","_Real",0},
    { "_class_Func2","_Func2",0},
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
    { "_class_Func","_Func",0},
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
    { "_C","_class_C",0},
    { "_class_Class","_class_Bar",SwigBarToClass},
    { "_class_Class","_Bar",SwigBarToClass},
    { "_class_Class","_Class",0},
    { "_ROnlyBase","_class_ROnly",SwigROnlyToROnlyBase},
    { "_ROnlyBase","_ROnly",SwigROnlyToROnlyBase},
    { "_ROnlyBase","_class_ROnlyBase",0},
    { "_Func2","_class_Func2",0},
    { "_class_ENUM","_class_ENUM1",SwigENUM1ToENUM},
    { "_class_ENUM","_ENUM1",SwigENUM1ToENUM},
    { "_class_ENUM","_ENUM",0},
    { "_Foo","_class_Foo",0},
    { "_Data","_class_Data",0},
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
     ADD COMMAND    : getenv --> char *getenv(char *);
     ADD COMMAND    : hello --> void hello();
     ADD COMMAND    : sum_int --> int sum_int(int ,int );
     ADD COMMAND    : sum_short --> short sum_short(short ,short );
     ADD COMMAND    : sum_long --> long sum_long(long ,long );
     ADD COMMAND    : sum_uint --> unsigned int sum_uint(unsigned int ,unsigned int );
     ADD COMMAND    : sum_ushort --> unsigned short sum_ushort(unsigned short ,unsigned short );
     ADD COMMAND    : sum_ulong --> unsigned long sum_ulong(unsigned long ,unsigned long );
     ADD COMMAND    : sum_uchar --> unsigned char sum_uchar(unsigned char ,unsigned char );
     ADD COMMAND    : sum_sint --> signed int sum_sint(signed int ,signed int );
     ADD COMMAND    : sum_sshort --> signed short sum_sshort(signed short ,signed short );
     ADD COMMAND    : sum_slong --> signed long sum_slong(signed long ,signed long );
     ADD COMMAND    : sum_schar --> signed char sum_schar(signed char ,signed char );
     ADD COMMAND    : sum_float --> float sum_float(float ,float );
     ADD COMMAND    : sum_double --> double sum_double(double ,double );
     ADD COMMAND    : prints --> void prints(char *);
     ADD COMMAND    : printc --> void printc(char );
     ADD COMMAND    : sum_pint --> int *sum_pint(int *,int *);
     ADD COMMAND    : sum_pshort --> short *sum_pshort(short *,short *);
     ADD COMMAND    : sum_plong --> long *sum_plong(long *,long *);
     ADD COMMAND    : sum_puint --> unsigned int *sum_puint(unsigned int *,unsigned int *);
     ADD COMMAND    : sum_pushort --> unsigned short *sum_pushort(unsigned short *,unsigned short *);
     ADD COMMAND    : sum_pulong --> unsigned long *sum_pulong(unsigned long *,unsigned long *);
     ADD COMMAND    : sum_puchar --> unsigned char *sum_puchar(unsigned char *,unsigned char *);
     ADD COMMAND    : sum_psint --> signed int *sum_psint(signed int *,signed int *);
     ADD COMMAND    : sum_psshort --> signed short *sum_psshort(signed short *,signed short *);
     ADD COMMAND    : sum_pslong --> signed long *sum_pslong(signed long *,signed long *);
     ADD COMMAND    : sum_pschar --> signed char *sum_pschar(signed char *,signed char *);
     ADD COMMAND    : sum_pfloat --> float *sum_pfloat(float *,float *);
     ADD COMMAND    : sum_pdouble --> double *sum_pdouble(double *,double *);
     ADD COMMAND    : incr_ptr --> void *incr_ptr(void *,int );
     ADD COMMAND    : new_Vector --> Vector *new_Vector(double ,double ,double );
     ADD COMMAND    : print_Vector --> void print_Vector(Vector *);
     ADD COMMAND    : addv --> Vector addv(Vector ,Vector );
     ADD COMMAND    : new_int --> int *new_int(int );
     ADD COMMAND    : new_short --> short *new_short(short );
     ADD COMMAND    : new_long --> long *new_long(long );
     ADD COMMAND    : new_uint --> unsigned int *new_uint(unsigned int );
     ADD COMMAND    : new_ushort --> unsigned short *new_ushort(unsigned short );
     ADD COMMAND    : new_ulong --> unsigned long *new_ulong(unsigned long );
     ADD COMMAND    : new_uchar --> unsigned char *new_uchar(unsigned char );
     ADD COMMAND    : new_sint --> signed int *new_sint(signed int );
     ADD COMMAND    : new_sshort --> signed short *new_sshort(signed short );
     ADD COMMAND    : new_slong --> signed long *new_slong(signed long );
     ADD COMMAND    : new_schar --> signed char *new_schar(signed char );
     ADD COMMAND    : new_float --> float *new_float(float );
     ADD COMMAND    : new_double --> double *new_double(double );
     ADD COMMAND    : malloc --> void *malloc(int );
     ADD COMMAND    : func --> struct Foo func(struct Foo );
     ADD COMMAND    : func1 --> class Bar func1(class Bar *);
     ADD COMMAND    : func2 --> union Grok func2(union Grok *);
     ADD COMMAND    : func3 --> enum Enum func3(enum Enum2 );
     ADD VARIABLE   : t_int --> int  t_int; 
     ADD VARIABLE   : t_short --> short  t_short; 
     ADD VARIABLE   : t_long --> long  t_long; 
     ADD VARIABLE   : t_uint --> unsigned int  t_uint; 
     ADD VARIABLE   : t_ushort --> unsigned short  t_ushort; 
     ADD VARIABLE   : t_ulong --> unsigned long  t_ulong; 
     ADD VARIABLE   : t_sint --> signed int  t_sint; 
     ADD VARIABLE   : t_sshort --> signed short  t_sshort; 
     ADD VARIABLE   : t_slong --> signed long  t_slong; 
     ADD VARIABLE   : t_u --> unsigned  t_u; 
     ADD VARIABLE   : t_s --> signed  t_s; 
     ADD VARIABLE   : t_schar --> signed char  t_schar; 
     ADD VARIABLE   : t_uchar --> unsigned char  t_uchar; 
     ADD VARIABLE   : t_char --> char  t_char; 
     ADD VARIABLE   : t_float --> float  t_float; 
     ADD VARIABLE   : t_double --> double  t_double; 
     ADD VARIABLE   : t_bool --> bool  t_bool; 
     ADD VARIABLE   : t_aint --> int * t_aint; 
     ADD VARIABLE   : t_adouble --> double * t_adouble; 
     ADD VARIABLE   : t_pfloat --> float *** t_pfloat; 
     ADD VARIABLE   : t_struct --> struct Matrix1  t_struct; 
     ADD VARIABLE   : t_class --> class Matrix2  t_class; 
     ADD VARIABLE   : t_union --> union Matrix3  t_union; 
     ADD VARIABLE   : t_user --> Matrix4  t_user; 
     ADD VARIABLE   : t_pstruct --> struct Matrix4 * t_pstruct; 
     ADD VARIABLE   : t_pclass --> class Matrix5 * t_pclass; 
     ADD VARIABLE   : t_punion --> union Matrix6 * t_punion; 
     ADD VARIABLE   : t_puser --> Matrix7 * t_puser; 
     ADD VARIABLE   : a --> int  a; 
     ADD VARIABLE   : b --> int * b; 
     ADD VARIABLE   : c --> int ** c; 
     ADD VARIABLE   : d --> int *** d; 
     ADD VARIABLE   : t_eint --> int  t_eint; 
     ADD VARIABLE   : t_eshort --> short  t_eshort; 
     ADD VARIABLE   : t_elong --> long  t_elong; 
     ADD VARIABLE   : t_euint --> unsigned int  t_euint; 
     ADD VARIABLE   : t_eushort --> unsigned short  t_eushort; 
     ADD VARIABLE   : t_eulong --> unsigned long  t_eulong; 
     ADD VARIABLE   : t_esint --> signed int  t_esint; 
     ADD VARIABLE   : t_esshort --> signed short  t_esshort; 
     ADD VARIABLE   : t_eslong --> signed long  t_eslong; 
     ADD VARIABLE   : t_eu --> unsigned  t_eu; 
     ADD VARIABLE   : t_es --> signed  t_es; 
     ADD VARIABLE   : t_eschar --> signed char  t_eschar; 
     ADD VARIABLE   : t_euchar --> unsigned char  t_euchar; 
     ADD VARIABLE   : t_echar --> char  t_echar; 
     ADD VARIABLE   : t_efloat --> float  t_efloat; 
     ADD VARIABLE   : t_edouble --> double  t_edouble; 
     ADD VARIABLE   : t_ebool --> bool  t_ebool; 
     ADD VARIABLE   : ea --> int  ea; 
     ADD VARIABLE   : eb --> int * eb; 
     ADD VARIABLE   : ec --> int ** ec; 
     ADD VARIABLE   : ed --> int *** ed; 
     ADD VARIABLE   : aa --> char  aa[32]; 
     ADD VARIABLE   : ai --> int  ai[100]; 
     ADD VARIABLE   : av --> Vector  av[200]; 
     ADD CONSTANT   : (int ) ICON1 = 42
     ADD CONSTANT   : (int ) ICON2 = -13
     ADD CONSTANT   : (double ) FCON1 = 3.14159
     ADD CONSTANT   : (double ) FCON2 = 2.134e3
     ADD CONSTANT   : (double ) FCON3 = 2e3
     ADD CONSTANT   : (double ) FCON4 = 2e+3
     ADD CONSTANT   : (double ) FCON5 = 2e-3
     ADD CONSTANT   : (double ) FCON6 = -3e-7
     ADD CONSTANT   : (char *) CCON1 = a
     ADD CONSTANT   : (char *) SCON1 = hello world
     ADD CONSTANT   : (char *) CCON2 = \n
     ADD CONSTANT   : (char *) CCON3 = \123
     ADD CONSTANT   : (char *) CCON4 = \x13
     ADD CONSTANT   : (double ) FCON65 = .53
     ADD CONSTANT   : (int ) SIZE_INT = sizeof(int)
     ADD CONSTANT   : (int ) IEXPR = 2+3
     ADD CONSTANT   : (int ) IEXPR2 = 2*3
     ADD CONSTANT   : (int ) IEXPR3 = 3-2
     ADD CONSTANT   : (int ) IEXPR4 = 3/2
     ADD CONSTANT   : (int ) IEXPR5 = (2+3)
     ADD CONSTANT   : (int ) IEXPR6 = (2+3*((2+3)))/4
     ADD CONSTANT   : (double ) FEXPR = 3.14159*2.3
     ADD CONSTANT   : (double ) FEXPR2 = (3.14159)/(2.134e3)
     ADD CONSTANT   : (double ) FEXPR3 = (2.1+3.5*7.4)*2.1
     ADD CONSTANT   : (double ) FEXPR4 = 3.14+2
     ADD CONSTANT   : (double ) FEXPR5 = 8.89+(2+3)
     ADD CONSTANT   : (int ) BCON1 = 0x3f&0x8
     ADD CONSTANT   : (int ) BCON2 = 0x3f|0x822
     ADD CONSTANT   : (int ) BCON3 = 0x3f^0x822
     ADD CONSTANT   : (int ) BCON4 = ~0x3f
     ADD CONSTANT   : (int ) BCON5 = 0x3f<<4
     ADD CONSTANT   : (int ) BCON6 = 0x3f>>4
     ADD CONSTANT   : (int ) BCON7 = (1<<8)|(1<<7)|(1<<6)
     ADD CONSTANT   : (int ) BCON8 = ((1<<8)|(1<<7)|(1<<6))&(0x3f>>4)
     ADD CONSTANT   : (int ) JAN = JAN
     ADD CONSTANT   : (int ) FEB = FEB
     ADD CONSTANT   : (int ) MAR = MAR
     ADD CONSTANT   : (int ) APR = APR
     ADD CONSTANT   : (int ) MAY = MAY
     ADD CONSTANT   : (int ) JUN = JUN
     ADD CONSTANT   : (int ) JUL = JUL
     ADD CONSTANT   : (int ) AUG = AUG
     ADD CONSTANT   : (int ) SEP = SEP
     ADD CONSTANT   : (int ) OCT = OCT
     ADD CONSTANT   : (int ) NOV = NOV
     ADD CONSTANT   : (int ) DEC = DEC
     ADD CONSTANT   : (int ) READ = READ
     ADD CONSTANT   : (int ) WRITE = WRITE
     ADD CONSTANT   : (int ) USER = USER
     ADD CONSTANT   : (int ) SUPER = SUPER
     ADD CONSTANT   : (int ) ECON1 = ECON1
     ADD CONSTANT   : (int ) ECON2 = ECON2
     ADD CONSTANT   : (int ) ECON3 = ECON3
     ADD CONSTANT   : (int ) cpp_int = 6
     ADD CONSTANT   : (double ) cpp_double = 3.14159
     ADD CONSTANT   : (int ) test_value = test_value
     ADD CONSTANT   : (char *) cpp_char = Hello world
     ADD CONSTANT   : (unsigned int ) UINT = 2400000000U
     ADD CONSTANT   : (long ) LONG = 2100000000L
     ADD CONSTANT   : (unsigned long ) ULONG = 4000000000UL
     ADD CONSTANT   : (unsigned long ) ULONG2 = 4100000000LU
     ADD CONSTANT   : (double ) FCON7 = 4f
     ADD CONSTANT   : (double ) FCON8 = 4.76F
     ADD CONSTANT   : (double ) FCON9 = 5e-34F
     ADD CONSTANT   : (double ) FCON10 = 7.88234E+3L
     ADD CONSTANT   : (unsigned int ) UINT2 = 2400U+2300U-14U
     ADD CONSTANT   : (PFOO ) FOO_CALLBACK = const_foo
     ADD CONSTANT   : (Vector *) vecaddr = &v1
     ADD CONSTANT   : (int ) CAST1 = (int)4
     ADD CONSTANT   : (double ) CAST2 = (double)4
     ADD CONSTANT   : (float ) CAST3 = ((float)3.14159)
     ADD CONSTANT   : (double ) CAST4 = (Real)2.71828
     ADD CONSTANT   : (double ) CAST5 = (FooBar)2.66
     ADD CONSTANT   : (int ) CAST6 = (3+(short)2)
     ADD CONSTANT   : (int ) CAST7 = (13+(int)3.82930)
     ADD CONSTANT   : (int ) CAST8 = (FooBar)7.8
     ADD CONSTANT   : (int ) ECAST1 = ECAST1
     ADD CONSTANT   : (short ) ECAST2 = ECAST2
     ADD CONSTANT   : (char ) ECAST3 = ECAST3
     ADD CONSTANT   : (long ) ECAST4 = ECAST4
     ADD CONSTANT   : (int ) ECAST8 = ECAST8
     ADD CONSTANT   : (int ) COMMENT1 = 1
     ADD CONSTANT   : (char *) COMMENT2 = foo
     ADD COMMAND    : Func_div --> double Func::div(double ,double );
     ADD CONSTANT   : (int ) PEAR = PEAR
     ADD CONSTANT   : (int ) APPLE = APPLE
     ADD CONSTANT   : (double ) PI = 3.141592654
     ADD CONSTANT   : (int ) N = 1000
     ADD CONSTANT   : (char *) VERSION = 1.0
     ADD VARIABLE   : new_variable --> int  my_variable; 
     ADD COMMAND    : add --> double sum(double ,double );
     ADD COMMAND    : retClass --> Class *retClass();
     ADD COMMAND    : NewName --> void OldName(double );
     ADD COMMAND    : SameName --> void SameName(int );
     ADD COMMAND    : foo10 --> int foo10(double );
     ADD COMMAND    : new_name --> int old_name(double );

     // C++ CLASS START : class Func
     ADD CONSTRUCT  : Func --> Func *Func(double );
     ADD DESTRUCT  : Func --> ~Func();
     ADD MEMBER FUN : add --> double add(double );
     ADD MEMBER FUN : abs --> double abs();
     ADD STATIC FUNC: mul --> double mul(double ,double );
     ADD MEMBER FUN : sub --> double sub(double &);
     ADD MEMBER FUN : new_double --> double &new_double(double );
     // C++ CLASS END 


     // C++ CLASS START : class Func2
     ADD MEMBER FUN : add_int --> int add_int(int ,int );
     ADD MEMBER FUN : add_short --> short add_short(short ,short );
     ADD MEMBER FUN : add_long --> long add_long(long ,long );
     ADD MEMBER FUN : add_uint --> unsigned int add_uint(unsigned int ,unsigned int );
     ADD MEMBER FUN : add_ushort --> unsigned short add_ushort(unsigned short ,unsigned short );
     ADD MEMBER FUN : add_ulong --> unsigned long add_ulong(unsigned long ,unsigned long );
     ADD MEMBER FUN : add_uchar --> unsigned char add_uchar(unsigned char ,unsigned char );
     ADD MEMBER FUN : add_char --> signed char add_char(signed char ,signed char );
     ADD MEMBER FUN : add_float --> float add_float(float ,float );
     ADD MEMBER FUN : add_double --> double add_double(double ,double );
     ADD MEMBER FUN : hello --> void hello();
     ADD MEMBER FUN : nothing_pint --> int *nothing_pint(int *,int *);
     ADD MEMBER FUN : nothing_pshort --> short *nothing_pshort(short *,short *);
     ADD MEMBER FUN : nothing_plong --> long *nothing_plong(long *,long *);
     ADD MEMBER FUN : nothing_puint --> unsigned int *nothing_puint(unsigned int *,unsigned int *);
     ADD MEMBER FUN : nothing_pushort --> unsigned short *nothing_pushort(unsigned short *,unsigned short *);
     ADD MEMBER FUN : nothing_pulong --> unsigned long *nothing_pulong(unsigned long *,unsigned long *);
     ADD MEMBER FUN : nothing_puchar --> unsigned char *nothing_puchar(unsigned char *,unsigned char *);
     ADD MEMBER FUN : nothing_pschar --> signed char *nothing_pschar(signed char *,signed char *);
     ADD MEMBER FUN : nothing_pfloat --> float *nothing_pfloat(float *,float *);
     ADD MEMBER FUN : nothing_pdouble --> double *nothing_pdouble(double *,double *);
     ADD MEMBER FUN : print --> void print(char *);
     ADD MEMBER FUN : ref_int --> int &ref_int(int &);
     ADD MEMBER FUN : ref_short --> short &ref_short(short &);
     ADD MEMBER FUN : ref_long --> long &ref_long(long &);
     ADD MEMBER FUN : ref_uint --> unsigned int &ref_uint(unsigned int &);
     ADD MEMBER FUN : ref_ushort --> unsigned short &ref_ushort(unsigned short &);
     ADD MEMBER FUN : ref_ulong --> unsigned long &ref_ulong(unsigned long &);
     ADD MEMBER FUN : ref_uchar --> unsigned char &ref_uchar(unsigned char &);
     ADD MEMBER FUN : ref_schar --> signed char &ref_schar(signed char &);
     ADD MEMBER FUN : ref_float --> float &ref_float(float &);
     ADD MEMBER FUN : ref_double --> double &ref_double(double &);
     ADD MEMBER FUN : ref_char --> char &ref_char(char &);
     // C++ CLASS END 


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
