#!/bin/sh

necho() {
   if [ "`echo -n`" = "-n" ]; then
      echo "${@}\c"
   else
      echo -n "${@}"
   fi
}

echo "Testing the SWIG C/C++ parser..."

# Make some of the larger files
perl makelarge.pl >large_comment.i
perl makeheader.pl >large_header.i

IFILE='
addmethods array code conditional constant cpp_const cpp_data cpp_func
cpp_inherit cpp_misc defarg doc enum_cond except extern function graph inline
library macro modlist multiline multinherit native nested new objc opengl ref
reference rename struct template test0.1a typedef typemap unsigned value
variable vector_ex void zero
large_comment
large_header'

LOGFILE='../../test.log'

rm -f ${LOGFILE}

echo "\nPerforming parser/regression tests on Tcl module..."
for i in ${IFILE}; do 
necho "    Testing (Tcl) : ${i}.i"; 
if ../../swig -I../../swig_lib -tcl -dnone -c++ -objc ${i}.i >${i}.tcl.output 2>&1; then 
# Look for a regression testing file
    if test -f ${i}_regr.tcl.c; then
         if diff ${i}_regr.tcl.c ${i}_wrap.c > ${i}.tcl.diff; then
             echo " ....... passed"
             rm -f ${i}.tcl.diff
         else
              echo " ....... FAILED COMPARE (see ${i}.tcl.diff) ***";
              echo "${i}.i (Tcl) ....... FAILED COMPARE (see ${i}.tcl.diff) ***" >> ${LOGFILE}
         fi;
    else
# Regression testing file doesn't exist, create it
         echo " ....... passed (creating ${i}_regr.tcl.c)"
         mv ${i}_wrap.c ${i}_regr.tcl.c
    fi;
rm -f ${i}_wrap*
else 
    echo " ....... FAILED (INTERNAL ERROR) ***";
    echo "${i}.i (Tcl) ....... FAILED (INTERNAL ERROR) ***" >> ${LOGFILE}
fi;
done

if test -s ${LOGFILE}; then
   echo "***** ERRORS were detected. See ${LOGFILE} for a summary."
fi


