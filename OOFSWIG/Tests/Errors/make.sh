#!/bin/sh

necho() {
   if [ "`echo -n`" = "-n" ]; then
      echo "${@}\c"
   else
      echo -n "${@}"
   fi
}


IFILE='errors operator unclosed_hblock friend missing_struct missing_endif misplaced_cond missing_header
       unterm_string unterm_comment vararg'

echo "Testing some parser error handling..."

for i in ${IFILE}; do 
necho "    Testing : ${i}.i"; 
../../swig -I../../swig_lib -debug -dnone -c++ ${i}.i >${i}.output 2>&1; 
echo " ....... output written to ${i}.output";
rm -f ${i}_wrap*
done


