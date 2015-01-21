#!/bin/sh
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

necho() {
   if [ "`echo -n`" = "-n" ]; then
      echo "${@}\c"
   else
      echo -n "${@}"
   fi
}

rm -f ${LOGFILE}

for i in ${IFILE}; do 
necho "    Testing : ${i}.i"; 
if ../../swig -I../../swig_lib -debug -dnone -c++ -objc ${i}.i >${i}.output 2>&1; then 
# See if SWIG generated any errors at all
    if test -f ${i}.output.msg; then 
        diff ${i}.output ${i}.output.msg > ${i}.msg.diff;
    else
	if test -s ${i}.output; then
             cp ${i}.output ${i}.output.msg
        fi;
    fi;
    if test -s ${i}.msg.diff; then
	echo " ....... FAILED with the following errors ***"
	cat ${i}.output;
	echo " ${i}.i ....... FAILED with the following errors ***" >> ${LOGFILE};
	cat ${i}.output >> ${LOGFILE};
    else
    rm -f ${i}.output;
    rm -f ${i}.msg.diff;
# Look for a regression testing file
    if test -f ${i}_regr.c; then
         if diff ${i}_regr.c ${i}_wrap.c > ${i}.diff; then
             echo " ....... passed"
             rm -f ${i}.diff
         else
              echo " ....... FAILED COMPARE (see ${i}.diff) ***";
              echo " ${i}.i ....... FAILED COMPARE (see ${i}.diff) ***" >> ${LOGFILE}
         fi;
    else
# Regression testing file doesn't exist, create it
         echo " ....... passed (creating ${i}_regr.c)";
         mv ${i}_wrap.c ${i}_regr.c
    fi;
    fi;
rm -f ${i}_wrap*
else 
    echo " ....... FAILED (INTERNAL ERROR) ***";
    echo " ${i}.i ....... FAILED (INTERNAL ERROR) ***" >> ${LOGFILE}
fi;
done

echo "
Performing parser/regression tests on Tcl module...
"

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

echo "
Performing parser/regression tests on Tcl8.0 module...
"
for i in ${IFILE}; do 
necho "    Testing (Tcl8) : ${i}.i"; 
if ../../swig -I../../swig_lib -tcl8 -dnone -c++ -objc ${i}.i >${i}.tcl8.output 2>&1; then 
# Look for a regression testing file
    if test -f ${i}_regr.tcl8.c; then
         if diff ${i}_regr.tcl8.c ${i}_wrap.c > ${i}.tcl8.diff; then
             echo " ....... passed"
             rm -f ${i}.tcl8.diff
         else
              echo " ....... FAILED COMPARE (see ${i}.tcl8.diff) ***";
              echo "${i}.i (Tcl8) ....... FAILED COMPARE (see ${i}.tcl8.diff) ***" >> ${LOGFILE}
         fi;
    else
# Regression testing file doesn't exist, create it
         echo " ....... passed (creating ${i}_regr.tcl8.c)"
         mv ${i}_wrap.c ${i}_regr.tcl8.c
    fi;
rm -f ${i}_wrap*
else 
    echo " ....... FAILED (INTERNAL ERROR) ***";
    echo "${i}.i (Tcl8) ....... FAILED (INTERNAL ERROR) ***" >> ${LOGFILE}
fi;
done

echo "
Performing parser/regression tests on Perl5 module...
"
for i in ${IFILE}; do 
necho "    Testing (Perl5) : ${i}.i"; 
if ../../swig -I../../swig_lib -perl5 -dnone -c++ -objc ${i}.i >${i}.perl5.output 2>&1; then 
# Look for a regression testing file
    if test -f ${i}_regr.perl5.c; then
         if diff ${i}_regr.perl5.c ${i}_wrap.c > ${i}.perl5.diff; then
             echo " ....... passed"
             rm -f ${i}.perl5.diff
         else
              echo " ....... FAILED COMPARE (see ${i}.perl5.diff) ***";
              echo "${i}.i (Perl5) ....... FAILED COMPARE (see ${i}.perl5.diff) ***" >> ${LOGFILE}
         fi;
    else
# Regression testing file doesn't exist, create it
         echo " ....... passed (creating ${i}_regr.perl5.c)"
         mv ${i}_wrap.c ${i}_regr.perl5.c
    fi;
rm -f ${i}_wrap*
else 
    echo " ....... FAILED (INTERNAL ERROR) ***";
    echo "${i}.i (Perl5) ....... FAILED (INTERNAL ERROR) ***" >> ${LOGFILE}
fi;
done


echo "
Performing parser/regression tests on Perl5 shadow classes...
"

for i in ${IFILE}; do 
necho "    Testing (Perl5 shadow) : ${i}.i"; 
if ../../swig -I../../swig_lib -perl5 -shadow -dnone -c++ -objc ${i}.i >${i}.perl5s.output 2>&1; then 
# Look for a regression testing file
    if test -f ${i}_regr.perl5s.c; then
         if diff ${i}_regr.perl5s.c ${i}_wrap.c > ${i}.perl5s.diff; then
             echo " ....... passed"
             rm -f ${i}.perl5s.diff
         else
              echo " ....... FAILED COMPARE (see ${i}.perl5s.diff) ***";
              echo "${i}.i (Perl5 shadow) ....... FAILED COMPARE (see ${i}.perl5s.diff) ***" >> ${LOGFILE}
         fi;
    else
# Regression testing file doesn't exist, create it
         echo " ....... passed (creating ${i}_regr.perl5s.c)"
         mv ${i}_wrap.c ${i}_regr.perl5s.c
    fi;
rm -f ${i}_wrap*
else 
    echo " ....... FAILED (INTERNAL ERROR) ***";
    echo "${i}.i (Perl5 shadow) ....... FAILED (INTERNAL ERROR) ***" >> ${LOGFILE}
fi;
done

echo "
Performing parser/regression tests on Python module...
"

for i in ${IFILE}; do 
necho "    Testing (Python) : ${i}.i"; 
if ../../swig -I../../swig_lib -python -dnone -c++ -objc ${i}.i >${i}.python.output 2>&1; then 
# Look for a regression testing file
    if test -f ${i}_regr.python.c; then
         if diff ${i}_regr.python.c ${i}_wrap.c > ${i}.python.diff; then
             echo " ....... passed"
             rm -f ${i}.python.diff
         else
              echo " ....... FAILED COMPARE (see ${i}.python.diff) ***";
              echo "${i}.i (Python) ....... FAILED COMPARE (see ${i}.python.diff) ***" >> ${LOGFILE}
         fi;
    else
# Regression testing file doesn't exist, create it
         echo " ....... passed (creating ${i}_regr.python.c)"
         mv ${i}_wrap.c ${i}_regr.python.c
    fi;
rm -f ${i}_wrap*
else 
    echo " ....... FAILED (INTERNAL ERROR) ***";
    echo "${i}.i (Python) ....... FAILED (INTERNAL ERROR) ***" >> ${LOGFILE}
fi;
done


echo "
Performing parser/regression tests on Python shadow classes...
"
for i in ${IFILE}; do 
necho "    Testing (Python shadow) : ${i}.i"; 
if ../../swig -I../../swig_lib -python -shadow -dnone -c++ -objc ${i}.i >${i}.pythons.output 2>&1; then 
# Look for a regression testing file
    if test -f ${i}_regr.pythons.c; then
         if diff ${i}_regr.pythons.c ${i}_wrap.c > ${i}.pythons.diff; then
             echo " ....... passed"
             rm -f ${i}.pythons.diff
         else
              echo " ....... FAILED COMPARE (see ${i}.pythons.diff) ***";
              echo "${i}.i (Python shadow) ....... FAILED COMPARE (see ${i}.pythons.diff) ***" >> ${LOGFILE}
         fi;
    else
# Regression testing file doesn't exist, create it
         echo " ....... passed (creating ${i}_regr.pythons.c)"
         mv ${i}_wrap.c ${i}_regr.pythons.c
    fi;
rm -f ${i}_wrap*
else 
    echo " ....... FAILED (INTERNAL ERROR) ***";
    echo "${i}.i (Python shadow) ....... FAILED (INTERNAL ERROR) ***" >> ${LOGFILE}
fi;
done

echo "
Performing parser/regression tests on Guile module...
"
for i in ${IFILE}; do 
necho "    Testing (Guile) : ${i}.i"; 
if ../../swig -I../../swig_lib -guile -dnone -c++ -objc ${i}.i >${i}.guile.output 2>&1; then 
# Look for a regression testing file
    if test -f ${i}_regr.guile.c; then
         if diff ${i}_regr.guile.c ${i}_wrap.c > ${i}.guile.diff; then
             echo " ....... passed"
             rm -f ${i}.guile.diff
         else
              echo " ....... FAILED COMPARE (see ${i}.guile.diff) ***";
              echo "${i}.i (Guile) ....... FAILED COMPARE (see ${i}.guile.diff) ***" >> ${LOGFILE}
         fi;
    else
# Regression testing file doesn't exist, create it
         echo " ....... passed (creating ${i}_regr.guile.c)"
         mv ${i}_wrap.c ${i}_regr.guile.c
    fi;
rm -f ${i}_wrap*
else 
    echo " ....... FAILED (INTERNAL ERROR) ***";
    echo "${i}.i (Guile) ....... FAILED (INTERNAL ERROR) ***" >> ${LOGFILE}
fi;
done

if test -s ${LOGFILE}; then
   echo "***** ERRORS were detected. See ${LOGFILE} for a summary."
fi


