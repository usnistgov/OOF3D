/* DEBUG : Language specific headers go here */

/* DEBUG : Pointer conversion function here */

/* DEBUG : Language specific code here */

#define   SWIG_init     swig_init

#define   SWIG_name    "swig"


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

SWIG POINTER-MAPPING TABLE

/*
 * This table is used by the pointer type-checker
 */
static struct { char *n1; char *n2; void *(*pcnv)(void *); } _swig_mapping[] = {
    { "_signed_long","_long",0},
    { "_double","_FooBar",0},
    { "_double","_Real",0},
    { "_Real","_FooBar",0},
    { "_Real","_double",0},
    { "_long","_unsigned_long",0},
    { "_long","_signed_long",0},
    { "_unsigned_long","_long",0},
    { "_FooBar","_double",0},
    { "_FooBar","_Real",0},
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
}  /* END INIT */
{
   int i;
   for (i = 0; _swig_mapping[i].n1; i++)
        SWIG_RegisterMapping(_swig_mapping[i].n1,_swig_mapping[i].n2,_swig_mapping[i].pcnv);
}
