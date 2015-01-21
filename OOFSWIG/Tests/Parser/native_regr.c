/* DEBUG : Language specific headers go here */

/* DEBUG : Pointer conversion function here */

/* DEBUG : Language specific code here */

#define   SWIG_init     swig_init

#define   SWIG_name    "swig"


int fact(int n) {
  if (n <= 1) return 1;
  else return n*fact(n-1);
}

int wrap_fact(ClientData clientdata, Tcl_Interp *interp,
	      int argc, char *argv[]) {
  int _result;
  int _arg0;
  if (argc != 2) {
    interp->result = "wrong # args";
    return TCL_ERROR;
  }

  _arg0 = atoi(argv[1]);
  _result = fact(_arg0);
  sprintf(interp->result,"%d",_result);
  return _result;
}
	      
extern int wrap_fact(ClientData ,Tcl_Interp *,int ,char **);
extern "C" int wrap_fact(ClientData ,Tcl_Interp *,int ,char **);
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
     ADD NATIVE     : fact --> wrap_fact
     ADD NATIVE     : fact3 --> wrap_fact
     ADD NATIVE     : fact4 --> wrap_fact
}  /* END INIT */
{
   int i;
   for (i = 0; _swig_mapping[i].n1; i++)
        SWIG_RegisterMapping(_swig_mapping[i].n1,_swig_mapping[i].n2,_swig_mapping[i].pcnv);
}
