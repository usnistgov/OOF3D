/* DEBUG : Language specific headers go here */

/* DEBUG : Pointer conversion function here */

/* DEBUG : Language specific code here */

#define   SWIG_init     swig_init

#define   SWIG_name    "swig"

double inline1(double &a) {
   inlined definition 1
}
double inline2() {
   inlined definition 2
}
double inline3() {
   inlined definition 3
}
int inline4();

int a;

static int foo1(int) {
   A static, but inlined function
}


#define BAR  4
static double foo()
{
   inlined definition 4;
}
WRAPPER : double inline1(double &);

WRAPPER : double inline2();

WRAPPER : double inline3();

WRAPPER : int inline4();

WRAPPER : int  a; 
WRAPPER : int foo1(int );

WRAPPER : double bar();

WRAPPER : double grok();

WRAPPER : double foo();

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
{0,0,0}};


/* MODULE INITIALIZATION */

void swig_init() {
     ADD COMMAND    : inline1 --> double inline1(double &);
     ADD COMMAND    : inline2 --> double inline2();
     ADD COMMAND    : inline3 --> double inline3();
     ADD COMMAND    : inline4 --> int inline4();
     ADD VARIABLE   : a --> int  a; 
     ADD COMMAND    : foo1 --> int foo1(int );
     ADD CONSTANT   : (int ) BAR = 4
     ADD COMMAND    : bar --> double bar();
     ADD COMMAND    : grok --> double grok();
     ADD COMMAND    : foo --> double foo();
}  /* END INIT */
{
   int i;
   for (i = 0; _swig_mapping[i].n1; i++)
        SWIG_RegisterMapping(_swig_mapping[i].n1,_swig_mapping[i].n2,_swig_mapping[i].pcnv);
}
