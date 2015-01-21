# -*- python -*-
# $RCSfile: menulogger.py,v $
# $Revision: 1.2.22.1 $
# $Author: langer $
# $Date: 2014/09/27 22:34:16 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

import gtk
import widgetlogger
import logutils
import loggers

import string

class MenuItemLogger(widgetlogger.WidgetLogger):
    classes = (gtk.MenuItem,)
    def location(self, menuitem, *args):
        parent, path = self._getMenuPath(menuitem)
        parentcode = loggers.findLogger(parent).location(parent)
        return "findMenu(%s, '%s')" % (parentcode, string.join(path, ':'))
    def record(self, obj, signal, *args):
        if signal == "activate":
            return ["%s.activate()" % self.location(obj, args)]
        return super(MenuItemLogger, self).record(obj, signal, *args)
    
    # Find a list of menu item names leading to the given
    # gtk.MenuItem.  This relies on setting gtk.Menu.oofparent in
    # gtklogger.set_submenu.  The return value is a tuple containing
    # the parent widget of the top of the menu hierarchy and the list
    # of menuitem names.
    def _getMenuPath(self, gtkmenuitem):
        path = [logutils.getWidgetName(gtkmenuitem)]
        parent = gtkmenuitem.get_parent()
        if isinstance(parent, gtk.Menu):
            try:
                pp = parent.oofparent
            except AttributeError:
                # Parent is a Menu, but doesn't have oofparent set.
                # It must be a pop-up menu.
                pass
            else:
                pparent, ppath = self._getMenuPath(pp)
                return pparent, ppath+path
        return parent, path

class MenuLogger(widgetlogger.WidgetLogger):
    classes = (gtk.MenuShell,)
    def record(self, obj, signal, *args):
        if signal == 'deactivate':
            return ["%s.deactivate()" % self.location(obj, args)]
        if signal == 'cancel':
            return ["%s.cancel()" % self.location(obj, args)]
        return super(MenuLogger, self).record(obj, signal, *args)
