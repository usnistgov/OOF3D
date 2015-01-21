# -*- python -*-
# $RCSfile: skeletondiff.py,v $
# $Revision: 1.5.18.1 $
# $Author: langer $
# $Date: 2013/11/08 20:44:49 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

# A container class to record "before"/"after" state of a skeleton
# subjected to a series of NodeMove operations.
class SkeletonDiff:
    def __init__(self):
        self.changes = {}
    def addChanges(self, node, before, after):
        if node in self.changes:
            self.changes[node][1] = after
        else:
            self.changes[node] = [before, after]
    def undoChanges(self):
        for node in self.changes:
            node.moveTo(self.changes[node][0])
    def redoChanges(self):
        for node in self.changes:
            node.moveTo(self.changes[node][1])

# A utility class for book-keeping a series of NodeMoves for a skeleton
class NodeMoveHistory:
    def __init__(self):
        self._data = []
        self.ndata = 0
        self.current = -1
        self.skeldiff = None
    def undo(self):
        self._data[self.current].undoChanges()
        self.current -= 1
    def redo(self):
        self.current += 1
        self._data[self.current].redoChanges()
    def undoable(self):
        return self.current>=0
    def redoable(self):
        return  self.ndata>(self.current+1)
    def update(self, node, before, after):
        if not self.skeldiff:
            self.skeldiff = SkeletonDiff()
        self.skeldiff.addChanges(node, before, after)
    def finish(self):
        self.append()
        self.skeldiff = None
    def append(self):
        if self.ndata!=(self.current+1):
            del self._data[(self.current+1):]
        self._data.append(self.skeldiff)
        self.ndata = len(self._data)
        self.current += 1
