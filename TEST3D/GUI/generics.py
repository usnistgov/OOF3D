# -*- python -*-
# $RCSfile: generics.py,v $
# $Revision: 1.1.2.8 $
# $Author: langer $
# $Date: 2014/09/28 17:31:02 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

# Generic tests that can be inluded in GUI test scripts.  Most import
# statements are included in function bodies so that the first import
# is unlikely to come from this file, which might affect program
# behavior if the import has side effects.

from ooflib.common.IO.GUI import gtklogger
import file_utils
import os
import re
import string
import sys
import types

floatpattern = \
    re.compile("([-+]?(?:\d+(?:\.\d*)?|\d*\.\d+)(?:[eE][-+]?\d+)?)")
intpattern = re.compile("[0-9]+$")

# fp_string_compare compares two strings.  Any floating point numbers
# within the strings are compared numerically, using the given
# tolerance.  If the tolerance is None or 0, the strings are compared
# character-wise.

def fp_string_compare(str1, str2, tolerance):
    if not tolerance:
        return str1 == str2

    s1_items = floatpattern.split(str1)
    s2_items = floatpattern.split(str2)
    
    if len(s1_items) != len(s2_items):
        return False

    for s1, s2 in zip(s1_items, s2_items):
        if not fp_substring_compare(s1, s2, tolerance):
            return False
    return True

def fp_substring_compare(s1, s2, tolerance):
    if intpattern.match(s1) and intpattern.match(s2):
        if int(s1) != int(s2):
            print >> sys.stderr, "fp_substring_compare: int mismatch", \
                s1, s2
            return False
    elif floatpattern.match(s1) and floatpattern.match(s2):
        x1 = float(s1)
        x2 = float(s2)
        diff = abs(x1 - x2)
        reltol = min(abs(x1), abs(x2))*tolerance
        if diff > reltol or diff > tolerance:
            print >> sys.stderr, "fp_substring_compare: float mismatch", \
                s1, s2, "diff=%s" % diff
            return False
    else:
        if s1 != s2:
            print >> sys.stderr, \
                ("fp_substring_compare: string mismatch\n==>%s<==\n==>%s<=="
                 % (s1, s2))
            return False
    return True

# fp_string_compare_tail is just like fp_string_compare, but it
# doesn't use all of str1.  It checks to see if str2 appears at the
# end of str1.

def fp_string_compare_tail(str1, str2, tolerance):
    if not tolerance:
        return str1.endswith(str2)
    s1_items = floatpattern.split(str1)
    s2_items = floatpattern.split(str2)
    if len(s1_items) < len(s2_items):
        return False
    # The first items are treated separately, because the piece from
    # str2 only needs to match the end of the piece from str1 if it's
    # not a float.
    s1 = s1_items[-len(s2_items)]
    s2 = s2_items[0]
    if not (floatpattern.match(s1) and floatpattern.match(s2)):
        s1_items = s1_items[1-len(s2_items):]
        s2_items = s2_items[1:]
        if not s1.endswith(s2):
            print >> sys.stderr, ("fp_string_compare_tail: "
                                  "string mismatch\n==>%s<==\n==>%s<=="
                                  % (s1, s2))
            return False
    else:
        s1_items = s1_items[-len(s2_items):]

    for s1, s2 in zip(s1_items, s2_items):
        if not fp_substring_compare(s1, s2, tolerance):
            return False
    return True

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
    from ooflib.SWIG.common import guitop
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

def allWindowsLayersGridSizes(): #Only the selections state is important
    from ooflib.common.IO import gfxmanager
    from ooflib.common.IO import ghostgfxwindow
    windows = gfxmanager.gfxManager.getAllWindows()
    count = 0
    for window in windows:
        count = count + window.checkLayersGridsSizes()
    return count

def emptyGraphicsWindow(windowname):
    from ooflib.common.IO import gfxmanager
    gfxwindow = gfxmanager.gfxManager.getWindow(windowname)
    return not gfxwindow.drawable()

def treeViewLength(widgetpath):
    # Return the number of items in the given TreeView.
    treeview = gtklogger.findWidget(widgetpath)
    return len(treeview.get_model())

def treeViewColCheck(widgetpath, col, choices, tolerance=None):
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
    for i,x in enumerate(liststore):
        if choices[i] != None:
            if not fp_string_compare(x[col], choices[i], tolerance):
                print >> sys.stderr, x[col], '!=', choices[i]
                return False
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
        
def GraphicsListedLayersWhats(windowname):
    from ooflib.common.IO import gfxmanager
    from ooflib.common.IO import ghostgfxwindow
    window = gfxmanager.gfxManager.getWindow(windowname)
    whats = [x.who().name() for x in window.listedLayers()]
    return tuple(whats)

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

def chooserCheck(widgetpath, choices, tolerance=None):
    return treeViewColCheck(widgetpath, 0, choices, tolerance)

def chooserStateCheck(widgetpath, choice):
    # only for ChooserWidget, not ChooserListWidget.  Checks that the
    # currently selected item is 'choice'.
    combobox = gtklogger.findWidget(widgetpath)
    index = combobox.get_active()
    if index == -1:
        return choice is None
    model = combobox.get_model()
    return choice == model[index][0]


def chooserListStateCheck(widgetpath, choices, tolerance=None):
    # for ChooserListWidget and friends, including MultiListWidget.
    # Checks that everything in the list 'choices' is selected.
    treeview = gtklogger.findWidget(widgetpath)
    selection = treeview.get_selection()
    model, paths = selection.get_selected_rows()
    if len(paths) != len(choices):
        print >> sys.stderr, "Wrong number of selections:", len(paths), "!=", len(choices)
        return False
    for path in paths:          # loop over actually selected objects
        val = model[path][0]
        for choice in choices:
            if fp_string_compare(val, choice, tolerance):
                break
        else:
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
    return file_utils.fp_file_compare(filename, 
                                      os.path.join(testdir(), filename),
                                      tolerance=1.e-8,
                                      comment='#')


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
    if len(grp) != n:
        print >> sys.stderr, (
            "Size of pixel group '%s' is %d.  Expected %d." % 
            (grpname, len(grp), n))
        return False
    return True

def gtkTextCompare(widgetpath, targettext, tolerance=None):
    gtktxt = gtklogger.findWidget(widgetpath)
    if not gtktxt:
        print >> sys.stderr, "Text widget not found: %s." % widgetpath
        return False
    sourcetext = string.strip(gtktxt.get_text())
    if not fp_string_compare(sourcetext, targettext, tolerance):
        print >> sys.stderr, ("Text compare failed for path %s, >%s< != >%s<"
                              % (widgetpath, sourcetext, targettext))
        return False
    return True

# Compare the value of text representing the value of a floating point
# number.
## TODO MER: This is redundant, now that gtkTextCompare uses
## fp_string_compare.
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
# their target texts.  If tolerance is nonzero, floating point
# comparison is done on any numbers found in the strings.
def gtkMultiTextCompare(widgetdict, widgetbase=None, tolerance=None):
    for (wname, ttext) in widgetdict.items():
        if widgetbase:
            w = widgetbase + ":" + wname
        else:
            w = wname
        if not gtkTextCompare(w, ttext, tolerance):
            return False
    return True

## TODO MER: This is redundant, now that gtkMultiTextCompare uses
## fp_string_compare.
def gtkMultiFloatCompare(widgetdict, widgetbase=None, tolerance=1.e-6):
    for (wname, val) in widgetdict.items():
        if widgetbase:
            w = widgetbase + ":" + wname
        else:
            w = wname
        if not gtkFloatCompare(w, val, tolerance):
            return False
    return True

def gtkTextviewCompare(widgetpath, targettext, tolerance=None):
    widget = gtklogger.findWidget(widgetpath)
    msgbuffer = gtklogger.findWidget(widgetpath).get_buffer()
    text = msgbuffer.get_text(msgbuffer.get_start_iter(),
                              msgbuffer.get_end_iter())
    if not fp_string_compare(text, targettext, tolerance):
        print >> sys.stderr, ("Textview compare failed for %s, >%s<!=>%s<."
                              % (widgetpath, text, targettext))
        return False
    return True

def gtkTextviewTail(widgetpath, targettext, tolerance=None):
    msgbuffer = gtklogger.findWidget(widgetpath).get_buffer()
    text = msgbuffer.get_text(msgbuffer.get_start_iter(),
                              msgbuffer.get_end_iter())
    if not fp_string_compare_tail(text, targettext, tolerance):
        print >> sys.stderr, (("gtkTextviewTail failed for %s\n"
                               "expected =>%s<=\ngot =>%s<=")
                              % (widgetpath, targettext, text))
        return False
    return True

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

def syntaxErrorMsg(text):
    # The syntax error message format changed slightly from Python 2.5
    # to 2.6.  Grrr.  The syntax format in the argument should be the
    # *2.6* version.
    text25 = "single-quoted string"
    text26 = "string literal"
    if sys.version_info[1] <= 5:
        return errorMsg(text.replace(text26, text25))
    return errorMsg(text)
    

def msgTextTail(text):
    return gtkTextviewTail('OOF3D Messages 1:Text', text+'\n')

###################

# Memory leak checker checks for the presence of allocated and
# inventoried C++ objects.

from ooflib.SWIG.common import cmicrostructure
from ooflib.SWIG.engine import cskeleton2, femesh
def objectInventory(microstructures=0, nodes=0, elements=0, meshes=0):
    counts = (cmicrostructure.get_globalMicrostructureCount(),
              cskeleton2.get_globalNodeCount(),
              cskeleton2.get_globalElementCount(),
              femesh.get_globalFEMeshCount())
    expected = (microstructures, nodes, elements, meshes)
    if counts != expected:
        print >> sys.stderr, \
            "objectInventory failed. Expected (micro, nodes, elems, meshes) =",\
            expected, "Got", counts
    return counts == expected
