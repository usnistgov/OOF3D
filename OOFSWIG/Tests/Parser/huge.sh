#!/bin/sh
necho() {
   if [ "`echo -n`" = "-n" ]; then
      echo "${@}\c"
   else
      echo -n "${@}"
   fi
}

echo "*** Warning.  The following test hammers SWIG with more than"
echo "              10000 declarations in order to detect memory leaks"
echo "              and failures that might occur with large files."
echo "              It will use more than 15 Mbytes of disk space and may"
echo "              take several minutes to complete... (This is the last"
echo "              test so you can safely abort if you don't care)"
echo "Automatically generating input..."
echo "    perl makehuge.pl >huge.i"; perl makehuge.pl >huge.i
necho "    Testing : huge.i"
if ../../swig -I../../swig_lib -debug -dnone -c++ huge.i; then
echo " ....... passed"
else
echo " ....... FAILED ***"
fi
rm -f huge.i
rm -f huge_wrap*

