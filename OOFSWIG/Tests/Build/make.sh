#!/bin/sh

necho() {
   if [ "`echo -n`" = "-n" ]; then
      echo "${@}\c"
   else
      echo -n "${@}"
   fi
}

echo "Testing SWIG's ability to build different types of modules."
echo ""
echo "This test uses the file Makefile.template (in the top level directory)"
echo "to try and build various types of language extensions.  This makefile"
echo "is used by all of the SWIG examples and is installed by 'make install'"
echo "as swig_lib/Makefile.   If a build fails, it means that the target language"
echo "is not installed, SWIG's configure script wasn't able to find it,"
echo "or that SWIG incorrectly guessed compiler options.  To fix build"
echo "problems for installed languages, you will need to edit the file"
echo "Makefile.template manually."
echo ""

TARGET='tcl_static wish_static perl5_static python_static tcl_dynamic perl5_dynamic python_dynamic'

echo "Testing the build of C extensions : "
echo ""
echo "*** Note : Dynamic loading builds will fail on machines without dynamic loading support"
echo ""

for i in ${TARGET}; do 
necho "    Testing build : ${i} (C)"; 
if make -f Makefile_C ${i} >${i}.output 2>&1; then 
# See if SWIG generated any errors at all
	echo " ....... passed";
	rm -f ${i}.output;
else 
    echo " ....... FAILED. (See ${i}.output)";
fi;
done

echo ""
echo "Testing the build of C++ extensions : "
echo ""
echo "*** Disclaimer : Your mileage may vary..."
echo ""

for i in ${TARGET}; do 
necho "    Testing build : ${i} (C++)"; 
if make -f Makefile_CPP ${i} >${i}.c++.output 2>&1; then 
# See if SWIG generated any errors at all
	echo " ....... passed";
	rm -f ${i}.c++.output;
else 
    echo " ....... FAILED. (See ${i}.c++.output)";
fi;
done

echo ""
echo "Test complete."
echo ""
echo "For an explanation of common failures, see the file TROUBLESHOOTING"
echo "in the top level directory."
echo ""






