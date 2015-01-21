# -*- python -*-
# $RCSfile: widgetscope.py,v $
# $Revision: 1.12.6.1 $
# $Author: langer $
# $Date: 2014/09/27 22:34:13 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# The WidgetScope class is used to arrange wrapped gtk widgets
# (usually instances of ParameterWidget subclasses) into a
# heirarchical (tree) structure.  Widgets can then search the
# heirarchy for other widgets on which they depend.  For example, the
# PixelGroupWidget presents a list of pixel groups, but since the
# groups are defined in a Microstructure, it needs to know which
# Microstructure's groups to list.  Therefore it uses the WidgetScope
# to find the closest Microstructure widget and gets the
# Microstructure from it.

# The main pages of the oofGUI window, RegisteredClassFactories, and
# ParameterTables all define WidgetScopes.  Other scopes can be
# defined as necessary.

# WidgetScopes serve a similar role to ParameterGroups, but in a
# different context.  ParameterGroups are used to associate specific
# OOFMenu Parameters with one another, and aren't used directly by the
# GUI.  WidgetScopes are used *only* by the GUI, and can group
# non-Parameter widgets, in principle.

## TODO LATER: As currently implemented, this doesn't quite work as
## promised.  Most widgets that search for their dependencies call
## WidgetScope.findWidget in their __init__s.  That means that the
## widget that they find will depend on the order in which widgets are
## added to the WidgetScope.  To do this correctly, there will have to
## be a way to tell widgets in a WidgetScope to re-run findWidget
## every time a widget is added or removed from the WidgetScope.
## Since the search process includes parent and child scopes, will it
## be necesssary to recompute *all* widget dependencies every time the
## contents of any scope changes?

from ooflib.common import debug

class WidgetScope:
    def __init__(self, parent):
        self.parent = parent            # another WidgetScope, or None
        self.children = []              # WidgetScopes
        self.widgetlist = []               # widget wrappers
        self.scope_data = {}            # Optional scope data.
        if parent is not None:
            parent._addChild(self)
    def _addChild(self, child):
        self.children.append(child)
    def _removeChild(self, child):
        self.children.remove(child)
    def destroyScope(self):
        for child in self.children:
            child.parent = None
        self.children = []
        for widget in self.widgetlist:
            widget.scope = None
        self.widgetlist = []
        if self.parent:
            self.parent._removeChild(self)
        self.parent = None
    def addWidget(self, widget):
        debug.mainthreadTest()
        self.widgetlist.append(widget)
    def removeWidget(self, widget):
        self.widgetlist.remove(widget)
    def findWidget(self, condition, excluded=None):
        debug.mainthreadTest()
        # Search through widgets in related WidgetScopes, returning
        # the first one that satisfies the condition.  The search
        # order is
        #   1.  Widgets in this scope
        #   2.  This scope's child scopes' widgets, recursively.
        #   3.  This scope's parent scope's widgets and scopes, recursively.
        for widget in self.widgetlist:
            if widget is not excluded and condition(widget):
                return widget
        for scope in self.children:
            if scope is not excluded:
                result = scope.findWidget(condition, excluded=self)
                if result is not None:
                    return result
        if self.parent and self.parent is not excluded:
            if condition(self.parent):
                return self.parent
            return self.parent.findWidget(condition, excluded=self)
#     def getPrevious(self, widget):      # is this used? useful?
#         for i in range(len(self.widgetlist)-1):
#             if self.widgetlist[i+1] is widget:
#                 return self.widgetlist[i]
    # Scope data operations -- simple.
    def setData(self, key, value):
        self.scope_data[key]=value
    def findData(self, key):
        try:
            return self.scope_data[key]
        except KeyError:
            if self.parent:
                return self.parent.findData(key)
            raise
