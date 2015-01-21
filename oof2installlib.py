# -*- python -*-
# $RCSfile: oof2installlib.py,v $
# $Revision: 1.1.2.2 $
# $Author: langer $
# $Date: 2011/05/19 19:38:51 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Modify the "install_lib" command so that it runs "install_name_tool" on Macs.

from distutils.command import install_lib
from distutils import log
import os
import sys

shared_libs = []                # set by setup.py

class oof_install_lib(install_lib.install_lib):
    def install(self):
        outfiles = install_lib.install_lib.install(self)
        install_shlib = self.get_finalized_command("install_shlib")
        if sys.platform == 'darwin':
            # We get the shared library names and locations from
            # global variables, because if we import oof2config.py it
            # will create oof2config.pyc, and will cause a conflict
            # for people using "stow" to install oof2.
            shared_lib_dir = install_shlib.install_dir
            build_dir = self.get_finalized_command('install_shlib').build_dir
            installed_names = {}        # new name keyed by old name
            for lib in shared_libs:
                installed_names["lib%s.dylib"%lib] = \
                              "%s/lib%s.dylib" % (shared_lib_dir, lib)
            prefix = self.get_finalized_command('install').prefix
            for phile in outfiles:
                if phile.endswith(".so"):
                    # See which dylibs it links to
                    f = os.popen('otool -L %s' % phile, "r")
                    for line in f.readlines():
                        l = line.lstrip()
                        dylib = l.split()[0]
                        for k in installed_names.keys():
                            if dylib.endswith(k) and dylib!=installed_names[k]:
                                cmd = 'install_name_tool -change %s %s %s' % (
                                    dylib, installed_names[k], phile)
                                log.info(cmd)
                                errorcode = os.system(cmd)
                                if errorcode:
                                    raise errors.DistutilsExecError(
                                        "command failed: %s" % cmd)
                                break
        return outfiles
        

