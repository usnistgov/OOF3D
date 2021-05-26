# -*- python -*- 


# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modifed
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

dirname = 'IO'
clib = 'oof3dengine'
if not NO_GUI:
    subdirs = ['GUI']

cfiles = ['propertyoutput.C', 'gridsource.C'] 

swigfiles = ['propertyoutput.swg', 'gridsource.swg',]

pyfiles = [
    'analyze.py', 'analyzemenu.py', 'anisocijkl.py',
    'boundaryconditionmenu.py', 'boundarymenu.py', 'contourdisplay.py',
    'displaymethods.py', 'isocijkl.py',
    'materialmenu.py', 'meshIO.py', 'meshcsdisplay.py',
    'meshcsparams.py', 'meshcstoolbox.py', 'meshinfo.py',
    'meshinfodisplay.py', 'meshmenu.py', 'meshparameters.py',
    'microstructuredisplay.py', 'movenode.py', 'movenodedisplay.py',
    'orientationmatrix.py', 'outputClones.py',
    'outputDefs.py', 'pbcparams.py', 'pinnodes.py', 'pinnodesdisplay.py',
    'propertymenu.py', 'skeletonIO.py', 'skeletonselectdisplay',
    'skeletonbdydisplay.py', 'skeletongroupmenu.py',
    'skeletongroupparams.py', 'skeletoninfo.py', 'skeletoninfodisplay.py',
    'skeletonmenu.py', 'skeletonselectiontoolbox.py',
    'skeletonselectmenu.py', 'profileIO.py',
    'pinnodesmenu.py', 'materialparameter.py', 'centerfilldisplay.py',
    'subproblemmenu.py', 'xmloutputs.py', 'output.py',
    'scheduledoutput.py', 'outputdestination.py', 'scheduledoutputmenu.py',
    'interfaceparameters.py', 'interfacemenu.py', 'genericinfotoolbox.py'] 


swigpyfiles = ['propertyoutput.spy']

hfiles = ['propertyoutput.h', 'gridsource.h']

if HAVE_MPI:
    pyfiles.extend([
            'boundaryconditionIPC.py', 'meshIPC.py', 'propertymenuIPC.py',
            'skeletonIPC.py', 'materialmenuIPC.py', 'solvermenuIPC.py',
            'subproblemIPC.py'])
