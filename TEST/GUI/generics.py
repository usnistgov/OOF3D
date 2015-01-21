# -*- python -*-
# $RCSfile: generics.py,v $
# $Revision: 1.46.12.1 $
# $Author: fyc $
# $Date: 2013/07/08 17:51:11 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov.

# Generic tests that can be inluded in GUI test scripts.  Most import
# statements are included in function bodies so that the first import
# is unlikely to come from this file, which might affect program
# behavior if the import has side effects.

from ooflib.common.IO.GUI import gtklogger
import filecmp
import os
import sys
import string

checkpoint_count = gtklogger.checkpoint_count

def testdir():
    # guitests.py sets OOFTESTDIR before running each test.  It's the
    # directory containing the log file and reference data files for
    # the test.
    return os.getenv('OOFTESTDIR')

def removefile(filename):
    if os.path.exists(filename):
        os.remove(filename)

def mainPageCheck(name):
    from ooflib.common import guitop
    return guitop.top().currentPageName == name 

def whoNameCheck(whoclass, names):
    from ooflib.common.IO import whoville
    classmembers = whoville.getClass(whoclass).actualMembers()
    if len(classmembers) != len(names):
        return False
    for whoobj in classmembers:
        if whoobj.name() not in names:
            return False
    return True

def gfxWindowCheck(names):
    from ooflib.common.IO import gfxmanager
    windows = gfxmanager.gfxManager.getAllWindows()
    if len(names) != len(windows):
        return False
    for window in windows:
        if window.name not in names:
            return False
    return True

def emptyGraphicsWindow(windowname):
    from ooflib.common.IO import gfxmanager
    gfxwindow = gfxmanager.gfxManager.getWindow(windowname)
    return not gfxwindow.drawable()

def treeViewLength(widgetpath):
    # Return the number of items in the given TreeView.
    treeview = gtklogger.findWidget(widgetpath)
    return len(treeview.get_model())

def treeViewColCheck(widgetpath, col, choices):
    # Check that the contents of the given column of a TreeView match
    # the given list of choices.  'widgetpath' is the gtklogger path
    # to the gtk TreeView.  'col' is actually a TreeStore or ListStore
    # column number.
    treeview = gtklogger.findWidget(widgetpath)
    liststore = treeview.get_model()
    if len(liststore) != len(choices):
        print >> sys.stderr, "length mismatch: %d!=%d" % (len(liststore),
                                                          len(choices))
        return False
    i = 0
    for x in iter(liststore):           # returns a TreeModelRow object
        if choices[i]!= None and x[col] != choices[i]:
            print >> sys.stderr, x[col], '!=', choices[i]
            return False
        i += 1
    return True

def treeViewColValues(widgetpath, col):
    treeview = gtklogger.findWidget(widgetpath)
    liststore = treeview.get_model()
    return [x[col] for  x in iter(liststore)]

def treeViewSelectCheck(widgetpath, col):
    # Returns the contents of the given column of a TreeStore in the
    # selected row of the given TreeView.
    treeview = gtklogger.findWidget(widgetpath)
    selection = treeview.get_selection()
    model, iter = selection.get_selected()
    if iter is not None:
        return model[iter][col]
        
def treeViewSizeCheck(widgetpath):
    # Returns the contents of the given column of a TreeStore in the
    # selected row of the given TreeView.
    treeview = gtklogger.findWidget(widgetpath)
    selection = treeview.get_selection()
    return selection.count_selected_rows() + 1

def listViewSelectedRowNo(widgetpath):
    # widgetpath must be a TreeView displaying a ListStore.  Returns
    # the index of the selected row, or None if nothing is selected.
    treeview = gtklogger.findWidget(widgetpath)
    selection = treeview.get_selection()
    model, iter = selection.get_selected()
    if iter is not None:
        return model.get_path(iter)[0]
    return None                         # nothing selected

def chooserCheck(widgetpath, choices):
    return treeViewColCheck(widgetpath, 0, choices)

def chooserStateCheck(widgetpath, choice):
    # only for ChooserWidget, not ChooserListWidget.  Checks that the
    # currently selected item is 'choice'.
    combobox = gtklogger.findWidget(widgetpath)
    index = combobox.get_active()
    if index == -1:
        return choice is None
    model = combobox.get_model()
    return choice == model[index][0]


def chooserListStateCheck(widgetpath, choices):
    # for ChooserListWidget and friends, including MultiListWidget.
    # Checks that everything in the list 'choices' is selected.
    treeview = gtklogger.findWidget(widgetpath)
    selection = treeview.get_selection()
    model, paths = selection.get_selected_rows()
    if len(paths) != len(choices):
        print >> sys.stderr, "Wrong number of selections:", len(paths), "!=", len(choices)
        return False
    for path in paths:
        val = model[path][0]
        if val not in choices:
            print >> sys.stderr, "Expected:", choices
            print >> sys.stderr, "     Got:", [model[p][0] for p in paths]
            return False
    return True

def chooserListStateCheckN(widgetpath, choices):
    # Just like chooserListStateCheck, but choices is a list of integers
    treeview = gtklogger.findWidget(widgetpath)
    selection = treeview.get_selection()
    model, paths = selection.get_selected_rows()
    if len(paths) != len(choices):
        print >> sys.stderr, "Wrong number of selections:", len(paths), "!=", len(choices)
        return False
    selected = [p[0] for p in paths]
    if selected == choices:
        return True
    print >> sys.stderr, "Selected rows are", selected
    return False


def is_sensitive(widgetpath):
    return _widget_sensitive(gtklogger.findWidget(widgetpath))

def menuSensitive(menu, item):
    topmenuwidget = gtklogger.findWidget(menu)
    if not topmenuwidget:
        print >> sys.stderr, "Didn't find widget for", menu
    menuitemwidget = gtklogger.findMenu(topmenuwidget, item)
    if not menuitemwidget:
        print >> sys.stderr, "Didn't find widget for %s:%s" % (menu, item)
    return _widget_sensitive(menuitemwidget)

def _widget_sensitive(widget):
    if not widget.get_property('sensitive'):
        return 0
    parent = widget.get_parent()
    while parent:
        if not parent.get_property('sensitive'):
            return 0
        parent = parent.get_parent()
    return 1

def sensitizationCheck(wdict, base=None):
    # Check widget sensitization.  wdict is a dictionary whose keys
    # are the gtklogger paths to widgets and whose values are 0 or 1,
    # indicating whether (1) or not (0) the widget is sensitive.  If
    # provided, base is prepended to each widget path.
    for wname, sense in wdict.items():
        if base:
            path = base + ':' + wname
        else:
            path = wname
        if is_sensitive(path) != sense:
            print >> sys.stderr, "Sensitization test failed for", path
            return False
    return True

def filediff(filename):
    return filecmp.cmp(filename, os.path.join(testdir(), filename))

# Assumes that every line in the files to be compared is either a
# comment, or a separator-separated list of float-ables, or identical
# strings.  If there are fields which cannot be converted to floats,
# they're checked for identicalness, and if they pass, the test just
# continues.
def floatFileDiff(filename, tolerance=1.0e-8, comment="#", separator=","):
    class FloatFileDiffFailure:
        def __init__(self, message):
            self.message = message
    reference = file(os.path.join(testdir(),filename))
    local = file(filename)
    try:
        try: # Again.
            for refline in reference:
                localline = local.next()
                if refline[0]==comment:
                    continue
                refitems = string.split(refline,separator)
                localitems = string.split(localline,separator)
                for(i1,i2) in zip(refitems, localitems):
                    try:
                        (f1, f2) = (float(i1), float(i2))
                    except ValueError:
                        if i1!=i2:
                            raise FloatFileDiffFailure(
                                "Text mismatch, >%s< != >%s<" % (i1,i2))
                    else:
                        if abs(f1-f2)>tolerance:
                            raise FloatFileDiffFailure(
                                "%f too far from %f" % (f1,f2))
                        if f1!=0.0 and f2!=0.0 and abs((f1/f2)-1.0)>tolerance:
                            raise FloatFileDiffFailure(
                                "%f/%f too far from 1.0" % (f1,f2))

        except FloatFileDiffFailure, f:
            print >> sys.stderr, "floatFileDiff failure, ", f.message
            return False
        except StopIteration: # Raised by local.next() if EOF is encountered.
            print >> sys.stderr, "floatFileDiff: File size mismatch."
            return False
        else:
            return True
    finally:
        reference.close()
        local.close()
        
    
def skeletonNodeSelectionCheck(skeleton, nodelist):
    from ooflib.common.IO import whoville
    sc = whoville.getClass('Skeleton')[skeleton]
    nodes = sc.nodeselection.retrieve()
    nodeindices = [node.index for node in nodes]
    nodeindices.sort()
    nodelist.sort()
    ok = (nodeindices == nodelist)
    if not ok:
        print >> sys.stderr, nodeindices
    return ok

def skeletonElementSelectionCheck(skeleton, elemlist):
    from ooflib.common.IO import whoville
    sc = whoville.getClass('Skeleton')[skeleton]
    elems = sc.elementselection.retrieve()
    elemindices = [el.index for el in elems]
    elemindices.sort()
    elemlist.sort()
    ok = (elemindices == elemlist)
    if not ok:
        print >> sys.stderr, elemindices
    return ok

def skeletonSegmentSelectionCheck(skeleton, seglist):
    from ooflib.common.IO import whoville
    sc = whoville.getClass('Skeleton')[skeleton]
    segs = sc.segmentselection.retrieve()
    nodepairs = [[n.index for n in seg.nodes()] for seg in segs]
    nodepairs.sort()
    seglist.sort()
    ok = nodepairs == seglist
    if not ok:
        print >> sys.stderr, nodepairs
    return ok

def skeletonSelectionTBSizeCheck(windowname, category, n):
    # Check that the right size is displayed in the Skeleton Selection
    # toolbox. 'category' must be "Element", "Node", or "Segment".
    text = gtklogger.findWidget(
        '%s:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:%s:size' %
        (windowname, category))
    return eval(text.get_text()) == n

def pixelSelectionTBSizeCheck(windowname, minpxls, maxpxls=None):
    # Check that the pixel selection size is displayed correctly in
    # the graphics window.  Since different versions of ImageMagick
    # can cause pixel selection operations to work differently after
    # image modifications, it's possible to specify a range of pixel
    # counts for this test.
    text = gtklogger.findWidget(
        '%s:Pane0:Pane1:Pane2:TBScroll:Pixel Selection:size' % windowname)
    n = eval(text.get_text())
    if maxpxls is None:
        return n == minpxls
    else:
        return minpxls <= n <= maxpxls

def pixelSelectionSizeCheck(msname, n):
    from ooflib.common.IO import whoville
    ms = whoville.getClass('Microstructure')[msname].getObject()
    return ms.pixelselection.size() == n


def pixelGroupSizeCheck(msname, grpname, n):
    from ooflib.common.IO import whoville
    ms = whoville.getClass('Microstructure')[msname].getObject()
    grp = ms.findGroup(grpname)
    return len(grp) == n

def gtkTextCompare(widgetpath, targettext):
    gtktxt = gtklogger.findWidget(widgetpath)
    if not gtktxt:
        print >> sys.stderr, "Text widget not found: %s." % widgetpath
        return False
    sourcetext = string.strip(gtktxt.get_text())
    if sourcetext != targettext:
        print >> sys.stderr, ("Text compare failed for path %s, >%s< != >%s<"
                              % (widgetpath, sourcetext, targettext))
        return False
    return True

# Compare the value of text representing the value of a floating point number.
def gtkFloatCompare(widgetpath, targetval, tolerance=1.e-6):
    gtktxt = gtklogger.findWidget(widgetpath)
    if not gtktxt:
        print >> sys.stderr, "Text widget not found: %s." % widgetpath
        return False
    sourceval = float(gtktxt.get_text())
    if abs(sourceval - targetval) > tolerance:
        print >> sys.stderr, ("Floating point comparison failed for %s, %g!=%g"
                              % (widgetpath, sourceval, targetval))
        return False
    return True

# Similar to the sensitizationCheck, takes a dictionary of widgets and
# their target texts.
def gtkMultiTextCompare(widgetdict, widgetbase=None):
    for (wname, ttext) in widgetdict.items():
        if widgetbase:
            w = widgetbase + ":" + wname
        else:
            w = wname
        if not gtkTextCompare(w, ttext):
            return False
    return True

def gtkMultiFloatCompare(widgetdict, widgetbase=None, tolerance=1.e-6):
    for (wname, val) in widgetdict.items():
        if widgetbase:
            w = widgetbase + ":" + wname
        else:
            w = wname
        if not gtkFloatCompare(w, val, tolerance):
            return False
    return True

def gtkTextviewCompare(widgetpath, targettext):
    widget = gtklogger.findWidget(widgetpath)
    msgbuffer = gtklogger.findWidget(widgetpath).get_buffer()
    text = msgbuffer.get_text(msgbuffer.get_start_iter(),
                              msgbuffer.get_end_iter())
    if text!=targettext:
        print >> sys.stderr, ("Textview compare failed for %s, >%s<!=>%s<."
                              % (widgetpath, text, targettext))
        return False
    return True
    

def gtkTextviewTail(widgetpath, targettext):
    msgbuffer = gtklogger.findWidget(widgetpath).get_buffer()
    text = msgbuffer.get_text(msgbuffer.get_start_iter(),
                              msgbuffer.get_end_iter())
    ok = text.endswith(targettext)
    if not ok:
        print >> sys.stderr, \
              ("gtkTextviewTail failed for %s: text =>%s< doesn't end with >%s<"
               % (widgetpath, text, targettext))
    return ok

def gtkTextviewHead(widgetpath, targettext):
    msgbuffer = gtklogger.findWidget(widgetpath).get_buffer()
    text = msgbuffer.get_text(msgbuffer.get_start_iter(),
                              msgbuffer.get_end_iter())
    ok = text.startswith(targettext)
    if not ok:
        print >> sys.stderr, \
          ("gtkTextviewHead failed for %s: text =>%s< doesn't start with >%s<"
           % (widgetpath, text, targettext))
    return ok

def gtkTextviewGetLines(widgetpath):
    msgbuffer = gtklogger.findWidget(widgetpath).get_buffer()
    text = msgbuffer.get_text(msgbuffer.get_start_iter(),
                              msgbuffer.get_end_iter()).split('\n')
    return text
    
def gtkTextviewGetLine(widgetpath, line):
    return gtkTextviewGetLines(widgetpath)[line]

def gtkTextviewLine(widgetpath, line, targettext):
    if gtkTextviewGetLine(widgetpath, line) != targettext:
        print >> sys.stderr, ("gtkTextviewLine failed for %s: text=  >%s<!=>%s<"
                              % (widgetpath, text, targettext))
        return False
    return True

def errorMsg(text):
    return gtkTextviewTail('Error:ErrorScroll:ErrorText', text+'\n')

def msgTextTail(text):
    return gtkTextviewTail('OOF3D Messages 1:Text', text+'\n')

###################

# Memory leak checker checks for the presence of allocated and
# inventoried C++ objects.

from ooflib.SWIG.common import cmicrostructure
from ooflib.SWIG.engine import cskeleton2, femesh
def objectInventory(microstructures=0, nodes=0, elements=0, meshes=0):
    counts = (cmicrostructure.get_globalMicrostructureCount(),
              cskeleton.get_globalNodeCount(),
              cskeleton.get_globalElementCount(),
              femesh.get_globalFEMeshCount())
    expected = (microstructures, nodes, elements, meshes)
    if counts != expected:
        print >> sys.stderr, \
            "objectInventory failed. Expected (micro, nodes, elems, meshes) =",\
            expected, "Got", counts
    return counts == expected
