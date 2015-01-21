# -*- python -*-
# $RCSfile: gfxmenu.py,v $
# $Revision: 1.56.2.4 $
# $Author: langer $
# $Date: 2014/07/30 21:28:37 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.common import debug
from ooflib.common import mainthread
from ooflib.common import utils
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import tooltips
from ooflib.common.IO.oofmenu import *
import gtk

def gtkOOFMenu(menu, accelgroup=None):
    """
    Function to turn an OOFMenu into GTK+.  The leading GtkMenuItem is
    returned.
    """
    debug.mainthreadTest()
    base = gtk.MenuItem(utils.underscore2space(menu.name))
    gtklogger.setWidgetName(base, menu.name)
    new_gtkmenu = gtk.Menu()
    try:
        menu.gtkmenu.append(new_gtkmenu)
    except AttributeError:
        menu.gtkmenu = [new_gtkmenu]

    new_gtkmenu.connect("destroy", menu.gtkmenu_destroyed)
                        
    gtklogger.set_submenu(base, new_gtkmenu)
    menu.setOption('accelgroup', accelgroup)

    for item in menu:
        if not (item.secret or item.getOption('cli_only')):
            item.construct_gui(menu, new_gtkmenu, accelgroup)
    return base


def gtkOOFMenuBar(menu, bar=None, accelgroup=None):
    """
    Function to turn an OOFMenu into a GTK+ MenuBar.  Reuse the given
    GtkMenuBar, if one is provided.
    """
    debug.mainthreadTest()
    if not bar is None:
        # remove old menus from bar
        bar.foreach(gtk.Object.destroy)
    else:
        bar = gtk.MenuBar()
    try:
        menu.gtkmenu.append(bar)
    except AttributeError:
        menu.gtkmenu = [bar]
        
    bar.connect("destroy", menu.gtkmenu_destroyed)
    
    menu.setOption('accelgroup', accelgroup)

    for item in menu:
        if not (item.secret or item.getOption('cli_only')):
            item.construct_gui(menu, bar, accelgroup)
    return bar

def gtkOOFPopUpMenu(menu, basewidget):
    # Create a pop-up menu for an OOFMenu. The basewidget argument
    # can be any existing gtk Widget on the same screen as the pop-up.
    # The pop-up is returned. 

    # Example:
    #  popup = gtkOOFPopUpMenu(oofmenu, basewidget)
    #  gtklogger.connect(basewidget, 'button-press-event', callback)
    #
    #  def callback(gtkobj, event):
    #     if event.button == 3:  # right-click
    #         popup.popup(None, None, None, event.button, event.time)
    #         ## The Nones are some vestigial gtk cruft, apparently.
    debug.mainthreadTest()
    popupmenu = gtk.Menu()
    gtklogger.newTopLevelWidget(popupmenu, 'PopUp-'+menu.name)
    popupmenu.set_screen(basewidget.get_screen())
    gtklogger.connect_passive(popupmenu, 'deactivate')
    for item in menu:
        item.construct_gui(menu, popupmenu, None)
    popupmenu.show_all()
    return popupmenu


###########################

# Extend the OOFMenu classes so that they can construct the gtk menu

#######################

class MenuCallBackWrapper:
    def __init__(self, menuitem):
        self.menuitem = menuitem
    def __call__(self, gtkmenuitem, *args):
        if self.menuitem.gui_callback is None:
            # No special gui callback.
            if self.menuitem.nargs() > 0:
                # Ask for args in a standard dialog box.
                if parameterwidgets.getParameters(
                    title=self.menuitem.name, data={'menuitem':self.menuitem},
                    *self.menuitem.params):
                    # Call and log the cli callback.
                    self.menuitem.callWithDefaults()
            else:
                # No gui callback and no args.  Call and log the cli callback.
                self.menuitem()
        else:
            # Call, but don't log, the gui callback.
            self.menuitem.gui_callback(self.menuitem)

def _gtklabel(self, gtkitem):
    debug.mainthreadTest()
    name = utils.underscore2space(self.name)
    # Add ellipsis automatically if there's an automatically generated
    # gui_callback.
    if self.ellipsis or (self.params and not self.gui_callback):
        name = name + '...'
    # Add tooltip.
    if self.helpstr:
        label = gtk.EventBox()
        if self.accel:                  # add accelerator too
            l2 = gtk.AccelLabel(name)
            l2.set_accel_widget(gtkitem)
        else:
            l2 = gtk.Label(name)         # don't add accelerator
        l2.set_alignment(0.0, 0.5)
        label.add(l2)
        tooltips.set_tooltip_text(label, self.helpstr)
    else:                               # don't add tooltip
        if self.accel:
            label = gtk.AccelLabel(name)
            label.set_accel_widget(gtkitem)
        else:
            label = gtk.Label(name)
        label.set_alignment(0.0, 0.5)
    label.show_all()
    return label

OOFMenuItem.gtklabel = _gtklabel

# Utility function to check if all of this menu item's children
# are visible.  Returns false if there are no children.  This tells
# the parent whether or not to construct a submenu, and prevents the
# construction of empty submenus.  Visibility is a GUI thing.
def _OOFMenuItem_children_visible(self):
    if not self.items:
        return None
    for i in self.items:
        if not (i.secret or i.getOption('cli_only')):
            return 1 # Return true on the first visible item.
    return None # Redundant, None is default return value, but clearer.

OOFMenuItem.children_visible = _OOFMenuItem_children_visible
    
def _OOFMenuItem_construct_gui(self, base, parent_menu, accelgroup):
    # "base" is this menu item's OOF menu parent, and "parent_menu" is
    # the to-be-constructed GtkMenuItem's gtk container.
    debug.mainthreadTest()
    if not (self.secret or self.getOption('cli_only')):

        new_gtkitem = gtk.MenuItem() # Built with no label.
        gtklogger.setWidgetName(new_gtkitem, self.name)
        new_gtkitem.add(self.gtklabel(new_gtkitem))
        try:
            self.gtkitem.append(new_gtkitem)
        except AttributeError:
            self.gtkitem = [new_gtkitem]
            
        new_gtkitem.connect("destroy", self.gtkitem_destroyed)
        
        parent_menu.insert(new_gtkitem, self.gui_order())
        if self.help_menu:
            base.gtkhelpmenu = 1
            new_gtkitem.set_right_justified(True)

        if (self.callback is None) and (self.gui_callback is None) \
               and self.children_visible():

            new_gtkmenu = gtk.Menu()
            try:
                self.gtkmenu.append(new_gtkmenu)
            except AttributeError:
                self.gtkmenu=[new_gtkmenu]

            gtklogger.set_submenu(new_gtkitem, new_gtkmenu)
            for item in self.items:
                item.construct_gui(self, new_gtkmenu, accelgroup) # recursive!
        else:                               # no submenu, create command
            gtklogger.connect(new_gtkitem, 'activate', MenuCallBackWrapper(self))
            if self.accel is not None and accelgroup is not None:
                new_gtkitem.add_accelerator('activate', accelgroup,
                                            ord(self.accel),
                                            gtk.gdk.CONTROL_MASK,
                                            gtk.ACCEL_VISIBLE)

        if not self.enabled():
            new_gtkitem.set_sensitive(0)

OOFMenuItem.construct_gui = _OOFMenuItem_construct_gui


# Destroys all the GUI objects associated with a menu item.
def _OOFMenuItem_destroy_gui(self):
    mainthread.runBlock(self.destroy_gui_thread)

def _OOFMenuItem_destroy_gui_thread(self):
    debug.mainthreadTest()
    if hasattr(self, 'gtkitem'):
        # Iterate over a copy, because destroy() triggers callbacks
        # which modify the list.
        for i in self.gtkitem[:]:
            i.destroy()
    if self.items and hasattr(self, 'gtkmenu'):
        # Copies again, for the same reason as above.
        for m in self.gtkmenu[:]:
            m.destroy()
        for item in self.items:
            item.destroy_gui_thread()
                
OOFMenuItem.destroy_gui = _OOFMenuItem_destroy_gui
OOFMenuItem.destroy_gui_thread = _OOFMenuItem_destroy_gui_thread

# GTK callbacks to clean up the object lists when GUIs are removed.
def _OOFMenuItem_gtkmenu_destroyed(self, gtkmenu):
    debug.mainthreadTest()
    self.gtkmenu.remove(gtkmenu)

OOFMenuItem.gtkmenu_destroyed = _OOFMenuItem_gtkmenu_destroyed

def _OOFMenuItem_gtkitem_destroyed(self, gtkitem):
    debug.mainthreadTest()
    i = self.gtkitem.index(gtkitem)
    del self.gtkitem[i]
    ## TODO 3.1: This is ugly.  Use a virtual function instead.
    if hasattr(self, 'handlerid'):
        del self.handlerid[i]
    
OOFMenuItem.gtkitem_destroyed = _OOFMenuItem_gtkitem_destroyed
    

########################

_oldAddItem = OOFMenuItem.addItem

def _newAddItem(self, item):
    return mainthread.runBlock(self.addItem_thread, (item,))
def _addItem_thread(self, item):
    debug.mainthreadTest()
    _oldAddItem(self, item)
    # Check to see if the gui has been constructed yet. The gui
    # objects for the root of the menu have gtkmenu attributes, but
    # not gtkitem attributes.  Other nodes of the tree have gtkitem,
    # but may not have gtkmenu, so it's necessary to check for both.
    if (hasattr(self, 'gtkitem') or hasattr(self, 'gtkmenu')) and \
       self.children_visible():
        # We've been guied, so gui the new children, if they're visible.
        if not hasattr(self, 'gtkmenu'):
            # Make a gtkmenu for each gtkitem.
            self.gtkmenu = [gtk.Menu() for i in range(len(self.gtkitem))]
            for (i,m) in zip(self.gtkitem, self.gtkmenu):
                gtklogger.set_submenu(i, m)
            for m in self.gtkmenu:
                m.connect("destroy", self.gtkmenu_destroyed)
            
        # At this point, we ourselves are guaranteed both gtkitem and gtkmenu.
        # Build a GUI object for each menu.
        for m in self.gtkmenu:
            item.construct_gui(self, m, item.getOption('accelgroup'))

    # If the parent menu had been desensitized because it had been
    # empty, it has to be sensitized now.
    self.enable_parent_gui()
    
    try:
        map(lambda x: x.show_all(), self.gtkmenu)
    except AttributeError:
        pass
    try:
        map(lambda x: x.show_all(), self.gtkitem)
    except AttributeError:
        pass
    return item

OOFMenuItem.addItem = _newAddItem
OOFMenuItem.addItem_thread = _addItem_thread

_oldRemoveItem = OOFMenuItem.removeItem

def _newRemoveItem(self, name):
    item = self.getItem(name)
    item.destroy_gui()
    _oldRemoveItem(self, name)
    if not self.items:    # desensitize self if it has no more items
        self.sensitize_gui(0)

OOFMenuItem.removeItem = _newRemoveItem
        

########################

class CheckMenuCallBackWrapper(MenuCallBackWrapper):
    def __call__(self, gtkmenuitem, *args):
        return self.menuitem(gtkmenuitem.active)

def _CheckOOFMenuItem_construct_gui(self, base, parent_menu, accelgroup):
    debug.mainthreadTest()
    new_gtkitem = gtk.CheckMenuItem()
    new_gtkitem.add(self.gtklabel(new_gtkitem))
    gtklogger.setWidgetName(new_gtkitem, self.name)

    try:
        self.gtkitem.append(new_gtkitem)
    except AttributeError:
        self.gtkitem = [new_gtkitem]
    new_gtkitem.connect("destroy", self.gtkitem_destroyed)
    # Set the state of the button.  This calls the callback, so we do
    # it here before the callback is connected.
    new_gtkitem.set_active(self.value)
    if self.accel is not None and accelgroup is not None:
        new_gtkitem.add_accelerator('activate', accelgroup,
                                     ord(self.accel),
                                     gtk.gdk.MOD1_MASK, gtk.ACCEL_VISIBLE)

    # Handler IDs are added in the same order as items, so there
    # is item-for-item correspondence of the lists.
    new_handler = gtklogger.connect(new_gtkitem, 'activate',
                                    CheckMenuCallBackWrapper(self))
    try:
        self.handlerid.append(new_handler)
    except AttributeError:
        self.handlerid = [new_handler]

    if not self.enabled():
        new_gtkitem.set_sensitive(0)

    parent_menu.insert(new_gtkitem, self.gui_order())

CheckOOFMenuItem.construct_gui = _CheckOOFMenuItem_construct_gui

# Redefine the CheckOOFMenuItem __call__ method so that commands
# executed from scripts will set the radio buttons in the GUI
# correctly. 
_old_CheckOOFMenuItem___call__ = CheckOOFMenuItem.__call__

def _CheckOOFMenuItem___call__(self, active):
    _old_CheckOOFMenuItem___call__(self, active)
    # Before calling set_active(), it's necessary to disable the gtk
    # callback mechanism for the button, so that set_active() won't
    # call the callback, which calls this function, which calls
    # set_active(), ad infinitum.
    try:
        gtkitem = self.gtkitem
    except AttributeError:
        pass
    else:
        mainthread.runBlock(_setactive, (gtkitem, self.handlerid, active))
        

def _setactive(gtkitem, handler, active):
    debug.mainthreadTest()
    for (i,h) in map(None, gtkitem, handler):
        h.block()
        i.set_active(active)
        h.unblock()

CheckOOFMenuItem.__call__ = _CheckOOFMenuItem___call__

#########################

class RadioMenuCallBackWrapper(CheckMenuCallBackWrapper):
    def __call__(self, gtkmenuitem, *args):
        debug.mainthreadTest()
        # Since the RadioOOFMenuItem takes care of calling the
        # callback for the item that's being turned off, here we only
        # call the callback if an item is being turned on.
        if gtkmenuitem.active:
            return self.menuitem()


def _RadioOOFMenuItem_construct_gui(self, base, parent_menu, accelgroup):
    debug.mainthreadTest()
    try:
        gtkgroup = self.group.gtk
    except AttributeError:
        new_gtkitem = gtk.RadioMenuItem(group=None)
        gtklogger.setWidgetName(new_gtkitem, self.name)
        self.group.gtk = [new_gtkitem]
    else:
        new_gtkitem = gtk.RadioMenuItem(group=gtkgroup[-1])
                                       
    new_gtkitem.add(self.gtklabel(new_gtkitem))
    # Set the state of the button.  This calls the callback, so we do
    # it here before the callback is connected.
    new_gtkitem.set_active(self.value)
    
    try:
        self.gtkitem.append(new_gtkitem)
    except AttributeError:
        self.gtkitem = [new_gtkitem]
    new_gtkitem.connect("destroy", self.gtkitem_destroyed)
        
    if self.accel is not None and accelgroup is not None:
        new_gtkitem.add_accelerator('activate', accelgroup,
                                     ord(self.accel),
                                     gtk.gdk.MOD1_MASK, gtk.ACCEL_VISIBLE)
        
    new_handlerid = gtklogger.connect(new_gtkitem, 'activate',
                                     RadioMenuCallBackWrapper(self))

    try:
        self.handlerid.append(new_handlerid)
    except AttributeError:
        self.handlerid = [new_handlerid]
    
    if self.getOption('disabled'):
        new_gtkitem.set_sensitive(0)
    parent_menu.add(new_gtkitem)

RadioOOFMenuItem.construct_gui = _RadioOOFMenuItem_construct_gui

# See comments above about redefining __call__ for CheckOOFMenuItem.

_old_RadioOOFMenuItem___call__ = RadioOOFMenuItem.__call__

def _RadioOOFMenuItem___call__(self):
    debug.mainthreadTest()
    _old_RadioOOFMenuItem___call__(self)
    mainthread.runBlock(_setactive, (self.gtkitem, self.handlerid, 1))


RadioOOFMenuItem.__call__ = _RadioOOFMenuItem___call__

###################################################

# Redefine 'enable' and 'disable' so that the menus are grayed out.

def _sensitize_gui(self, sensitive):
    mainthread.runBlock(self.sensitize_gui_thread, (sensitive,))

def _sensitize_gui_thread(self, sensitive):
    debug.mainthreadTest()
    try:
        itemlist = self.gtkitem
    except AttributeError:
        pass
    else:
        for i in itemlist:
            i.set_sensitive(sensitive)
OOFMenuItem.sensitize_gui = _sensitize_gui
OOFMenuItem.sensitize_gui_thread = _sensitize_gui_thread

_old_disable = OOFMenuItem.disable
def _OOFMenuItem_disable(self):
    mainthread.runBlock(self.disable_thread)
def disable_thread(self):
    debug.mainthreadTest()
    _old_disable(self)
    self.sensitize_gui(0)
OOFMenuItem.disable = _OOFMenuItem_disable
OOFMenuItem.disable_thread = disable_thread

def _enable_children(self):
    debug.mainthreadTest()
    if self.enabled():
        self.sensitize_gui(1)
        for item in self.items:
            item.enable_children()
OOFMenuItem.enable_children = _enable_children

def _enable_parent_gui(self):
    debug.mainthreadTest()
    if self.enabled():
        self.sensitize_gui(1)
    if self.parent is not None:
            self.parent.enable_parent_gui()
OOFMenuItem.enable_parent_gui = _enable_parent_gui

_old_enable = OOFMenuItem.enable
def _OOFMenuItem_enable(self):
    _old_enable(self)
    mainthread.runBlock(self.enable_children)
OOFMenuItem.enable = _OOFMenuItem_enable

# When a gui callback is added, an automatically disabled menu item
# might become enabled.
_old_add_gui_callback = OOFMenuItem.add_gui_callback
def _OOFMenuItem_add_gui_callback(self, callback):
    _old_add_gui_callback(self, callback)
    if self.enabled():
        self.sensitize_gui(1)
OOFMenuItem.add_gui_callback = _OOFMenuItem_add_gui_callback

####################################################

def _invokeGUICallback(self):
    self.gui_callback(self)

OOFMenuItem.invokeGUICallback = _invokeGUICallback
