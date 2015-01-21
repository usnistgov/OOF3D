%module native
%{

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
	      
%}

/* This file tests the %native directive */

%native(fact) wrap_fact;
%native(fact3) extern int wrap_fact(ClientData clientdata, Tcl_Interp *interp, int argc, char **argv);
%native(fact4) extern "C" int wrap_fact(ClientData clientdata, Tcl_Interp *interp, int argc, char **argv);







