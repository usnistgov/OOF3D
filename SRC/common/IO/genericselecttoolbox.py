# -*- python -*-
# $RCSfile: genericselecttoolbox.py,v $
# $Revision: 1.13.18.8 $
# $Author: langer $
# $Date: 2013/05/07 21:16:55 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 


# Each way of selecting pixels is described by a SelectionMethod
# subclass.  SelectionMethod is a RegisteredClass.  The
# PixelSelectToolbox builds an OOFMenu with a menu item for each
# subclass.  The arguments to the menu item are the parameters for the
# SelectionMethod plus a list of Points.  Invoking the menu item
# creates an instance of the method and calls its select() function on
# the list of points.

# Each Registration for a SelectionMethod subclass needs to have an
# 'events' attribute, which consists of a list of strings indicating
# which mouse events it requires.  Allowed events are 'down', 'move',
# and 'up'.  

# The GUI version of the toolbox contains a RegisteredClassFactory for
# the SelectionMethods.  It installs itself as the graphics window's
# MouseHandler.  When it gets a 'down' mouse event, it starts storing
# the events' positions.  When it gets an 'up' event, it checks the
# 'events' setting for current SelectionMethod in the factory,
# constructs an OOFMenu argument list with the method's parameters,
# and invokes the non-GUI menu item, which creates the actual method
# does the selection.


from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common.IO import view
from ooflib.common import primitives
from ooflib.common import debug
from ooflib.common import registeredclass
from ooflib.common import toolbox
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from types import *
import math


# Base class for selection toolboxes.

# Child classes should implement the "signal" method, which
# notifies whoever needs to be notified when a new selection
# is available.
#
# Selections are made to Selection objects that live inside some
# source object.  For example, the pixel selection lives inside a
# Microstructure.  Child classes must provide a "sourceParams" method,
# which returns a list of Parameter objects that will be used to
# locate the source, and a "getSourceObject" method which, given the
# parameters, returns the Who object corresponding to the source.  See
# PixelSelectToolbox in pixelselect.py for an example.

# "name" is the menu tree entry, as well as the string that will
# appear on the notebook tab in the GUI window.  "method" is the base
# of a registered class hierarchy of selection operations.

class GenericSelectToolbox(toolbox.Toolbox):
    def __init__(self, name, method, gfxwindow, **extrakwargs):
        toolbox.Toolbox.__init__(self, name, gfxwindow)
        self.method = method
        self.lastclick = None           # position of last mouse click
        self.menu = None

        ## extrakwargs are passed to the getSelectionContext()
        ## function to retrieve the Who object of the current
        ## selection.
        self.extrakwargs = extrakwargs

        self.sb_callbacks = [
            switchboard.requestCallback(method, self.rebuildMenus)
            ]

    def close(self):
        for s in self.sb_callbacks:
            switchboard.removeCallback(s)
                
    def makeMenu(self, menu):
        self.menu = menu
        self.rebuildMenus()

    def rebuildMenus(self):
        # Put all the selection methods in the menu.
        if self.menu is not None:
            self.menu.clearSubMenu()
            sourceparams = self.sourceParams()
            self.menu.addItem(oofmenu.OOFMenuItem(
                'Clear',
                params=sourceparams,
                callback=self.clearCB,
                help="Clear the selection.",
                discussion="""<para>
                Unselect all %(object)ss in a %(source)s.  The
                <varname>%(param)s</varname> parameter is the
                %(source)s in which the %(object)ss are to be
                deselected.
                </para>""" % {'object':self.objName(),
                              'source':self.sourceName(),
                              'param':self.sourceParamName()}
                ))
            self.menu.addItem(oofmenu.OOFMenuItem(
                'Undo',
                params=sourceparams,
                callback=self.undoCB,
                help="Undo the selection.",
                discussion="""<para>
                Undo the previous %(object)s selection in the
                %(source)s named by the <varname>%(param)s</varname>
                parameter.  Previous selections are stored on a stack,
                and the <command>Undo</command> pops off the top of
                the stack.  The popped selection is not lost, however.
                It can be recovered with the <link
                linkend='MenuItem:%(parent)s.Redo'><command>Redo</command></link>
                command.

                </para><para>
                The stack has a finite size.  Once it is full, old
                selections will be lost when new selections are made.
                </para>""" % {'object':self.objName(),
                              'source':self.sourceName(),
                              'param':self.sourceParamName(),
                              'parent':self.menu.path()}
                ))
            self.menu.addItem(oofmenu.OOFMenuItem(
                'Redo',
                params=sourceparams,
                callback=self.redoCB,
                help="Redo the latest undone selection.",
                discussion="""<para>
                Redo the previously undone %(object)s selection in the
                %(source)s named in the <varname>%(param)s</varname>
                parameter.  Selections are stored on a stack, and the
                <link
                linkend='MenuItem:%(parent)s.Undo'><command>Undo</command></link>
                pops a selection off the stack.  The
                <command>Redo</command> places a selection back onto
                the stack.
                </para>
                <para>
                It's only possible to <command>Redo</command> a
                selection if no other %(object)ss have been selected
                since the last <link
                linkend='MenuItem:%(parent)s.Undo'><command>Undo</command></link>.
                </para>""" % {'object':self.objName(),
                              'source':self.sourceName(),
                              'param':self.sourceParamName(),
                              'parent':self.menu.path()}
                ))
            self.menu.addItem(oofmenu.OOFMenuItem(
                'Invert',
                params=sourceparams,
                callback=self.invertCB,
                help="Invert the selection.",
                discussion="""<para>
                Invert the current %(object)s selection in the
                %(source)s named by the <varname>%(param)s</varname>
                parameter.  All of the currently selected %(object)ss
                will be unselected and all of the currently unselected
                ones will be selected.
                </para>""" % {'object':self.objName(),
                              'source':self.sourceName(),
                              'param':self.sourceParamName()}
                ))
            for registration in self.method.registry:
                try:
                    help=registration.tip
                except AttributeError:
                    help = None
                params = sourceparams + registration.params + [
                   primitives.ListOfPointsParameter(
                        'points', tip=parameter.emptyTipString),
                   view.ViewParameter('view'),
                   parameter.BooleanParameter(
                        'shift', 0, tip="True for addition."),
                   parameter.BooleanParameter(
                        'ctrl', 0, tip="True for toggle.")
                   ]
                menuitem = self.menu.addItem(
                    oofmenu.OOFMenuItem(registration.name(),
                                        callback=self.selectCB,
                                        threadable=oofmenu.THREADABLE,
                                        params=params,
                                        help=help,
                                        discussion=registration.discussion))
                menuitem.data = registration

    def getSelection(self, params):
        # params is the dictionary of args passed to the menu
        # callback.  This returns the object that holds the current
        # selection.
        source = self.getSourceObject(params, self.gfxwindow())
        if source is not None:
            return source.getSelectionContext(**self.extrakwargs)

    def selectCB(self, menuitem, **params):
        # The arguments are the parameters for the SelectionMethod's
        # Registration, plus the list of points at which the mouse
        # events occurred and the current view.
        selMethodReg = menuitem.data    # selection method registration object

        # Construct arguments to pass to the registration to create an
        # instance.  Because the callback has more arguments than the
        # selection method, make sure that only the correct arguments
        # are used.
        argdict = {}
        for p in selMethodReg.params:
            argdict[p.name] = params[p.name]

        # create the SelectionMethod instance.
        selMethod = selMethodReg(**argdict)

        # fetch the Who object on which to act.
        source = self.getSourceObject(params, self.gfxwindow())
        if source is not None:
            selection = source.getSelectionContext(**self.extrakwargs)
            # In 3D, the pointlist is a list of screen coords, so it
            # really ought to be list of iPoints, but in 2D it's a
            # list of Points, because the screen coords have already
            # been translated into physical coords.  There's no good
            # way to do the translation in 3D before this point,
            # because the resolution of the z coordinate depends on
            # what's being selected.
            pointlist = params['points']    # mouse click points
            view = params['view']
            shift = params['shift']         # modifier keys
            ctrl = params['ctrl']
            if source and pointlist:
                selection.begin_writing()
                try:
                    selection.start()
                    if not shift and not ctrl:
                        selection.clear()
                    # Determine which selection func to pass to the
                    # selection method
                    if shift and ctrl:
                        # select pixels from selected objects
                        selector = selection.selectSelected
                    elif not shift and ctrl:
                        selector = selection.toggle
                    else:
                        selector = selection.select # simply selects objects
                    # Actually make the selection.
                    selMethod.select(source, self.gfxwindow(), pointlist, view,
                                     selector)
                finally:
                    selection.end_writing()
                # Tell the interested parties that the selection has changed.
                self.signal(selMethod, pointlist, selection)

    def clearCB(self, menuitem, **params):
        selection = self.getSelection(params)
        if selection is not None:
            selection.begin_writing()
            try:
                selection.start()
                selection.clear()
            finally:
                selection.end_writing()
            self.signal(None, None, selection)

    def undoCB(self, menuitem, **params):
        selection = self.getSelection(params)
        if selection is not None:
            selection.begin_writing()
            try:
                selection.undo()
            finally:
                selection.end_writing()
            self.signal(None, None, selection)

    def redoCB(self, menuitem, **params):
        selection = self.getSelection(params)
        if selection is not None:
            selection.begin_writing()
            try:
                selection.redo()
            finally:
                selection.end_writing()
            self.signal(None, None, selection)

    def invertCB(self, menuitem, **params):
        selection = self.getSelection(params)
        if selection is not None:
            selection.begin_writing()
            try:
                selection.start()
                selection.invert()
            finally:
                selection.end_writing()
            self.signal(None, None, selection)

    # Default signal, should be overridden by child classes.  This
    # routine should send a switchboard signal that is caught by the
    # appropriate graphics objects to tell them to update themselves.
    def signal(self, method, pointlist, who):
        pass

    def emptyMessage(self):
        # Called to get a string to display in the GUI when there's
        # nothing to make a selection from.  Redefined in subclasses
        # if more clarity is needed.
        return "No source!"
