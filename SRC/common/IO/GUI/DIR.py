# -*- python -*- 


# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modifed
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

dirname = 'GUI'
clib = 'oof3dcommonGUI'
clib_order = 100

pyfiles = [
    'activeareaPage.py',
    'activityViewer.py',
    'chooser.py',
    'colorparamwidgets.py',
    'console.py',
    'displaymethodwidget.py',
    'fileselector.py',
    'fixedwidthtext.py',
    'fontselector.py',
    'genericselectGUI.py',
    'gfxLabelTree.py',
    'gfxmenu.py',
    'gfxwindow.py',
    'gtklogger.py',
    'gtkutils.py',
    'guilogger.py',
    'historian.py',
    'initialize.py',
    'introPage.py',
    'labelledslider.py',
    'mainmenuGUI.py',
    'mainthreadGUI.py',
    'matrixparamwidgets.py',
    'microstructurePage.py',
    'mousehandler.py',
    'oofGUI.py',
    'oof_mainiteration.py',
    'parameterwidgets.py',
    'pixelPage.py',
    'pixelgroupwidget.py',
    'pixelinfoGUI.py',
    'pixelselectparamwidgets.py'
    'pixelselecttoolboxGUI.py',
    'progressbarGUI2.py',
    'questioner.py',
    'quit.py',
    'regclassfactory.py',
    'reporter_GUI.py',
    'reporterrorGUI.py',
    'subWindow.py',
    'toolboxGUI.py',
    'tutorialsGUI.py',
    'viewertoolboxGUI.py',
    'whowidget.py',
    'widgetscope.py',
    'workerGUI.py'
 ]

    
cfiles = ['progressGUI.C']
if USE_COCOA:
    cfiles.append('oofcanvas3d.mm')
else:
    cfiles.append('oofcanvas3d.C')

swigfiles = ['oofcanvas3d.swg', 'progressGUI.swg']

hfiles = ['oofcanvas3d.h', 'progressGUI.h']

swigpyfiles = ['progressGUI.spy']


def set_clib_flags(clib):
    import oof2setuputils

    # This is a hack that is needed by pkg-config on Macs using
    # fink. After merging its pangocairo branch, fink isn't putting
    # pango.pc and freetype2.pc in the default locations because they
    # can cause conflicts.  Once fink completes upgrading to modern
    # versions of these libraries, this hack can be removed.
    oof2setuputils.extend_path("PKG_CONFIG_PATH",
                               "/sw/lib/pango-ft219/lib/pkgconfig",
                               "/sw/lib/freetype219/lib/pkgconfig/")

    oof2setuputils.pkg_check("gtk+-2.0", GTK_VERSION, clib)
    oof2setuputils.pkg_check("pygtk-2.0", PYGTK_VERSION, clib)
    oof2setuputils.pkg_check("pygobject-2.0", PYGOBJECT_VERSION)
    addOOFlibs(clib, 'oof3dcommon')


