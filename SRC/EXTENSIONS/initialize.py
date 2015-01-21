# -*- python -*-
# $RCSfile: initialize.py,v $
# $Revision: 1.2.6.1 $
# $Author: langer $
# $Date: 2014/09/27 22:33:37 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

######

# If you want to explicitly load extensions every time OOF2 runs, then
# import their python modules here.  Be aware that this file will be
# overwritten when a new version of OOF2 is installed, so your edits
# will be lost.

# If you want all modules in the EXTENSIONS directory (this directory)
# to be loaded when OOF2 starts, then start OOF2 with the --autoload
# command line option.  You *don't* have to explicitly import
# extension modules if you use --autoload, but you *do* have to
# arrange for them to be built (by putting them in DIR.py in this
# directory, or by building them elsewhere and installing them in this
# directory).

## <Put your own import lines here>


##### 

# This loads all modules if --autoload has been specified.

from ooflib.common import autoload
import sys
import os.path
extmodname = 'ooflib.EXTENSIONS'
if autoload.autoload:
    extensionsmodule = sys.modules[extmodname]
    extensionsdir = extensionsmodule.__path__[0]
    files = os.listdir(extensionsdir)
    dont_load = ['__init__.py', 'DIR.py', 'initialize.py']
    for phile in files:
        if phile not in dont_load:
            fullname = os.path.join(extensionsdir, phile)
            if os.path.isdir(fullname):
                if os.path.exists(os.path.join(fullname, '__init__.py')):
                    exec 'import ' + extmodname + '.' + phile
            else:
                if phile.endswith('.py'):
                    exec 'import ' + extmodname + '.' + phile[:-3]
        

        
        
