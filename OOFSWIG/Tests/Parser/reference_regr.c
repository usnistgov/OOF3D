/* DEBUG : Language specific headers go here */

/* DEBUG : Pointer conversion function here */

/* DEBUG : Language specific code here */

#define   SWIG_init     swig_init

#define   SWIG_name    "swig"
extern double foo(double &);
extern double &foobar2(double &,double &);
extern int dot_product(Vector ,Vector );
extern double mutt(double &);
WRAPPER : double bar(double &);

WRAPPER : double &foobar(double &,double &);

WRAPPER : double foo(double &);

WRAPPER : double &foobar2(double &,double &);

WRAPPER : int dot_product(Vector ,Vector );

WRAPPER : double mutt(double &);

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
     ADD COMMAND    : bar --> double bar(double &);
     ADD COMMAND    : foobar --> double &foobar(double &,double &);
     ADD COMMAND    : foo --> double foo(double &);
     ADD COMMAND    : foobar2 --> double &foobar2(double &,double &);
     ADD COMMAND    : dot_product --> int dot_product(Vector ,Vector );
     ADD COMMAND    : mutt --> double mutt(double &);
}  /* END INIT */
{
   int i;
   for (i = 0; _swig_mapping[i].n1; i++)
        SWIG_RegisterMapping(_swig_mapping[i].n1,_swig_mapping[i].n2,_swig_mapping[i].pcnv);
}
