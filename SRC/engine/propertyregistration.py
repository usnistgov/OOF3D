# -*- python -*-
# $RCSfile: propertyregistration.py,v $
# $Revision: 1.117.2.5 $
# $Author: langer $
# $Date: 2014/12/08 19:41:52 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

# This file defines the PropertyRegistration class, which is used
# to get information on how to construct instances of the registered
# property classes when no such instances exist.

# Also, this file defines/contains the global AllProperties object,
# which looks like a dictionary, but has the capability of notifying
# the world when something has been inserted -- this is so the
# GUI PropertyTree can be updated.

from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.engine import properties
from ooflib.common import debug
from ooflib.common import labeltree
from ooflib.common import utils
from ooflib.common.IO import mainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import reporter
from ooflib.common.IO import xmlmenudump
from ooflib.common import parallel_enable
import string, types, sys


# Load the convertible registered types used as parameters
# by the properties.
from ooflib.engine.IO import isocijkl
from ooflib.engine.IO import orientationmatrix

#Interface branch
from ooflib.engine.IO import interfaceparameters

# The PropertyManager is the object over which the GUI's propertyTree
# is built.  It has as data a labeltree whose objects are property
# registration entries.  There are two kinds of leaf entities on the
# tree, those corresponding to imported property classes and hosting a
# "generic" (or "unnamed") potential-instance, and their immediate
# children, are named instances of the property class corresponding to
# their parent.

OOF = mainmenu.OOF

OOF.addItem(oofmenu.OOFMenuItem(
    'Property',
    cli_only=1,
    help='Create, modify, and delete material properties.',
    discussion="""<para>

    The <command>Property</command> menu contains the basic tools for
    managing material &properties;.  Unnamed versions of all
    &properties; are created when &oof2; starts.  The <link
    linkend='MenuItem-OOF.Property.Copy'><command>Copy</command></link>
    command creates <emphasis>named</emphasis> copies of &properties;.
    The <link
    linkend='MenuItem-OOF.Property.Parametrize'><command>Parametrize</command></link>
    menu changes the parameters of named and unnamed &properties;, and
    the <link
    linkend='MenuItem-OOF.Property.Delete'><command>Delete</command></link>
    command removes named &properties;.

    </para>"""
    ))

OOF.LoadData.addItem(oofmenu.OOFMenuItem(
    'Property'
    ))

#=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=#

# MenuKey objects are used to identify the various menus that are
# automatically created from the Property LabelTree.

class MenuKey:
    def __init__(self, string):
        self.string = string
parametrizeKey = MenuKey('Parametrize')
loadKey = MenuKey('Load')

#=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=#

class PropertyManager:
    def __init__(self):
        self.materialmanager = None # Set by materialmanager when it starts up.
        self.data = labeltree.LabelTree()

        # Need to own the references to the key objects, which are
        # only weakly referenced in LabelTree, and used to identify
        # menus.  This allows the menus to disappear automatically
        # when the PropertyManager is destroyed.  (Why bother?  The
        # PropertyManager isn't destroyed until the program quits.)
        self.parametrizekey = parametrizeKey
        self.loadkey = loadKey

        def paramcopy(object):
            # This routine is a callback function passed to
            # LabelTree.makeOOFMenu. makeOOFMenu uses it to get the
            # list of parameters for each menuitem that it creates.
            # The 'object' argument is the PropertyRegistration for
            # which the menu item is being built.

            # It's tempting to simply return the
            # PropertyRegistration's list of Parameters, so that the
            # registration and the menu item share Parameter objects,
            # and eliminating the need to copy values back and forth.
            # This temptation must be resisted.  If the Parameters are
            # shared, then loading a named Property from a data file
            # will change the settings of an already parametrized
            # unnamed Property.
            if object:
                return [ p.clone() for p in object.getDefaultParams() ]
            return []
        
        def kwarg_func(object):         # Extra kwargs for OOFMenuItem ctor.
            if object and object.secret():
                return {'secret':1, 'no_doc':1}
            return {}

        # Menu items are put into OOF.Property for scripts and
        # OOF.LoadData.Property for data files.  The menus are created
        # automatically by the LabelTree, which uses the given key to
        # distinguish them.
        OOF.Property.addItem(self.data.makeOOFMenu(
            # The name 'Parametrize' is also used in _parametrizeDiscussion.
            # Don't change it here without changing it there.
            name='Parametrize',
            key=self.parametrizekey,
            param_func = paramcopy,
            kwarg_func = kwarg_func,
            callback = self.parametrizercallback,
            help=xmlmenudump.DiscussionFunc(_parametrizeHelp),
            discussion=xmlmenudump.DiscussionFunc(_parametrizeDiscussion)))

        OOF.LoadData.addItem(self.data.makeOOFMenu(
            name='Property',
            key=self.loadkey,
            param_func = paramcopy,
            kwarg_func = kwarg_func,
            callback = self.creatorcallback,
            params = [parameter.StringParameter('name',
                                                tip="Name of Property.")],
            discussion=xmlmenudump.DiscussionFunc(_loadDiscussion),
            help=xmlmenudump.DiscussionFunc(_loadHelp)))

    # __setitem__ gets called whenever a new registration is
    # instantiated.  This happens for unnamed properties at start-up
    # time and for named properties whenever they're created.  Does
    # collision detection by first attempting a retrieval on the key
    # -- if that succeeds, you drop through to the "else:".
    def __setitem__(self,key,value):
        try:
            collision = self.data[key]
        except labeltree.LabelTreeKeyError:
            # Key not found, OK to insert. 
            propclass = string.split(key,':')[-1]

            # Add it to the labeltree.
            self.data.__setitem__(key, value, ordering=value.ordering)
        else:
            # Name-collision has occurred.  This is only an error
            # if the parameter values conflict.
            for (p1, p2) in zip(collision.object.params, value.params):
                if (p1.name != p2.name) or (p1.value != p2.value):
                    raise KeyError(
                        "Assignment collision in PropertyManager, key %s."
                        % `key`)


    # Make a named instance of the given property.  Called by
    # OOF.Property.Copy, so it's not necessary to do all the checks
    # done in __setitem__.  The passed-in newname is the leaf
    # component, but oldname is a fully qualified name.
    def new_prop(self, oldname, newname):
        oldreg = self.data[oldname].object
        if hasattr(oldreg , "parent"):
            namelist = string.split(oldname, ':')[:-1]
            fullname = string.join(namelist+[newname], ':')
        else:
            fullname = oldname+":"+newname
        newreg = oldreg.named_copy(fullname)
        switchboard.notify("new property", newreg)
    
    def __getitem__(self, key):
        return self.data[key].object

    # Delete the named item.  LabelTree ("self.data") will raise
    # ErrUserError if the named item is a non-leaf.
    def delete(self, name):
        reg = self.data[name].object
        if hasattr(reg, "parent"):
            self.materialmanager.delete_prop(name)
            reg.unregister()
            self.data.delete(name)
        else:
            reporter.warn("Predefined properties cannot be deleted!")

    # Delete all copied (not predefined) Properties.
    def deleteAll(self):
        # Get a list of all the Properties to delete
        doomed = []
        def deleter(path, reg, doomed):
            if hasattr(reg, "parent"):
                doomed.append((path, reg))
        self.data.apply2(deleter, doomed=doomed)
        # Delete them.
        for path, reg in doomed:
            self.materialmanager.delete_prop(path)
            reg.unregister()
            self.data.delete(path)
        

    # Property name uniquifier, used when copying.  "oldprop" is a
    # fully qualified name of an existing property, and newname is an
    # unqualfied candidate "leaf" name.
    def uniqueName(self, oldprop, newname):
        oldreg = self.data[oldprop].object
        try:
            contextreg = oldreg.parent
        except AttributeError:
            contextreg = oldreg
        # Get the labeltreenode.
        ltn = self.data[self.data.objpath(contextreg)]
        nameset = ltn.children()
        return utils.menUniqueName(newname, nameset)
        

    # This menu callback gets called when the parameters of a
    # property are changed.  Figure out which property registration
    # object is relevant, and run its new_params() method.
    def parametrizercallback(self, menuitem, **kwargs):
        if parallel_enable.enabled():
            OOF.LoadData.IPC.Property.Parametrize(**kwargs)
        else:
            # Translate the menuitem's path to the tree's path.  The first
            # three words of the path are OOF.Property.Parametrize.
            # We want the remainder.
            treepath = string.split(menuitem.path(),".")[3:]
            reg = self.data[treepath].object
            reg.new_params(**kwargs)
            switchboard.notify("redraw")

    # This method is called by propertymenuIPC.py during
    # initialization.  It is not placed in PropertyManager.__init__
    # because OOF.LoadData.IPC.Property has not been added yet.
    def set_parallel_parametrizercallback(self):
        def paramcopy(object):
            if object:
                return [ p.clone() for p in object.getDefaultParams() ]
            return []

        def kwarg_func(object):         # Extra kwargs for OOFMenuItem ctor.
            if object and object.secret():
                return {'secret':1, 'no_doc':1}
            return {}

        # Take the ipc menu already created in propertymenuIPC and
        # build a menu for parametrizing to all processes
        ipcpropmenu=OOF.LoadData.IPC.Property
        ipcpropmenu.addItem(self.data.makeOOFMenu(
            name='Parametrize',
            key=self.parametrizekey,
            param_func = paramcopy,
            kwarg_func = kwarg_func,
            callback = self.parallel_parametrizercallback,
            threadable=oofmenu.PARALLEL_THREADABLE))

    def parallel_parametrizercallback(self, menuitem, **kwargs):
        # The first five words of menuitem.path() are
        # OOF.LoadData.IPC.Property.Parametrize
        # We want the remainder.
        treepath = string.split(menuitem.path(),".")[5:]
        reg = self.data[treepath].object
        reg.new_params(**kwargs)
        switchboard.notify("redraw")

    # Menu callback for OOF.LoadData.Property.  "reg" is the
    # registration entry corresponding to the menu item that initiated
    # the callback, e.g.
    # "OOF.LoadData.Property.Create.Elasticity.IsoElasticity".  The
    # PropertyRegistration and NamedPropertyRegistration's writeData
    # methods ensure that "reg" is always a PropertyRegistration.
    def creatorcallback(self, menuitem, **kwargs):
        treepath = string.split(menuitem.path(),".")[3:]
        reg = self.data[treepath].object
        name = menuitem.params[0].value

        # Collision looks for the name under this tree, and if it
        # finds it, checks if the parameter values are all equal.  If
        # a collision occurs and the parameters conflict, an exception
        # is raised.  If collision returns "true", that means a
        # collision occurred but the parameters matched.  If collision
        # returns "false", a collision did not occur.
        namecollision, parametercollision = reg.collision(name,
                                                          menuitem.params[1:])
        if namecollision:               # name is a duplicate
            if parametercollision:      # parameters disagree
                if name != "":
                    raise ooferror.ErrSetupError("Named property in datafile conflicts with existing property '%s'" % name)
                # reparametrization of unnamed property
                if reg.materials:
                    raise ooferror.ErrSetupError("Unnamed property in datafile conflicts with existing property '%s'" % name)
                # Unnamed property is being reparametrized, but it's
                # not used in any materials, so it's ok.
                reg.new_params(**kwargs)
                switchboard.notify("redraw")
            # A name collision with no parameter collision doesn't
            # require any action.  The data file contained a property
            # identical to an existing property.
        else:
            # No collision, we must create a new NamedRegistration.
            # We know it's a NamedRegistration because unnamed
            # property registrations *always* produce a name conflict.
            fullname = string.join( treepath + [name], ":")
            newreg = reg.named_copy(fullname, menuitem.params[1:])
            switchboard.notify("redraw")

#=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=#

# _PropertyStructureInfo and its helper classes, _PropertyFieldInfo
# and _PSInfo, keep track of how a Property is used, ie, how it
# interacts with Fields, Fluxes, and Equations.

class _PropertyFieldInfo:
    def __init__(self, time_derivs, nonlinear, time_dependent):
        self.time_derivs = time_derivs
        self.nonlinear = nonlinear
        self.time_dependent = time_dependent

class _PSInfo:
    # _PSInfo is used within _PropertyStructureInfo to store the
    # fields used by a single Flux or Equation.
    def __init__(self):
        self._fields = {}
    def add(self, field, time_derivs, nonlinear, time_dependent):
        # field might be None if the property doesn't have any field dependence
        self._fields[field] = _PropertyFieldInfo(time_derivs, nonlinear, 
                                                 time_dependent)
    def fields(self):
        return self._fields.keys()
    def fields_of_order(self, order):
        return [f for f in self._fields
                if (f is not None and
                    order in self._fields[f].time_derivs)]
    def nonlinear(self, fields):
        # Is the property nonlinear in any of the given fields? 
        for field in fields+[None]:
            try:
                if self._fields[field].nonlinear:
                    return True
            except KeyError:
                pass
        return False
    def timeDependent(self, fields):
        for field in fields+[None]:
            try:
                if self._fields[field].time_dependent:
                    return True
            except KeyError:
                pass
        return False

class _PropertyStructureInfo:
    def __init__(self):
        self._dict = {}         # key = Flux or Equation obj, value = _PSInfo
    def add(self, obj, field, time_derivs=[], nonlinear=False,
            time_dependent=False):
        # obj is either a Flux or an Equation
        try:
            info = self._dict[obj]
        except KeyError:
            info = self._dict[obj] = _PSInfo()
        info.add(field, time_derivs, nonlinear, time_dependent)
    def fields(self):
        flds = set()
        for pinfo in self._dict.values():
            flds.update(pinfo.fields())
        return [f for f in flds  if f is not None]

    # These functions *could* use the "fields_of_order(x)" scheme, but
    # in the calling context (subproblem and materials), they're
    # really clearer this way.
    def first_order_fields(self, objs):
        flds = set()
        for obj in objs:
            try:
                flds.update(self._dict[obj].fields_of_order(1))
            except KeyError:
                pass
        return list(flds)
    def second_order_fields(self, objs):
        flds = set()
        for obj in objs:
            try:
                flds.update(self._dict[obj].fields_of_order(2))
            except KeyError:
                pass
        return list(flds)
    def time_deriv_fields(self, objs):
        flds = set()
        for obj in objs:
            try:
                flds.update(self._dict[obj].fields_of_order(1))
                flds.update(self._dict[obj].fields_of_order(2))
            except KeyError:
                pass
        return list(flds)
    def all(self):
        return self._dict.keys()
    def nonlinear(self, fields):
        for key,pinfo in self._dict.items():
            if pinfo.nonlinear(fields):
                return True
        return False
    def timeDependent(self, fields):
        for pinfo in self._dict.values():
            if pinfo.timeDependent(fields):
                return True
        return False
            

#=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=#

# Property registrations live in the tree data structure of the
# PropertyManager, and consequently are managed separately from the
# usual OOF Registration mechanism.  They do their own tree-based
# collision detection, and are not known to the global OOF namespace.
# Properties are instanced via the "OOF.Property.Create..." menu in
# scripts, and parametrized via the "OOF.Property.Parametrize..." 
# menu.  PropertyRegistration and NamedPropertyRegistration objects
# differ in that the former construct a default name for themselves,
# whereas the latter accept one as an argument.  Both prepend the
# resulting name as a parameter to their parameter list.

class PropertyRegistrationParent:
    def __init__(self, subclass, modulename, ordering, secret):
        self.subclass = subclass        # for PythonExportability of Property
        self.modulename = modulename    # ditto
        self.ordering = ordering
        properties.Property.registry.append(self)
        self._secret = secret

    def unregister(self):
        del properties.Property.registry[self.getIndex()]

    def getIndex(self):
        for i in range(len(properties.Property.registry)):
            if properties.Property.registry[i] is self:
                return i
    def secret(self):
        return self._secret
    
# PropertyRegistration knows special things about itself, like the
# fact that all properties have names as their first arguments.
# Property nonlinearity is stored here at registration-time, by
# passing "nonlinear=1" in to here.  Nonlinear properties force the
# recomputation of the stiffness matrix when mesh.make_stiffness is
# called, even if the mesh itself hasn't changed.
class PropertyRegistration(PropertyRegistrationParent):
    def __init__(self, name, subclass, modulename, ordering, params=[],
                 propertyType=None,
                 outputs=[],
                 secret=0,
                 interfaceCompatibility=interfaceparameters.COMPATIBILITY_BULK_ONLY,
                 interfaceDiscontinuousFields=[],
                 tip=None,
                 discussion=None):

        PropertyRegistrationParent.__init__(self, subclass,
                                            modulename, ordering, secret)

        # Save the fully-qualified name for error reporting.  This
        # datum should not be confused with the parameter "name",
        # which contains only the leaf part of the FQN.
        self._name = name
        # Keep a copy of the local parameters.
        self.params = params

        # Equations to which this property makes *direct*
        # contributions (ie, not via a flux).  This is a basically a
        # dictionary of _PSInfo objects, keyed by Equation.
        self._equations = _PropertyStructureInfo()
        # Ditto, for Fluxes instead of Equations
        self._fluxes = _PropertyStructureInfo()
        self._constraints = _PropertyStructureInfo()

        self._outputs = outputs    # names of PropOutputs it contributes to
        self.tip = tip
        self.discussion = discussion  # discussion string or loadFile
        
        if propertyType is None:
            raise ooferror.ErrPyProgrammingError(
                "Missing propertyType in PropertyRegistration %s" % name)
        self._propertyType=propertyType

        #Interface branch
        self._interfaceCompatibility=interfaceCompatibility
        self._interfaceDiscontinuities=interfaceDiscontinuousFields

        # name-indexed dictionary of materials in which this property
        # occurs -- it is managed by the MaterialProps objects, except
        # in the new_params call, where it is local.
        self.materials = {}
        # At creation time, all parameters are new.
        self.new_params()

        # Add yourself to the AllProperties data object.  "name"
        # must be the fully qualified name of the property.
        AllProperties[name]=self

    # This returns the fully-qualified name in the labeltree.
    def name(self):
        return self._name

    def baseName(self):       # different in NamedPropertyRegistration
        return self._name

    # After creating a Registration, eqnInfo and fluxInfo must be
    # called to indicate which Fields the Property uses, and how they
    # appear in the Equations and Fluxes.  
    #
    # The nonlinear arg can be either a list or tuple of Fields in
    # which the Property is nonlinear, or a bool.  If it's a bool, it
    # applies to all Fields in the fields arg.

    def fluxInfo(self, fluxes, fields=[None], time_derivs=[], nonlinear=False,
                 time_dependent=False):
        for flux in fluxes:
            for field in fields:
                nl = ((isinstance(nonlinear, (types.ListType, types.TupleType))
                       and field in nonlinear)
                      or nonlinear)
                self._fluxes.add(flux, field, time_derivs, nl, time_dependent)

    def eqnInfo(self, equations, fields=[None], time_derivs=[],
                nonlinear=False, time_dependent=False):
        # fields == [None] means that the property makes a
        # contribution to the equation when no fields are defined.
        # fields==[] is different!  It means that the property makes
        # no contributions.
        for eqn in equations:
            for field in fields:
                nl = ((isinstance(nonlinear, (types.ListType, types.TupleType))
                       and field in nonlinear)
                      or nonlinear)
                self._equations.add(eqn, field, time_derivs, nl, time_dependent)

    def constraintInfo(self,equations,fields=[None]):
        # Constraint equations the property contributes to, if any.
        # The fields mentioned must be defined but need not be active.
        for eqn in equations:
            for field in fields:
                self._constraints.add(eqn, field)

    def discontinuousFields(self):
        return self._interfaceDiscontinuities
    
    # These functions are different in the NamedPropertyRegistration
    def nonlinear(self, fields):
        return (self._fluxes.nonlinear(fields) or
                self._equations.nonlinear(fields))
    def timeDependent(self, fields):
        return (self._fluxes.timeDependent(fields) or
                self._equations.timeDependent(fields))
    def fields(self):
        return set(self._equations.fields() + self._fluxes.fields())
    def second_order_fields(self, *equations):
        return self._equations.second_order_fields(equations)
    def first_order_fields(self, *equations):
        return self._equations.first_order_fields(equations)
    def time_deriv_fields(self, *equations):
        return self._equations.time_deriv_fields(equations)
    def fluxes(self):
        return self._fluxes.all()
    def equations(self):
        return self._equations.all()
    def propertyType(self):
        return self._propertyType
    def outputs(self):
        return self._outputs
    
    def is_property_type(self, other_name):
        # Don't use self._propertyType, you might be the derived class.
        return self.propertyType()==other_name

    #Interface branch
    def interfaceCompatibility(self):
        return self._interfaceCompatibility

    # "Call" method creates a property instance from a registration.
    # This is the only way to create a property instance, and this
    # routine does not do any book-keeping with the AllProperties
    # object.  We do not use the Registration class's __call__ method,
    # because we need to pass the registration itself as an argument to
    # the property constructor.
    def __call__(self):
        return self.subclass(self, self._name, *[p.value for p in self.params])


    # Collision looks for the name under this tree, and if it finds
    # it, checks if the parameter values are all equal.  Called by
    # PropertyManager.creatorcallback, which is the callback for
    # OOF.LoadData.Property.

    # Return value is (namecollision, parametercollision)
    def collision(self, name, params):
        if name == "":
            for ppair in zip(params, self.params):
                if ppair[0].value != ppair[1].value:
                    return (1, 1)
            return (1, 0)
        else: # Nontrivial name, look for it in the local subtree.
            ltn = AllProperties.data.reverse_dict[self]
            for other in [x.object for x in ltn.nodes]:
                if other.moniker==name:
                    # "Other" params list starts with a name, because
                    # it's a NamedPropertyRegistration -- don't compare that
                    # one, passed-in params omits it.
                    for ppair in zip(params, other.params[1:]):
                        if ppair[0].value != ppair[1].value:
                            return (1, 1)
                    return (1, 0) # Collision occurred, parameters matched.
            return (0, 0) # Made it through "other", no collision.


    # Called locally via the init or from the menucallback function.
    # (The GUI calls the menu when the dialog box closes).  Builds
    # new property instances for all the materials it knows about.
    def new_params(self, **kwargs):
        for p in self.params:
            if p.name != "name":
                try:
                    p.value = kwargs[p.name]
                except KeyError:
                    pass
        # "m" is a MaterialProps object, "o" is the old property instance.
        for (m, o) in self.materials.values():
            newcopy = self() # Run the registration to get the prop.
            m.new_params(o, newcopy)
            self.materials[m.name]=(m, newcopy)
            switchboard.notify("material changed", m.name)

    def add_material(self, matname, matdata):
        self.materials[matname]=matdata

    def remove_material(self, matname):
        del self.materials[matname]

    def rename_material(self, newmatname, oldmatname):
        self.materials[newmatname]=self.materials[oldmatname]
        del self.materials[oldmatname]

    def __repr__(self):
        return "PropertyRegistration(%s, %s, %s)" % \
               (self.subclass.__name__, `self.ordering`,
                `self.params`)

    def writeData(self, datafile):
        datafile.startCmd(
            AllProperties.data.reverse_dict[self].\
            getOOFMenu(AllProperties.loadkey))
        datafile.argument('name', '')
        for param in self.params:
            datafile.argument(param.name, param.value)
        datafile.endCmd()

    def getDefaultParams(self):
        return self.params[:]

    # Create a NamedPropertyRegistration from yourself.
    # Called from PropertyManager.new_prop() and
    # PropertyManager.creatorcallback()
    def named_copy(self, name, instance_params=[], secret=None):
        if secret is None:
            secret = self._secret
        old_params = instance_params or self.params
        new_params = [parameter.StringParameter('name',name)] + \
                     [p.clone() for p in old_params]
        return NamedPropertyRegistration(self, name, self.subclass,
                                         self.modulename, 
                                         self.ordering, new_params,
                                         secret)
    def getParameter(self, name):
        for p in self.params:
            if p.name == name:
                return p
    
# Registration object for named properties.  Conventionally,
# all named properties have an "ordering" equal to that of their
# parent.  They differ from the PropertyRegistration class in
# being created automatically by the tree, and by having a "parent"
# attribute which refers to a PropertyRegistration object.
class NamedPropertyRegistration(PropertyRegistration):
    def __init__(self, parent, name, subclass,
                 modulename, ordering, params, secret):
        
        ## TODO 3.1: Why does NamedPropertyRegistration inherit from
        ## PropertyRegistration, but call PropertyRegistrationParent's
        ## __init__?  Is the class hierarchy strange?
        PropertyRegistrationParent.__init__(self, subclass,
                                            modulename, ordering, secret)

        self._name = name
        self.moniker = string.split(name,":")[-1]
        self.parent = parent
        self.materials = {}
        self.params = params
        # At creation-time, all params are new.
        self.new_params()

        # Add yourself to the AllProperties object.  "name"
        # should be a fully qualified name.
        AllProperties[name] = self

    def baseName(self):
        return self.parent.baseName()

    def nonlinear(self, fields):
        return self.parent.nonlinear(fields)
    def timeDependent(self, fields):
        return self.parent.timeDependent(fields)
    def fields(self):
        return self.parent.fields()
    def second_order_fields(self, *eqns):
        return self.parent.second_order_fields(*eqns)
    def first_order_fields(self, *eqns):
        return self.parent.first_order_fields(*eqns)
    def time_deriv_fields(self, *eqns):
        return self.parent.time_deriv_fields(*eqns)
    def fluxes(self):
        return self.parent.fluxes()
    def equations(self):
        return self.parent.equations()
    def propertyType(self):
        return self.parent.propertyType()
    def outputs(self):
        return self.parent.outputs()

    #Interface branch
    def interfaceCompatibility(self):
        return self.parent.interfaceCompatibility()

    # We do not expect NamedPropertyRegistrations to be used
    # for anything other than direct instantiation via the pre-set
    # params, so no kwargs for this one.  2nd argument is name.
    def __call__(self):
        return self.subclass(self, self._name, 
                             *[p.value for p in self.params[1:]])

    def __repr__(self):
        return "NamedPropertyRegistration(%s, %s, %s, %s)" % \
               (`self.moniker`, self.subclass.__name__, `self.ordering`,
                `self.params`)

    def writeData(self, datafile):
        datafile.startCmd(
            AllProperties.data.reverse_dict[self.parent].\
            getOOFMenu(AllProperties.loadkey))
        
        # Use only the tail of the fully-qualified name in the menu,
        # for brevity.  The menu item implicitly knows the rest of the
        # name.
        datafile.argument('name', self.moniker)
        for param in self.params[1:]:
            datafile.argument(param.name, param.value)
        datafile.endCmd()

    # Similar to parent "named_copy", except it gets the ordering from
    # the parent.
    def named_copy(self, name, instance_params = [], secret=None):
        if secret is None:
            secret = self._secret
        # Don't clone the name parameter, since the new property has a new name.
        non_name_params = instance_params or self.params[1:]
        new_params = [parameter.StringParameter('name', name)] + \
                     [p.clone() for p in non_name_params]
        return NamedPropertyRegistration(self.parent, name, self.subclass,
                                         self.modulename, 
                                         self.parent.ordering, new_params,
                                         secret)
    
    # Return all except the "name" parameter, which is fixed by
    # the tree structure.
    def getDefaultParams(self):
        return self.params[1:]

#=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=#

# Functions for getting xml documentation out of a Property menu item.
# These all work by extracting the property registration from the
# menuitem.  If there's no PropertyRegistration for this menuitem,
# then the menuitem is an intermediate node in the Property tree, in
# which case the name of the Property class is extracted from the
# menuitem's path.

def _parametrizeDiscussion(menuitem):
    # It's ok if this raises an AttributeError
    reg = menuitem.data
    if reg:
        return """<para> 

Set the parameters for the unnamed material &property;,
<classname>%s</classname>.  To create a <emphasis>named</emphasis>
copy of the &property;, use <xref
linkend='MenuItem-OOF.Property.Copy'/>, and use
<command>OOF.Property.%s.</command><emphasis>name</emphasis> to set
its parameters. 
</para>

<para>
See <xref linkend="Property-%s"/> for a complete description of the
parameters for this &property;.
</para>
""" % (reg.name(), reg.name().replace(':','.'), reg.name().replace(':','-'))

    # No discussion section for intermediate nodes in the Property
    # tree, except for the root.
    if reg.path() == 'OOF.Property.Parametrize':
        return """<para>
        The <command>Parametrize</command> menu contains an entry for
        each <emphasis>unnamed</emphasis> &property;.  The menu
        hierarchy echoes the hierarchical arrangement of the
        &properties; themselves.  Each command sets the parameters of
        a &property;.  The <emphasis>named</emphasis> &properties;
        appear in the menus as submenus for their unnamed
        counterparts.  They aren't listed in the documentation,
        though.  </para>"""
    return ""

def _parametrizeHelp(menuitem):
    reg = menuitem.data
    if reg:
        try:
            return reg.tip
        except AttributeError:
            name = reg.name()
            return "Set parameters for a%s %s Property." \
                   % ('n'*(name[0] in 'aeiouAEOIU'), name)
    splitpath = menuitem.path().split('.')
    proppath = splitpath[3:]            # remove "OOF.Property.Parametrize"
    return "Set parameters for %s Properties" % string.join(proppath, '.')
    

def _loadDiscussion(menuitem):
    reg = menuitem.data
    if reg:
        name = reg.name()
        return  """
<para>
Create an instance of the material &property;
<classname>%s</classname>.  This command is only used in data files.
Data files containing &properties; are created by the <link
linkend='MenuItem-OOF.File.Save.Materials'><command>Materials</command></link>,
<link
linkend='MenuItem-OOF.File.Save.Microstructure'><command>Microstructure</command></link>,
<link
linkend='MenuItem-OOF.File.Save.Skeleton'><command>Skeleton</command></link>
and <link
linkend='MenuItem-OOF.File.Save.Mesh'><command>Mesh</command></link>
commands in the <xref linkend='MenuItem-OOF.File.Save'/> menu.
</para> <para> The <varname>name</varname> argument should be set to
the name of a named &property; or to an empty string
(<userinput>''</userinput>) when setting parameters in an unnamed
&property;.
</para>
<para>
See <xref linkend="Property-%s"/> for a complete description of the
parameters for this &property;.
</para>
                """ % (reg.name(), reg.name().replace(':','-'))

        return intro + xmlmenudump.getDiscussion(reg)

    # No discussion section for intermediate nodes in the Property
    # tree, except for the root.
    if reg.path() == 'OOF.LoadData.Property':
        return """<para>

        The <command>OOF.LoadData.Property</command> menu contains an
        entry for each <emphasis>unnamed</emphasis> &property;.  The
        menu hierarchy echoes the hierarchical arrangement of the
        &properties; themselves.  The commands are used only in data
        files, where each command sets the parameters of a &property;.
        Unlike the <xref linkend='MenuItem-OOF.Property.Parametrize'/>
        menu, which is also based on the &property; hierarchy, the
        <command>OOF.LoadData.Property</command> menu does not include
        named properties.  Instead, each command has a
        <varname>name</varname> argument, which is set to an empty
        string (<userinput>''</userinput>) when assigning parameters
        to unnamed &properties;.</para>"""

    return ""

    
def _loadHelp(menuitem):
    reg = menuitem.data
    if reg:
        try:
            return reg.tip + " Used internally in data files."
        except:
            name = reg.name()
            return "Define a%s %s Property.  Used internally in data files." \
                   % ('n'*(name[0] in 'aeiouAEIOU'), name)
    splitpath = menuitem.path().split('.')
    proppath = splitpath[3:]            # remove "OOF.LoadDataProperty"
    return "Set parameters for %s Properties.  This menu is used only in data files." % string.join(proppath, '.')
    

def xmldocs(phile):
    # Called by xmldump in problem.py.

    # First, do some bookkeeping 
    ptypedict = {}  # lists of Properties of each PropertyType.
    propdict = {}   # lists of Properties for each equation, field, or flux
    for reg in AllProperties.data.getObjects():
        if reg.secret():
            continue
        ptype = reg.propertyType()
        try:
            ptypedict[ptype].append(reg)
        except KeyError:
            ptypedict[ptype] = [reg]
        # propdict is returned to problem.xmldump so that equations
        # and fluxes can list their relevant properties.
        for eqn in reg.equations():
            try:
                propdict[eqn].append(reg)
            except KeyError:
                propdict[eqn] = [reg]
        for flux in reg.fluxes():
            try:
                propdict[flux].append(reg)
            except KeyError:
                propdict[flux] = [reg]
        for field in reg.fields():
            try:
                propdict[field].append(reg)
            except KeyError:
                propdict[field] = [reg]


    print >> phile, "<section id='Section-Properties'>"
    print >> phile, "<title>Material Properties</title>"
    print >> phile, """
<para>
This is a listing of &properties; by category.  Each &material; may
have at most one &property; from each category.  Follow the links for
more detail about each &property;, including which &fields; it
requires and which &fluxes; and/or &equations; it contributes to.
</para>"""
    print >> phile, "<itemizedlist>"
    ptypes = ptypedict.keys()
    ptypes.sort()
    for ptype in ptypes:
        print >> phile, '<listitem id="PropertyType-%s">' % ptype
        print >> phile, '<para>', ptype
        print >> phile, '<itemizedlist>'
        for reg in ptypedict[ptype]:
            print >> phile, '<listitem><simpara><link linkend="Property-%s">%s</link></simpara></listitem>' % (reg.name().replace(':', '-'), reg.name())
        print >> phile, '</itemizedlist>'
        print >> phile, '</para>'
        print >> phile, '</listitem>'
    print >> phile, '</itemizedlist>'

    # Create a refentry page for each Property
    for reg in AllProperties.data.getObjects():
        if reg.secret():
            continue
        name = reg.name()
        idname = name.replace(':', '-')
        ptype = reg.propertyType()
        xmlmenudump.xmlIndexEntry(name, ptype+" Property", "Property-"+idname)
        print >> phile, '<refentry xreflabel="%s" id="Property-%s" role="Property">' \
            % (name, idname)
        print >> phile, '<refnamediv>'
        print >> phile, '<refname>%s</refname>' % name
        if reg.tip is not parameter.emptyTipString:
            tip = reg.tip or "MISSING PROPERTY TIP STRING for %s" % name
        else:
            tip = ""
        print >> phile, '<refpurpose>%s</refpurpose>' % tip
        print >> phile, '</refnamediv>'
        print >> phile, '<refsect1>'
        print >> phile, '<title>Details</title>'
        print >> phile, '<itemizedlist>'
        # Category
        print >> phile, '<listitem><simpara>'
        print >> phile, 'Property Category: <link linkend="PropertyType-%(t)s">%(t)s</link>' % dict(t=ptype)
        print >> phile, '</simpara></listitem>'
        # Parameters
        print >> phile, '<listitem>'
        print >> phile, '<para>Parameters:'
        print >> phile, '<variablelist>'
        for param in reg.params:
            print >> phile, '<varlistentry>'
            print >> phile, '<term><varname>%s</varname></term>' % param.name
            print >> phile, '<listitem>'
            if param.tip is not parameter.emptyTipString:
                tip = param.tip or "MISSING PROPERTY PARAMETER TIP for %s"%name
            else:
                tip = ""
            print >> phile, '<simpara>%s <emphasis>Type</emphasis>: %s </simpara>'\
                % (tip, param.valueDesc())
            print >> phile, '</listitem>'
            print >> phile, '</varlistentry>'
        print >> phile, '</variablelist>'
        print >> phile, '</para></listitem> <!-- Parameters -->'

        for classname, plural, objlist in [('Field', 'Fields', reg.fields()),
                                 ('Flux', 'Fluxes', reg.fluxes()),
                                 ('Equation', 'Equations', reg.equations())]:
            if objlist:
                print >> phile, '<listitem><simpara>'
                text = ["<link linkend='%s-%s'><varname>%s</varname></link>"
                        % (classname, obj.name(), obj.name())
                        for obj in objlist]
                print >> phile, "%s: %s" % (plural, ", ".join(text))
                print >> phile, '</simpara></listitem>'

        print >> phile, '</itemizedlist>'
        print >> phile, '</refsect1> <!-- Details -->'

        print >> phile, '<refsect1>'
        print >> phile, '<title>Discussion</title>'
        try:
            print >> phile, xmlmenudump.getDiscussion(reg)
        except AttributeError:
            print >> phile, "<para>MISSING PROPERTY DISCUSSION: %s</para>" % name
        print >> phile, '</refsect1> <!-- Discussion -->'
        print >> phile, '</refentry>'

    print >> phile, "</section> <!-- Properties -->"

    return propdict

#=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=#
    
# AllProperties is the global instance of the manager.
AllProperties = PropertyManager()



