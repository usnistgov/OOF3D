#!/bin/sh

necho() {
   if [ "`echo -n`" = "-n" ]; then
      echo "${@}\c"
   else
      echo -n "${@}"
   fi
}

echo "Testing the SWIG Documentation System"
echo ""
IFILE='after before sort end chop multiline ignore single enable skip text'

LOGFILE='../../test.log'

echo "Testing ASCII module"
for i in ${IFILE}; do 
necho "    Testing (ASCII+TCL): ${i}.i"; 
if ../../swig -I../../swig_lib -tcl -dascii -c++ ${i}.i >${i}.output 2>&1; then 
    rm -f ${i}.output;
# Look for a regression testing file
    if test -f ${i}_regr.doc; then
         if diff ${i}_regr.doc ${i}_wrap.doc > ${i}.ascii.diff; then
             echo " ....... passed"
             rm -f ${i}.ascii.diff
         else
              echo " ....... FAILED COMPARE (see ${i}.ascii.diff) ***";
              echo "${i}.i (TCL+ASCII) ....... FAILED COMPARE (see ${i}.ascii.diff) ***" >> ${LOGFILE}
         fi;
    else
# Regression testing file doesn't exist, create it
         echo " ....... passed (creating ${i}_regr.doc)"
         mv ${i}_wrap.doc ${i}_regr.doc
    fi;
rm -f ${i}_wrap*
else 
    echo " ....... FAILED (INTERAL ERROR) ***";
    echo "${i}.i (TCL+ASCII) ....... FAILED (INTERAL ERROR) ***" >> ${LOGFILE}
fi;
done

echo "Testing HTML module"
for i in ${IFILE}; do 
necho "    Testing (HTML+PERL5): ${i}.i"; 
if ../../swig -I../../swig_lib -perl5 -dhtml -c++ ${i}.i >${i}.output 2>&1; then 
    rm -f ${i}.output;
# Look for a regression testing file
    if test -f ${i}_regr.html; then
         if diff ${i}_regr.html ${i}_wrap.html > ${i}.html.diff; then
             echo " ....... passed"
             rm -f ${i}.html.diff
         else
              echo " ....... FAILED COMPARE (see ${i}.html.diff) ***";
              echo "${i}.i (PERL5+HTML) ....... FAILED COMPARE (see ${i}.html.diff) ***" >> ${LOGFILE}
         fi;
    else
# Regression testing file doesn't exist, create it
         echo " ....... passed (creating ${i}_regr.html)"
         mv ${i}_wrap.html ${i}_regr.html
    fi;
rm -f ${i}_wrap*
else 
    echo " ....... FAILED (INTERAL ERROR) ***";
    echo "${i}.i (PERL5+HTML) ....... FAILED (INTERAL ERROR) ***" >> ${LOGFILE}
fi;
done


echo "Testing LATEX module"
for i in ${IFILE}; do 
necho "    Testing (LATEX+PYTHON): ${i}.i"; 
if ../../swig -I../../swig_lib -python -dlatex -c++ ${i}.i >${i}.output 2>&1; then 
    rm -f ${i}.output;
# Look for a regression testing file
    if test -f ${i}_regr.tex; then
         if diff ${i}_regr.tex ${i}_wrap.tex > ${i}.tex.diff; then
             echo " ....... passed"
             rm -f ${i}.tex.diff
         else
              echo " ....... FAILED COMPARE (see ${i}.tex.diff) ***";
              echo "${i}.i (PYTHON+LATEX) ....... FAILED COMPARE (see ${i}.tex.diff) ***" >> ${LOGFILE}
         fi;
    else
# Regression testing file doesn't exist, create it
         echo " ....... passed (creating ${i}_regr.tex)"
         mv ${i}_wrap.tex ${i}_regr.tex
    fi;
rm -f ${i}_wrap*
else 
    echo " ....... FAILED (INTERAL ERROR) ***";
    echo "${i}.i (PYTHON+LATEX) ....... FAILED (INTERAL ERROR) ***" >> ${LOGFILE}
fi;
done

