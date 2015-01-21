# -*- python -*-
# $RCSfile: output.py,v $
# $Revision: 1.21.4.14 $
# $Author: langer $
# $Date: 2014/11/05 16:54:37 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config

from ooflib.SWIG.common import coord
from ooflib.SWIG.common import ooferror
from ooflib.SWIG.engine import outputval
from ooflib.common import debug
from ooflib.common import enum
from ooflib.common import primitives
from ooflib.common import utils
from ooflib.common.IO import parameter
from ooflib.common.IO import xmlmenudump
import itertools
import string
import struct
import types

structIntFmt = '>i'
structIntSize = struct.calcsize(structIntFmt)

## The Output class is used when computing output quantities on a
## mesh, such as for a contour plot.  Each Output instance performs a
## simple operation on a set of inputs.  Outputs may be chained
## together to perform more complicated operations.  The idea is that
## eventually users will be able to construct new Output operations at
## run-time by assembling predefined Outputs into new Output chains.

## TODO OPT: Use iterables instead of lists, maybe.  Do NOT use
## generators or iterators, unless it's guaranteed that they won't
## have to be interated over more than once.

class Output(object):
    def __init__(self, name, otype, callback, inputs=[], params=[],
                 tip=parameter.emptyTipString,
                 discussion=parameter.emptyTipString,
                 srepr=None,
                 instancefn=None, column_names=None,
                 bulk_only=False, surface_only=False,
                 parent=None):
        # otype is the type of the output.

        # inputs is a list of Parameters specifying the names and
        # types of the inputs to this Output.

        # params is a list of Parameters governing the behavior of
        # this Output.

        # callback is a function or other callable object (see
        # engine/IO/outputClones.py).  The arguments to the callback
        # are (mesh, elements, coords) plus anything specified by the
        # Output constructor's inputs and params arguments.  Those
        # extra arguments are passed as keyword arguments, with the
        # keyword determined by the input or param's 'name'.

        # The 'elements' argument to the callback is a list of the
        # Elements that the Output is being evaluated in.  The
        # 'coords' argument is a list of lists of Coords.  coords[i]
        # is a list of MasterCoords within the Element elements[i].
        # The Output must be evaluated at these positions.
        
        # callback arguments corresponding to items in the 'params'
        # list are simple values, whose type is determined by the
        # param's Parameter type.

        # callback arguments corresponding to items in the 'inputs'
        # list are lists of values, whose type is determined by the
        # input's Parameter type.  There's one entry in the list for
        # each coord in the 'coords' list.  The input list is a flat
        # list, for now.  This may change.

        # srepr is a function to be used as the shortrepr for the
        # Output.  srepr takes a single argument, self, and returns a
        # string.  It should use findParam, resolveAlias, and
        # findInput as necessary and evaluate their shortreprs.

        # column_names is a function that returns a list of the names
        # of the output columns.  If it's None, the parent's column
        # names function will be used.

        self.name = name
        self.callback = callback
        self.tip = tip
        self.discussion = discussion
        self.parent = parent
        self.prototype = (parent is None)
        self.bulk_only = bulk_only
        self.surface_only = surface_only

        if srepr is not None:
            self.srepr = srepr      # short repr

        # 'instancefn' is a function that returns an instance of the
        # OutputVal subclass that this Output will produce.  If it's
        # None, then self.instancefn won't be defined, and the
        # Output's parent's 'instancefn' method will be used.
        if instancefn is not None:
            self.instancefn = instancefn
        # Same for column_names, which returns a list of names of the
        # columns in the output.
        if column_names is not None:
            self.column_names = column_names

        # Check that all names in iparms and params are unique.
        names = set()
        for p in params:
            p.set_data("Output", self)
            if p.name in names:
                raise KeyError("Parameter name '%s' is not unique" % p.name)
            names.add(p.name)
        for p in inputs:
            if p.name in names: 
                raise KeyError("Input name '%s' is not unique" % p.name)
            names.add(p.name)
        del names
        
        # self.params and self.iparms are OrderedDicts so that the
        # parameters will appear in the UI in the same order in which
        # they were specified in the params list.  Both are
        # dictionaries of Parameters keyed by name.
        self.params = utils.OrderedDict()
        for p in params:          
            self.params[p.name] = p
        self.iparms = utils.OrderedDict()
        for i in inputs:                
            self.iparms[i.name] = i

        # TODO 3.1: This is a hack that will have to be cleaned up.  Most
        # Outputs have an otype that is a single class (most commonly
        # OutputValPtr).  Some used to be PositionOutputs and have an
        # otype that's a tuple, (Point, Coord).  When Outputs are
        # connected to one another, the parameter.TypeChecker
        # mechanism is used.  When Outputs are used in analyze.py, it
        # only checks the class. For now, TypeChecker has been changed
        # so that it works correctly on a single class.  The correct
        # solution is for Outputs not to use TypeChecker at all,
        # maybe.
        ## TODO 3.1: What does the elimination of PositionOutputs mean for
        ## the preceding remark?
        self.otype = otype
        if isinstance(otype, parameter.TypeChecker):
            self.otype = otype
        elif isinstance(otype, (types.ListType, types.TupleType)):
            self.otype = parameter.TypeChecker(*otype)
        else:
            self.otype = otype

        # Dictionary of other Outputs that are connected to us
        self.inputs = utils.OrderedDict() # keyed by name

        # Dictionaries of aliases for parameters
        self.aliases = {}               # key = param, value = alias
        self.sesaila = {}               # key = alias, value = param

    def getPrototype(self):
        if self.prototype:
            return self
        return self.parent.getPrototype()

    # Make a copy of ourself, optionally giving values to parameters.
    def clone(self, name=None, params={}, srepr=None,
              column_names=None,
              tip=None, discussion=None):
        # First clone without copying aliases
        bozo = self._clone(name=name, srepr=srepr, 
                           column_names=column_names,
                           tip=tip, discussion=discussion)
        # Copy the aliases only once, so they're all in the top level dict.
        bozo.copyAliases(self)   
        # The params dict may use aliases, so assign values only after
        # the aliases have been copied.
        for pname, pvalue in params.items():
            bozo.resolveAlias(pname).value = pvalue
        return bozo

    # Clone without copying aliases.  Used by Output.clone()
    def _clone(self, name=None, srepr=None,
               column_names=None,
               tip=None, discussion=None):
        bozo = Output(name=name or self.name,
                      otype=self.otype,
                      callback=self.callback,
                      inputs=[i.clone() for i in self.iparms.values()],
                      params=[p.clone() for p in self.params.values()],
                      bulk_only=self.bulk_only,
                      surface_only=self.surface_only,
                      tip=tip or self.tip,
                      discussion=discussion,
                      srepr=srepr,
                      column_names=column_names,
                      parent=self)
        for iname, inpt in self.inputs.items():
            bozo.connect(iname, inpt._clone())
        return bozo
    
    # Defining __getattr__ like this makes Output cloning look a bit
    # more like subclassing.
    def __getattr__(self, name):
        try:
            return getattr(self.parent, name)
        except AttributeError:
            raise AttributeError("Output %s has no attribute named '%s'"
                                 % (self.name, name))

        
    # Look for a parameter, without considering aliases.  path is a
    # colon separated string.
    def findParam(self, path):
        path = path.rsplit(':', 1) # separate path into "input : param"
        if len(path) == 2:
            return self.findInput(path[0]).findParam(path[1])
        # len(path) == 1
        try:
            return self.params[path[0]]
        except KeyError:
            raise KeyError("Output '%s' has no parameter named '%s'" %
                           (self.name, path[0]))

    def findInput(self, path):
        path = path.split(':', 1)
        if len(path) == 2:
            try:
                inp = self.inputs[path[0]]
            except KeyError:
                raise KeyError("Output '%s' has no input named '%s'" 
                               % (self.name, path[0]))
            return inp.findInput(path[1])
        # len(path) == 1
        try:
            return self.inputs[path[0]]
        except KeyError:
            raise KeyError("Output '%s' has no input named '%s'"
                           % (self.name, path[0]))

    def allInputs(self):
        inputs = []
        for inpt in self.inputs.values():
            inputs.append(inpt)
            inputs.extend(inpt.allInputs())
        return inputs

    def __repr__(self):
        return "getOutput(%s)" % self.defaultRepr() 
    def shortrepr(self, s=None):
        # The optional 's' argument lets the shortrepr be computed for
        # an object other than the one it's defined in.  See
        # SymmMatrix3PropertyOutputRegistration for an example.
        s = s or self
        if self.srepr:
            return self.srepr(s) # instance method! Needs extra 'self'.
        return self.defaultRepr()
    def defaultRepr(self):
        params = self.getSettableParams() # dictionary keyed by alias
        args = ["'%s'" % self.getPath()] + ['%s=%s' % (alias, `p.value`)
                                            for alias, p in params.items()]
        return string.join(args, ',')

    def outputInstance(self): 
        # outputInstance returns an instance of the OutputVal subclass
        # that this Output will produce when run.  It looks for an
        # instance method called 'instancefn' which must be defined in
        # this Output or one of its parents.  If instancefn is defined
        # as a class method, then the __getattr__ lookup used to
        # search the parents won't run!  (__getattr__ is only used
        # when normal attribute lookup fails.)  Don't define a default
        # instancefn in the class!
        return self.instancefn(self) # extra 'self' arg for instance method

    def columnNames(self):
        # See comment in outputInstance above.  columnNames and
        # column_names are analogous to outputInstance and instancefn,
        # except that here we have a default behavior if column_names
        # isn't defined in the Output or its parents.
        try:
            cnames = self.column_names
        except AttributeError:
            return self.outputInstance().label_list()
        return cnames(self)     # an instance method

    # Get the path to this Output in the OutputTrees.  This is the
    # external identifier for the Output.
    def getPath(self):
        proto = self.getPrototype()
        for tree in outputTrees:
            try:
                return tree.objpath(proto)
            except KeyError:
                pass
        return "<Unregistered Output>"

    def connect(self, iname, inpt):
        # Because inputs are cloned before they're connected, there's
        # no need to check for connection loops.  They can't occur.
        # Ridiculous inputs can be constructed, but there's no way to
        # generate an infinite loop.
        splitname = iname.split(':', 1)
        if len(splitname) > 1:
            # Connect to an existing input
            try:
                inp = self.inputs[splitname[0]]
            except KeyError:
                raise KeyError("Output '%s' has no input named '%s'"
                               % (self.name, splitname[0]))
            inp.connect(splitname[1], inpt)
        else:
            # Connect to self.  First check the type
            try:
                inp = self.iparms[splitname[0]]
            except KeyError:
                raise KeyError("Output '%s' has no input named '%s'"
                               % (self.name, splitname[0]))
            else:
                inp.checker(inpt.otype)
            # Check for bulk/surface compatibility.  Outputs that can
            # only be evaluated on surfaces can't serve as inputs for
            # outputs that can only be evaluated in the bulk.
            if inpt.isSurfaceOnly() and self.bulk_only:
                raise ooferr.ErrPyProgrammingError(
                    "Attempt to connect surface input to bulk output!")

            # Make the connection.
            self.inputs[splitname[0]] = inpt.clone()

            # connect() calls might not be in order! Make sure that
            # inputs stay in the right order.  They have to be ordered
            # correctly or listAllParameterPaths won't work properly.
            self.inputs.reorder(self.iparms.keys())

    def isSurfaceOnly(self):
        # An Output can be evaluated only on surfaces if it or any of
        # its inputs can be evaluated only on surfaces.
        if self.surface_only:
            return True
        for inpt in self.inputs.values():
            if inpt.isSurfaceOnly():
                return True
        return False

    # Return all parameter paths, as lists of lists of names ([input,
    # input, ..., parameter]), unaliased.
    def listAllParameterPaths(self, filter=lambda x: True):
        plist = [[n] for n,p in self.params.items() if filter(p)]
        for inputname, inpt in self.inputs.items():
            plist.extend([[inputname]+path
                          for path in inpt.listAllParameterPaths(filter)])
        return plist

    # Return all parameter names as colon separated paths, unaliased.
    def listAllParameterNames(self, filter=lambda x: True):
        return [string.join(path, ':')
                for path in self.listAllParameterPaths(filter)]

    # Return a dictionary of clones of the settable Parameters, keyed
    # by their aliases.
    def getSettableParams(self):
        # Get names of the settable parameters from the prototype
        def valueless(p): return p.value is None
        pnames = self.getPrototype().listAllParameterNames(valueless)

        # Using the names, make a dict of clones of our *own* parameters
        pdict = utils.OrderedDict()
        for name in pnames:
            param = self.findParam(name)
            try:
                alias = self.getAliasForParam(param)
            except KeyError:
                pdict[name] = param.clone()
            else:
                pdict[alias] = param.clone()
        return pdict

    # Get a hierarchical list of the names of the Parameters.  Only
    # Parameters for which philtre(p) is true will be included.
    def getParameterNameHierarchy(self, philtre):
        phier = []
        # Get parameters from inputs.  This *must* be done before
        # getting our own parameters, because the order of parameters
        # in the hierarchical list determines the order in which their
        # widgets are created, and often widgets higher in the
        # hierarchy need to find widgets farther down at construction
        # time.
        for inputname, inpt in self.inputs.items():
            ihier = inpt.getParameterNameHierarchy(philtre)
            if ihier:
                phier.extend(prependHierarchyName(inputname, ihier))
        # Get our own parameters
        plist = [n for n,p in self.params.items() if philtre(p)]
        if len(plist) == 1:
            phier.append(plist[0])
        elif len(plist) > 1:
            phier.append(plist)
        return phier
        
    # Create a hierarchical list of the parameters, using
    # their aliased names. This list is used to construct the GUI
    # (hence the aliased names) and the widget scopes (hence the
    # hierarchy).  If onlySettable is true, then only those Parameters
    # whose value is None in the prototype will be included.
    def listAllParametersHierarchically(self, onlySettable=True):
        if onlySettable:
            def philtre(x): return x.value is None
        else:
            def philtre(x): return True

        # Get the full names of all parameters meeting the criterion
        pnames = self.getPrototype().getParameterNameHierarchy(philtre)

        # Convert the list of names to a list of Parameters, using
        # aliased names and default values.
        phier = self.convertNameHierarchy(pnames)
        return phier

    # Utility function called by listAllParametersHierarchically().
    # Recursively converts a hierarchical list of Parameter names into
    # a hierarchical list of Parameters.
    def convertNameHierarchy(self, pnames):
        hier = []
        for p in pnames:
            if type(p) is types.ListType:
                hier.append(self.convertNameHierarchy(p))
            else:
                param = self.findParam(p)
                try:
                    param.name = self.getAliasForParam(param)
                except KeyError:
                    pass
                hier.append(param)
        return hier

    # Make an alias for an existing parameter.  Both paramname and
    # alias are colon separated strings.  Optionally set a default
    # value and tip.
    def aliasParam(self, paramname, alias, default=None, tip=None):
        param = self.resolveAlias(paramname)
        self.aliases[param] = alias
        self.sesaila[alias] = param
        if default is not None:
            param.default = default
        if tip is not None:
            param.tip = tip

    # Return a Parameter, given an alias as a colon separated string.
    def resolveAlias(self, alias):
        try:
            # First, see if we have this alias registered
            return self.sesaila[alias]
        except KeyError:
            # We don't know this alias.  Maybe it's an alias for one
            # of our inputs' parameters.
            splt = alias.split(':', 1)
            if len(splt) == 2:
                try:
                    return self.inputs[splt[0]].resolveAlias(splt[1])
                except KeyError:
                    pass
            # It's not an alias.  Perhaps it's an actual parameter
            # name!  findParam will raise a KeyError if it fails.
            return self.findParam(alias)

    # Return a colon separated string, given a full parameter name as
    # a colon separated string.
    def getAliasForName(self, paramname):
        return self.getAliasForParam(self.findParam(paramname))

    # Return a colon separated string, given a Parameter.  The
    # Parameter *must* be one of ours, not a clone.
    def getAliasForParam(self, param):
        try:
            # Do we have an alias for this parameter?
            return self.aliases[param]
        except KeyError:
            # No local alias. Is it one of our parameters?
            if param in self.params.values():
                raise KeyError         # It has no alias!
            # It's not one of our parameters. Look in each of our inputs.
            for inputname, inpt in self.inputs.items():
                try:
                    # If the parameter belongs to one of our inputs,
                    # our name for it is (input's name):(param's alias)
                    return string.join([inputname,
                                        inpt.getAliasForParam(param)], ':')
                except KeyError:
                    pass
            raise KeyError              # Not one of us.

    # Copy aliases from another Output.  All of the aliases are stored
    # in our top-level alias dictionary, even if they were defined in
    # the other Output's inputs.
    def copyAliases(self, other):
        for paramname in self.listAllParameterNames():
            try:
                self.aliasParam(paramname, other.getAliasForName(paramname))
            except KeyError:
                pass

    # Checks to see if all inputs and parameters are defined, and that
    # the inputs themselves are computable.
    def incomputable(self, mesh):
        for i in self.iparms:
            try:
                inp = self.inputs[i]
            except KeyError:
                return True
            else:
                if inp.incomputable(mesh):
                    return True
        for p in self.params.values():
            if p.incomputable(mesh):
                return True
        return False

    def evaluate(self, mesh, domain, elements, coords):
        # elements is a list (or other iterable container) of Elements
        # on which to evaluate the output.  coords is a list of lists
        # of MasterCoords, one list per each Element, at which to
        # evaluate the output.  The Elements may be either bulk or
        # surface elements.  Some outputs can only be evaluated on one
        # type of element, so this routine needs to convert from
        # surface to bulk if necessary (using information from the
        # domain to translate from one to the other).  It should never
        # be necessary to translate from bulk to surface.  The
        # translation is moderately expensive, so it's done before
        # calling the inputs' evaluation routines, which will reduce
        # but not eliminate redundancy.

        # Do any inputs or evaluatable parameters require bulk or
        # surface elements?
        bulk_required = self.bulk_only
        surf_required = self.surface_only
        for inpt in self.inputs.values():
            if inpt.bulk_only:
                bulk_required = True
            if inpt.surface_only:
                surf_required = True
        for param in self.params.values():
            if isinstance(param, OutputParameter):
                if param.value.bulk_only:
                    bulk_required = True
                if param.value.surface_only:
                    surf_required = True
        # What kind of elements did we get?  (Don't use elements[0] to
        # get the first element, because elements may be iterable but
        # not indexable.)
        elementdim = next(iter(elements)).dimension()

        if elementdim == 3:
            bulk_elements = elements
            bulk_coords = coords
            if surf_required:
                # We got bulk elements, but we need surface elements.  Tough.
                raise ooferror.ErrPyProgrammingError(
                    "Can't evaluate surface outputs on bulk elements!")
        else:
            # We got surface elements.
            surf_elements = elements
            surf_coords = coords
            if bulk_required:
                # Convert surface elements to bulk.
                bulk_elements = utils.MappedIterable(domain.convertToBulk,
                                                     elements)
                # Convert surface coords to bulk
                def convertCoordsToBulk(surf_elem, bulk_elem, surf_coords):
                    real_coords = map(surf_elem.from_master, surf_coords)
                    return map(bulk_elem.to_master, real_coords)
                bulk_coords = utils.MappedIterable(convertCoordsToBulk,
                                                   elements, bulk_elements,
                                                   coords)

        argdict = {}
        for inputname, inpt in self.inputs.items():
            if inpt.bulk_only:
                argdict[inputname] = inpt.evaluate(mesh, domain,
                                                   bulk_elements, bulk_coords)
            elif inpt.surface_only:
                argdict[inputname] = inpt.evaluate(mesh, domain,
                                                   surf_elements, surf_coords)
            else:
                argdict[inputname] = inpt.evaluate(mesh, domain,
                                                   elements, coords)
        for paramname, param in self.params.items():
            # Some parameters are OutputParameters, which need to be
            # evaluated before calling the callback.
            if isinstance(param, OutputParameter):
                if param.value.bulk_only:
                    argdict[paramname] = param.value.evaluate(
                        mesh, domain, bulk_elements, bulk_coords)
                elif param.value.surface_only:
                    argdict[paramname] = param.value.evaluate(
                        mesh, domain, surf_elements, surf_coords)
                else:
                    argdict[paramname] = param.value.evaluate(
                        mesh, domain, elements, coords)
            else:   # just a regular Parameter, not an OutputParameter
                argdict[paramname] = param.value

        if self.bulk_only:
            result = self.callback(mesh, bulk_elements, bulk_coords, **argdict)
        elif self.surface_only:
            result = self.callback(mesh, surf_elements, surf_coords, **argdict)
        else:
            result = self.callback(mesh, elements, coords, **argdict)
        return result

    def __eq__(self, other):
        return (self.name == other.name and
                self.callback == other.callback and
                self.params == other.params and
                self.iparms == other.iparms and
                self.inputs == other.inputs)

    def __hash__(self):
        return hash((self.name, self.callback, self.parent))

    def binaryRepr(self, datafile):
        #Get the path to the prototype that will be provided to getOutput(name)
        pathlengthstr=struct.pack(structIntFmt,len(self.getPath()))
        #string (e.g. self.getPath()) itself need not be packed
        strings=[pathlengthstr,self.getPath()]
        for pvalue in self.getSettableParams().values():
            strings.append(pvalue.binaryRepr(datafile,pvalue.value))
        return string.join(strings,'')

    def dump(self, indent=""):
        if indent=="":
            print "Output dump"
        print indent, "name:", self.name
        print indent, "callback:", self.callback
        print indent, "prototype:", self.prototype
        if self.params:
            print indent, "Params:"
            for name, param in self.params.items():
                print indent, param
        if self.aliases:
            print indent, "aliases:", self.aliases
        for name,inp in self.inputs.items():
            print indent, "input:", name
            inp.dump(indent + "   ")

# Utility function used in Output.getParameterNameHierarchy().  Takes
# a hierarchical list of Parameters names and prepends the given name
# to each.
def prependHierarchyName(name, hier):
    for i in range(len(hier)):
        if type(hier[i]) is types.ListType:
            hier[i] = prependHierarchyName(name, hier[i])
        else:
            hier[i] = string.join([name, hier[i]], ':')
    return hier

################################################################

# Outputs are stored in LabelTrees according to their otype.  These
# trees are used to construct the GUI widgets from which the user
# chooses an Output.  Outputs are put into the trees by the function
# defineOutput(), which automatically decides which LabelTree to use.

from ooflib.common import labeltree

class OutputTree(labeltree.LabelTree):
    def __setitem__(self, label, out):
        labeltree.LabelTree.__setitem__(self, label, out)
        out.prototype = True
    def insert(self, label, out, ordering=0):
        labeltree.LabelTree.__setitem__(self, label, out, ordering=ordering)
        out.prototype = True

# In 2D there used to be a set of positionOutputs whose values were
# Points or Coords, but they're no used in 3D.  In 3D the location
# where an Output is plotted is determined by a MeshNodePosition
# object, which will be used in 2D too after we merge the code.
valueOutputs = OutputTree()
scalarOutputs = OutputTree()

outputTrees = (valueOutputs, scalarOutputs)

scalarOutputCheck = parameter.TypeChecker(outputval.ScalarOutputValPtr)

def defineOutput(path, output, ordering=0):
    valueOutputs.insert(path, output, ordering=ordering)
    # Scalar outputs are inserted into both the valueOutputs and
    # scalarOutputs trees.
    if scalarOutputCheck.test(output.otype) is None:
        scalarOutputs.insert(path, output, ordering=ordering)

# There are cases in which an Output should be put into the
# scalarOutputs tree, but not in the generic valueOutputs tree,
# because the equivalent generic output is already there.  Those
# Outputs should use defineScalarOutput.

def defineScalarOutput(path, output, ordering=0):
    scalarOutputs.insert(path, output, ordering=ordering)

#################################################################

class OutputParameter(parameter.Parameter):
    pass

# A Parameter whose value is an Output whose value is a scalar.
class ScalarOutputParameter(OutputParameter):
    def checker(self, x):
        if not (isinstance(x, Output)
                and issubclass(x.otype, outputval.ScalarOutputValPtr)):
            parameter.raiseTypeError(type(x), 'Scalar Output')
    def valueDesc(self):
        return "An <link linkend='Section-Output-Scalar'><classname>Output</classname></link> object whose value is a real number."

# Parameter for outputs which are not positionOutputs, but rather are
# the values of things.  This class mainly has the valueDesc string.
class ValueOutputParameter(OutputParameter):
    def checker(self, x):
        if not isinstance(x, Output):
            parameter.raiseTypeError(type(x), 'Output')
    def valueDesc(self):
        return "An <link linkend='Section-Output-Value'><classname>Output</classname></link> object whose value is a composite object."""

    def binaryRepr(self, datafile, value):
        return value.binaryRepr(datafile)
    def binaryRead(self, parser):
        #First get path to prototype output
        (pathlengthstr,)=struct.unpack(structIntFmt,
                                       parser.getBytes(structIntSize))
        pathstr=parser.getBytes(pathlengthstr)
        prototypeoutput=getOutput(pathstr)
        argdict={}
        for pname,pvalue in prototypeoutput.getSettableParams().items():
            pvalueclone=pvalue.clone()
            #The following line should set the value of pvalueclone
            pvalueclone=pvalue.binaryRead(parser)
            argdict[pname]=pvalueclone
        return prototypeoutput.clone(params=argdict)

def getOutput(name, **kwargs):
    # Look for the prototype output by searching the OutputTrees
    for tree in outputTrees:
        try:
            leaf = tree[name]
        except KeyError:
            pass
        else:
            # It's possible for the name of an Output in one tree to
            # be only a partial path in another tree, so even if
            # 'name' is a valid path in a tree, it's necessary to
            # check that something is stored there.
            if leaf.object:
                return leaf.object.clone(params=kwargs)
    raise KeyError("Unknown Output: %s" % name)

utils.OOFdefine('getOutput', getOutput)
