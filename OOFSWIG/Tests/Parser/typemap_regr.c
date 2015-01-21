/* DEBUG : Language specific headers go here */

/* DEBUG : Pointer conversion function here */

/* DEBUG : Language specific code here */

#define   SWIG_init     swig_init

#define   SWIG_name    "swig"
WRAPPER : int foobar(double ,double );

WRAPPER : int parse_args(int ,char **);

WRAPPER : int parse_charpp(int ,char **);

C++ CLASS DECLARATION : class Foo
C++ CLASS DECLARATION : class Bar
WRAPPER : void no_typemap(double );

WRAPPER : void atest1(double [4]);

WRAPPER : void atest2(double [4][4]);

C++ CLASS DECLARATION : struct atest3
WRAPPER : void atest4(double [6]);

WRAPPER : void atest5(double [13][8]);

WRAPPER : void atest6(double [7][17]);

C++ CLASS DECLARATION : struct atest7
WRAPPER : void local1(double *);

WRAPPER : void local2(double *,double *);

WRAPPER : void local3(double *,double *,double *,double *);

WRAPPER : void apply1(double *);

WRAPPER : void apply2(double *,Real *);

WRAPPER : void apply3(double *,double *);

WRAPPER : void apply4(Matrix *);

WRAPPER : void apply5(double *,Real *,double *);

WRAPPER : void apply6(double *);

WRAPPER : double array1(double [4]);

WRAPPER : double array2(double [4],double [4],double [4]);

WRAPPER : void vector1(Vector *);

WRAPPER : void int1(int );

WRAPPER : void int2(int ,int );

WRAPPER : void int3(Integer );

WRAPPER : void int4(Integer ,Integer ,INT32 );

WRAPPER : void int5(Integer ,INT32 );

WRAPPER : void user1(int *);

WRAPPER : void user2(double **);

WRAPPER : void user3(FloatMatrix *);

WRAPPER : void user4(FloatMatrix );

WRAPPER : void user5(char *);

WRAPPER : void user6(int [4]);

WRAPPER : void user7(double **[]);

WRAPPER : void test1(double *,int [4],int [4],double *);

WRAPPER : void test2(Vector *,Vector *);

WRAPPER : double vars1(double );

WRAPPER : double vars2(double );

WRAPPER : double vars3(double );

WRAPPER : double vars4(double );

WRAPPER : double vars5(double );

WRAPPER : double vars6(double );

WRAPPER : double  vars7; 
C++ CLASS DECLARATION : struct varstruct
WRAPPER : double vars9(double );

WRAPPER : double vars10(double );

C++ CLASS START : class Foo  ========================================

        MEMBER FUNC   : double dmember(double );

        MEMBER FUNC   : void charpp(char **);

        MEMBER FUNC   : Vector &get_vector();

        MEMBER FUNC   : void set_vector(Vector &);

C++ CLASS END ===================================================

C++ CLASS START : class Bar  ========================================

        MEMBER FUNC   : double dmember2(double );

C++ CLASS END ===================================================

C++ CLASS START : struct atest3  ========================================

        ATTRIBUTE     : double  a[4]; 
        ATTRIBUTE     : double  b[4][4]; 
C++ CLASS END ===================================================

C++ CLASS START : struct atest7  ========================================

        ATTRIBUTE     : double  a[5][6]; 
        ATTRIBUTE     : double  b[10][]; 
C++ CLASS END ===================================================

C++ CLASS START : struct varstruct  ========================================

        ATTRIBUTE     : double  b; 
C++ CLASS END ===================================================

SWIG POINTER-MAPPING TABLE

/*
 * This table is used by the pointer type-checker
 */
static struct { char *n1; char *n2; void *(*pcnv)(void *); } _swig_mapping[] = {
    { "_signed_long","_long",0},
    { "_double","_Real",0},
    { "_struct_varstruct","_varstruct",0},
    { "_INT32","_Integer",0},
    { "_INT32","_unsigned_int",0},
    { "_INT32","_signed_int",0},
    { "_INT32","_int",0},
    { "_class_Foo","_Foo",0},
    { "_Real","_double",0},
    { "_long","_unsigned_long",0},
    { "_long","_signed_long",0},
    { "_Bar","_class_Bar",0},
    { "_class_Bar","_Bar",0},
    { "_unsigned_long","_long",0},
    { "_signed_int","_INT32",0},
    { "_signed_int","_Integer",0},
    { "_signed_int","_int",0},
    { "_struct_atest3","_atest3",0},
    { "_struct_atest7","_atest7",0},
    { "_unsigned_short","_short",0},
    { "_varstruct","_struct_varstruct",0},
    { "_signed_short","_short",0},
    { "_unsigned_int","_INT32",0},
    { "_unsigned_int","_Integer",0},
    { "_unsigned_int","_int",0},
    { "_short","_unsigned_short",0},
    { "_short","_signed_short",0},
    { "_int","_INT32",0},
    { "_int","_Integer",0},
    { "_int","_unsigned_int",0},
    { "_int","_signed_int",0},
    { "_Integer","_INT32",0},
    { "_Integer","_int",0},
    { "_Integer","_signed_int",0},
    { "_Integer","_unsigned_int",0},
    { "_atest3","_struct_atest3",0},
    { "_atest7","_struct_atest7",0},
    { "_Foo","_class_Foo",0},
{0,0,0}};


/* MODULE INITIALIZATION */

void swig_init() {
     ADD COMMAND    : foobar --> int foobar(double ,double );
     ADD COMMAND    : parse_args --> int parse_args(int ,char **);
     ADD COMMAND    : parse_charpp --> int parse_charpp(int ,char **);
     ADD COMMAND    : no_typemap --> void no_typemap(double );
     ADD COMMAND    : atest1 --> void atest1(double [4]);
     ADD COMMAND    : atest2 --> void atest2(double [4][4]);
     ADD COMMAND    : atest4 --> void atest4(double [6]);
     ADD COMMAND    : atest5 --> void atest5(double [13][8]);
     ADD COMMAND    : atest6 --> void atest6(double [7][17]);
     ADD COMMAND    : local1 --> void local1(double *);
     ADD COMMAND    : local2 --> void local2(double *,double *);
     ADD COMMAND    : local3 --> void local3(double *,double *,double *,double *);
     ADD COMMAND    : apply1 --> void apply1(double *);
     ADD COMMAND    : apply2 --> void apply2(double *,Real *);
     ADD COMMAND    : apply3 --> void apply3(double *,double *);
     ADD COMMAND    : apply4 --> void apply4(Matrix *);
     ADD COMMAND    : apply5 --> void apply5(double *,Real *,double *);
     ADD COMMAND    : apply6 --> void apply6(double *);
     ADD COMMAND    : array1 --> double array1(double [4]);
     ADD COMMAND    : array2 --> double array2(double [4],double [4],double [4]);
     ADD COMMAND    : vector1 --> void vector1(Vector *);
     ADD COMMAND    : int1 --> void int1(int );
     ADD COMMAND    : int2 --> void int2(int ,int );
     ADD COMMAND    : int3 --> void int3(Integer );
     ADD COMMAND    : int4 --> void int4(Integer ,Integer ,INT32 );
     ADD COMMAND    : int5 --> void int5(Integer ,INT32 );
     ADD COMMAND    : user1 --> void user1(int *);
     ADD COMMAND    : user2 --> void user2(double **);
     ADD COMMAND    : user3 --> void user3(FloatMatrix *);
     ADD COMMAND    : user4 --> void user4(FloatMatrix );
     ADD COMMAND    : user5 --> void user5(char *);
     ADD COMMAND    : user6 --> void user6(int [4]);
     ADD COMMAND    : user7 --> void user7(double **[]);
     ADD COMMAND    : test1 --> void test1(double *,int [4],int [4],double *);
     ADD COMMAND    : test2 --> void test2(Vector *,Vector *);
     ADD COMMAND    : vars1 --> double vars1(double );
     ADD COMMAND    : vars2 --> double vars2(double );
     ADD COMMAND    : vars3 --> double vars3(double );
     ADD COMMAND    : vars4 --> double vars4(double );
     ADD COMMAND    : vars5 --> double vars5(double );
     ADD COMMAND    : vars6 --> double vars6(double );
     ADD VARIABLE   : vars7 --> double  vars7; 
     ADD CONSTANT   : (double ) vars8 = 10
     ADD COMMAND    : vars9 --> double vars9(double );
     ADD COMMAND    : vars10 --> double vars10(double );

     // C++ CLASS START : class Foo
     ADD MEMBER FUN : dmember --> double dmember(double );
     ADD MEMBER FUN : charpp --> void charpp(char **);
     ADD MEMBER FUN : get_vector --> Vector &get_vector();
     ADD MEMBER FUN : set_vector --> void set_vector(Vector &);
     // C++ CLASS END 


     // C++ CLASS START : class Bar
     ADD MEMBER FUN : dmember2 --> double dmember2(double );
     // C++ CLASS END 


     // C++ CLASS START : struct atest3
     ADD MEMBER     : a --> double  a[4]; 
     ADD MEMBER     : b --> double  b[4][4]; 
     // C++ CLASS END 


     // C++ CLASS START : struct atest7
     ADD MEMBER     : a --> double  a[5][6]; 
     ADD MEMBER     : b --> double  b[10][]; 
     // C++ CLASS END 


     // C++ CLASS START : struct varstruct
     ADD MEMBER     : b --> double  b; 
     // C++ CLASS END 

}  /* END INIT */
{
   int i;
   for (i = 0; _swig_mapping[i].n1; i++)
        SWIG_RegisterMapping(_swig_mapping[i].n1,_swig_mapping[i].n2,_swig_mapping[i].pcnv);
}
