# -*- python -*-
# $RCSfile: scriptloader.py,v $
# $Revision: 1.18.2.2 $
# $Author: fyc $
# $Date: 2014/07/17 15:38:04 $


# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# ScriptLoader is a derived class of InteractiveInterpreter that
# provides a correct traceback when exceptions occur while processing
# a Python file.  In addition, it provides a hook that can be
# redefined in a derived class to update a progress bar.

# The problem with InteractiveInterpreter is that when an exception is
# raised, the line numbers in the traceback are offsets into the
# current code block, and the current code block is not the file being
# processed.  It is instead just the set of lines passed to runsource
# since the last successful execution.  The traceback uses these
# erroneous line numbers to find the source code for the offending
# instructions.  The filename passed to runsource is only used in
# error messages and to find the source code.  The solution presented
# here is to pass a fake filename to runsource.  The fake name encodes
# the line number of the beginning of the code block.  Then when an
# exception occurs, the actual line numbers can be computed, and the
# traceback can be corrected.

# Because it's difficult to actually create and modify a traceback
# object, this code only creates a modified traceback list, as
# returned by traceback.extract_tb.  That means that the modified
# traceback can't be passed to sys.excepthook.  Instead we pass the
# traceback list to excepthook.displayTraceBack().

# Another problem with InteractiveInterpreter is that it doesn't work
# the way execfile() does -- it requires a blank line at the end of an
# indented block, unless the next line is an "else", "elif", or
# "except".  So here we use InteractiveInterpreter to process blocks
# of code, but use the compiler module to find those blocks.  That way
# we're guaranteed that we won't separate an "if" from its "else".
# This is somewhat of a hack, and it fails in some perverse cases.  In
# particular, it won't work if multiline statements are concatenated
# by a semi-colon, like this:
#   f(
#   ); g(
#   )
# This case is sufficiently perverse that we won't worry about it.

from ooflib.SWIG.common import ooferror
from ooflib.common import debug
from ooflib.common import excepthook
import code
import compiler
import sys
import traceback
import weakref

magicstring = 'O#O#F'           # used to construct fake file name
lenmagic = len(magicstring)
lenlenname = 4                  # number of digits used to encode
                                # length of real filename in the fake
                                # file name

_allLoaders = weakref.WeakValueDictionary()

############

# We use the compiler module to find the smallest blocks of code that
# can be passed to the interpreter.  compiler.parseFile() returns Node
# objects, which usually, but not always (esp. in Python 2.3), have
# their lineno set.  We need the line number so that we know which
# lines to interpret and which to report in tracebacks and syntax
# errors.  
## TODO OPT: perhaps this can be simplified since we don't support Python
## 2.3 anymore.

def _findLineNo(node):
    # Find the minimum line number of a node and all of its child
    # nodes in the AST, skipping any children without line numbers.
    kidlines = [lineno
                for lineno in [_findLineNo(n) for n in node.getChildNodes()]
                if lineno is not None]
    if not kidlines:
        return node.lineno
    minkidline = min(kidlines)
    if node.lineno is None:
        return minkidline
    return min([node.lineno, minkidline])

############

def encodeLocation(filename, lineno):
    return "%s%0*d%s%d" % (magicstring, lenlenname, len(filename), filename,
                          lineno)

def decodeLocation(location):
    if location.startswith(magicstring):
        namelen = int(location[lenmagic : lenmagic+lenlenname])
        filename = location[lenmagic+lenlenname : lenmagic+lenlenname+namelen]
        lineno = int(location[lenmagic+lenlenname+namelen:])
        return filename, lineno

def fixTraceBack(tback):
    tblist = traceback.extract_tb(tback)
    fixedtb = []
    for (filename, lineno, func, text) in tblist[1:]:
        if filename.startswith(magicstring):
            filename, baselineno = decodeLocation(filename)
            lineno += baselineno
            scriptloader = _allLoaders[filename]
            fixedtb.append((filename, lineno, func,
                            scriptloader.lines[lineno-1][:-1]))
        else:
            fixedtb.append((filename, lineno, func, text))
    return fixedtb

############

# Objects of the _ScriptExceptHook class are installed as
# sys.excepthook when loading a script.  For some reason, they're only
# invoked in non-threaded mode.  In threaded mode,
# ScriptLoader.showtraceback is used instead.

class _ScriptExceptHook(excepthook.OOFexceptHook):
    def __init__(self, scriptloader):
        self.scriptloader = scriptloader
    def __call__(self, e_type, e_value, tback):
        self.scriptloader.error = (e_type, e_value, fixTraceBack(tback))
        self.scriptloader.errhandler(*self.scriptloader.error)
        oldhook = excepthook.remove_excepthook(self)
    def getTraceBackList(self, tback):
        return fixTraceBack(tback)

############

class ScriptLoader(code.InteractiveInterpreter):
    def __init__(self, filename, locals=None, errhandler=None):
        self.filename = filename
        # If the open is going to fail, we want it to happen as early
        # as possible.
        self.fileobj = open(self.filename)

        _allLoaders[filename] = self
        code.InteractiveInterpreter.__init__(self, locals)

        # self.errhandler is set this way, and not via a default
        # argument, because excepthook.displayTraceBack may change
        # between class definition and instantiation.
        self.errhandler = errhandler or excepthook.displayTraceBack

        # Parse the file and find the python blocks.  We need to find
        # the blocks first, so that we don't accidentally execute an
        # "if" and strand its "else".
        try:
            modj = compiler.parseFile(self.filename)
        except SyntaxError:
            self.showsyntaxerror(self.filename)
            raise
        # modj is an AST.Module, modj.node is an AST.Stmt
        blocknodes = modj.node.nodes  # generic list of AST.Nodes
        # self.blocks is a list of line numbers where blocks start
        self.blocks = [_findLineNo(node) for node in blocknodes]

        self.error = None

            
    def run(self):
        if self.error is None:
            self.lines = self.fileobj.readlines()
            nlines = len(self.lines)
            nblocks = len(self.blocks)
            self.blocks.append(nlines+1)  # avoid special case for last block
            self.excepthook = excepthook.assign_excepthook(
                _ScriptExceptHook(self))
            # We can't use a try/finally here to restore an old excepthook
            # after we're done reading the file.  If an exception is
            # raised, the "finally" clause would run before the
            # excepthook.
            for blockno in range(nblocks):
                # line numbers start at 1, not 0
                blockstart = self.blocks[blockno] - 1
                blockend = self.blocks[blockno+1] - 1
                source = ''.join(self.lines[blockstart:blockend])
                more = self.runsource(source,
                                      encodeLocation(self.filename, blockstart))
                if more:
                    raise ooferror.ErrPyProgrammingError(
                        "Error reading script!")
                self.progress(blockend+1, nlines)
                if self.stop() or self.error:
                    break
            excepthook.remove_excepthook(self.excepthook)
        self.done()

    def showtraceback(self):
        self.error = (type, value, tb) = sys.exc_info()
        fixedtb = fixTraceBack(tb)
        self.errhandler(type, value, fixedtb) 

    def showsyntaxerror(self, filename):
        (etype, value, tb) = sys.exc_info()
        msg, (dummy_filename, lineno, offset, line) = value
        value = (msg, (self.filename, lineno, offset, line))
        self.error = (etype, value, None)
        raise etype, value, None

    def progress(self, current, total): # May be redefined in subclasses
        pass

    def stop(self):             # May be redefined in subclasses
        return False

    def done(self):             # May be redefined in subclasses
        self.fileobj.close()
