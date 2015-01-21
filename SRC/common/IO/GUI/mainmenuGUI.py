# -*- python -*-
# $RCSfile: mainmenuGUI.py,v $
# $Revision: 1.46.2.4 $
# $Author: langer $
# $Date: 2014/09/27 01:20:03 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# This file adds GUI code to the menu items defined in common.IO.mainmenu

from ooflib.SWIG.common import switchboard
from ooflib.common.IO import gfxmanager
from ooflib.common import debug
from ooflib.common import enum
from ooflib.common.IO import mainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO.GUI import activityViewer
from ooflib.common.IO.GUI import fontselector
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import tooltips
import gtk
import os

##########################

from ooflib.common.IO.GUI import quit
mainmenu.OOF.File.Quit.add_gui_callback(quit.queryQuit)

############################

def open_activityviewer(menuitem):
    activityViewer.openActivityViewer()
    menuitem()                          # just logs this command
mainmenu.OOF.Windows.Activity_Viewer.add_gui_callback(open_activityviewer)

############################

def toggleTips(menuitem, value):
    debug.mainthreadTest()
    if value:
        tooltips.enable_tooltips()
    else:
        tooltips.disable_tooltips()

## TODO 3.1: Uncomment this if we figure out how to disable tooltips
## again.  The way it used to work isn't available in new versions of
## gtk+.

# mainmenu.OOF.Help.addItem(
#     oofmenu.CheckOOFMenuItem('Show_Tooltips', 1,
#                              callback=toggleTips,
#                              threadable = oofmenu.UNTHREADABLE,
#                              gui_only=1,
#                              ordering=-9,
#                              help='Turn annoying pop-up hints off.'))

#############################

def setFont_gui(menuitem):
    fontname = fontselector.getFontName()
    if fontname:
        menuitem.callWithDefaults(fontname=fontname)

mainmenu.OOF.Settings.Fonts.Widgets.add_gui_callback(setFont_gui)

def reallySetFont(fontname):
    debug.mainthreadTest()
    settings = gtk.settings_get_default()
    settings.set_property("gtk-font-name", fontname)
    switchboard.notify('gtk font changed')

switchboard.requestCallbackMain('change font', reallySetFont)

##############################

# The text font is actually set by the widgets that use it. This code
# here just sets up the callback to get the font, and also stores it
# where it can be found by new widgets.

fixedfont = "Mono 12"
mainmenu.OOF.Settings.Fonts.Fixed.add_gui_callback(setFont_gui)

def setFixedFont(fontname):
    global fixedfont
    fixedfont = fontname

def getFixedFont():
    global fixedfont
    return fixedfont

switchboard.requestCallbackMain('change fixed font', setFixedFont)

##############################

themedirs = [gtk.rc_get_theme_dir(),
             os.path.join(os.path.expanduser("~"), ".themes")]

themes = []
for dir in themedirs:
    try:
        themes += os.listdir(dir)
    except:
        pass

if themes:
    # This is ugly... We can't use an EnumParam for the theme, because the
    # theme names are only known when the GUI is loaded.  But it's easiest
    # to use a EnumParameter and a ParameterDialog to get the value.  So
    # we create an Enum and an EnumParameter just for the GUI, then pass
    # the string to the menuitem.

    class ThemeEnum(enum.EnumClass(*themes)): pass

    themeParam = enum.EnumParameter('theme', ThemeEnum)

    def setTheme_gui(menuitem):
        if parameterwidgets.getParameters(themeParam,
                                          title="Choose a Gnome Theme"):
            themename = themeParam.value.name
            menuitem.callWithDefaults(theme=themename)

    mainmenu.OOF.Settings.Theme.add_gui_callback(setTheme_gui)

    def reallySetTheme(themename):
        debug.mainthreadTest()
        settings = gtk.settings_get_default()
        settings.set_property("gtk-theme-name", themename)

    switchboard.requestCallbackMain('change theme', reallySetTheme)
