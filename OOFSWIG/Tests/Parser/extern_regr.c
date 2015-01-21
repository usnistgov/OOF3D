/* DEBUG : Language specific headers go here */

/* DEBUG : Pointer conversion function here */

/* DEBUG : Language specific code here */

#define   SWIG_init     swig_init

#define   SWIG_name    "swig"
extern int  foo; 
extern int  foo1; 
extern int  foo2; 
extern int bar(int );
extern int bar1(int );
extern int bar2(double );
extern "C" int grok(int );
extern double &foo3(double &,int &);
WRAPPER : int  foo; 
WRAPPER : int  foo1; 
WRAPPER : int  foo2; 
WRAPPER : int bar(int );

WRAPPER : int bar1(int );

WRAPPER : int bar2(double );

WRAPPER : int grok(int );

WRAPPER : int flob(int );

WRAPPER : double &foo3(double &,int &);

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
     ADD VARIABLE   : foo --> int  foo; 
     ADD VARIABLE   : foo1 --> int  foo1; 
     ADD VARIABLE   : foo2 --> int  foo2; 
     ADD COMMAND    : bar --> int bar(int );
     ADD COMMAND    : bar1 --> int bar1(int );
     ADD COMMAND    : bar2 --> int bar2(double );
     ADD COMMAND    : grok --> int grok(int );
     ADD COMMAND    : flob --> int flob(int );
     ADD COMMAND    : foo3 --> double &foo3(double &,int &);
}  /* END INIT */
{
   int i;
   for (i = 0; _swig_mapping[i].n1; i++)
        SWIG_RegisterMapping(_swig_mapping[i].n1,_swig_mapping[i].n2,_swig_mapping[i].pcnv);
}
