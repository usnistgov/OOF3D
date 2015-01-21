# -*- python -*-
# $RCSfile: xmlmenudump.py,v $
# $Revision: 1.59.4.1 $
# $Author: langer $
# $Date: 2014/09/27 22:34:07 $


# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.common import debug
from ooflib.common import enum
from ooflib.common import labeltree
from ooflib.common import utils
from ooflib.common.IO import parameter
import string
import types

enumdict = {}
regclassdict = {}

#################

# Keep track of which parameter types need to be documented.  This
# function is called on every parameter that appears in a menu item.

def process_param(param):
    global regclassdict
    global enumdict
    # Check for RegisteredParameters
    if isinstance(param, parameter.RegisteredParameter):
        processRegClass(param.reg)  # recursively includes reg. class params
    # Check for EnumParameters
    if isinstance(param, enum.EnumParameter):
        enumdict[param.enumclass.__name__] = param.enumclass
    elif isinstance(param, enum.ListOfEnumsParameter):
        for enumclass in param.enumclasses:
            enumdict[enumclass.__name__] = enumclass

def processRegClass(regclass):
    regclassdict[stripPtr(regclass.__name__)] = regclass
    for r in regclass.registry:
        for p in r.params:
            process_param(p)

# Registered (base) classes that need to be documented but for some
# reason aren't picked up by looping over menu items and their
# parameters should be identified by calling addRegisteredClass.  We
# don't immediately call processRegClass on them, because the registry
# might not be filled yet.

otherregclasses = []
def addRegisteredClass(regclass):
    otherregclasses.append(regclass)

##################
        
def regclassID(regclass):
    # xml id string to mark the definition of a base RegisteredClass
    return "RegisteredClass:%s" % stripPtr(regclass.__name__)
def registrationID(reg):
    return "RegisteredClass:%s" % stripPtr(reg.subclass.__name__)
def stripPtr(name):
    if name[-3:] == "Ptr":
        return name[:-3]
    return name

###################

# RegisteredClasses, Registrations, MenuItems, and Enums (and possibly
# other classes) have 'discussion' strings, which go into the xml
# manual.  If these strings are long, it's a pain to have them inside
# the source code (especially because editing xml in emacs's
# python-mode is a nuisance).  So those strings live in files in the
# MAN_OOF2 directory.  The xml menu dump command only works when OOF2
# is run in the MAN_OOF2 directory.  The loadFile function allows
# discussion strings stored in files to be associated with the
# appropriate objects without actually reading the files until
# xmlmenudump is run.  func is an optional function for processing the
# string in the file before inserting it into the xml.

def loadFile(filename, func=None):
    return DiscussionFile(filename, func)

class DiscussionFile:
    def __init__(self, filename=None, func=None):
        self.filename = filename
        self.func = func
    def read(self, obj):
        if self.filename:
            file = open(self.filename, 'r')
            text = file.read()
        else:
            text = None
        if self.func:
            return self.func(text, obj)
        return text

class DiscussionFunc:
    def __init__(self, func):
        # func is a function that returns a string or a DiscussionFile
        self.func = func
    def read(self, obj):
        return self.func(obj)

def getDiscussion(obj):
    ## Raises AttributeError if the object doesn't have a discussion
    ## or if its discussion isn't either a string or a DiscussionFile.
    if type(obj.discussion) is types.StringType:
        return obj.discussion
    return obj.discussion.read(obj)

def getHelp(obj):                       # get help, helpstr, or tip
    for helpattr in ("helpstr", "help", "tip"):
        try:
            help = getattr(obj, helpattr)
        except AttributeError:
            pass
        else:
            if type(help) is types.StringType:
                return help
            return help.read(obj)

##################    

# Keep track of other objects that need to be documented -- this
# includes anything except for RegisteredClasses, Enums, Outputs, and
# MenuItems. Every file that defines such objects must create an
# XMLObjectDoc object for each object type.  The 'discussion' argument
# should be a complete docbook refentry element or a DiscussionFile
# object containing a refentry.  The refentry id should be
# 'Object:name' where 'name' is the name of the object.

objDocs = labeltree.LabelTree()

class XMLObjectDoc:
    def __init__(self, name, discussion, ordering=0):
        self.name = name
        self.discussion = discussion
        objDocs.__setitem__(name, self, ordering)

# Other parts of the code that want to add a complete Section to the
# reference manual can register a callback here.  The callback will be
# called with a file argument.

otherSections = []

def addSection(callback, ordering):
    otherSections.append((ordering, callback))

###################

def dumpMenu(file, menu, toplevel):
    if menu.getOption('no_doc'):
        return
    path = menu.path()
    if not toplevel:
        print >> file, '<section xreflabel="%s" id="MenuItem:%s" role="Menu">' \
              % (path, path)
        print >> file, "<title>%s</title>" % path
    try:
        print >> file, "<subtitle>%s</subtitle>" % getHelp(menu)
    except AttributeError:
        pass
    try:
        print >> file, getDiscussion(menu)
    except AttributeError:
        pass

    if not toplevel:
        print >> file, \
              "<simpara>Parent Menu: <xref linkend='MenuItem:%s'/></simpara>" \
              % menu.parent.path()

    # Create an alphabetical list of menu items.  It's more convenient
    # to find things in alphabetical lists in the manual, even if
    # they're not presented alphabetically in the GUI.
    itemnames = [item.name for item in menu.items]
    itemnames.sort()

    print >> file, "<itemizedlist spacing='compact'>"
    print >> file, " <title>%s Menu Items</title>" % path
    for itemname in itemnames:
        item = menu.getItem(itemname)
        if not item.getOption('no_doc'):
            itempath = item.path()
            print >> file, " <listitem><simpara>"
            print >> file, "  <link linkend='MenuItem:%s'><command>%s</command></link>" \
                  % (itempath, itempath)
            try:
                help = getHelp(item)
                if help:
                    print >> file, "--", help
            except AttributeError:
                pass
            print >> file, " </simpara></listitem>"
    print >> file, "</itemizedlist>"

    if not toplevel:
        print >> file, "</section> <!-- %s -->" % path

    submenus = []
    commands = []
    for itemname in itemnames:
        item = menu.getItem(itemname)
        if not item.getOption('no_doc'):
            if item.items:
                submenus.append(item)
            else:
                commands.append(item)
    if submenus:
        for menu in submenus:
            dumpMenu(file, menu, toplevel=0)
    if commands:
        print >> file, "<section role='CommandListing'>"
        print >> file, "<title>%s Commands</title>" % path
        for command in commands:
            dumpMenuItem(file, command) # writes refentries
        print >> file, "</section> <!-- end of commands for %s -->" % path


def dumpMenuItem(file, menuitem):
    if menuitem.getOption('no_doc'):
        return
    path = menuitem.path()
    print >> file, '<refentry xreflabel="%s" id="MenuItem:%s" role="MenuItem">'\
          % (path, path)
    print >> file, " <refnamediv>"
    print >> file, "  <refname>%s</refname>" % path
    try:
        help = getHelp(menuitem)
        if help:
            print >> file, "  <refpurpose>%s</refpurpose>" % help
        else:
            print >> file, "   <refpurpose></refpurpose>"
    except AttributeError:
        print >> file, "  <refpurpose>MISSING HELP STRING: %s</refpurpose>" \
              % path
    print >> file, " </refnamediv>"

    menuitem.xmlSynopsis(file)

    print >> file, " <refsect1>"
    print >> file, "   <title>Details</title>"
    print >> file, "   <itemizedlist>"
    print >> file, "    <listitem><simpara>Parent Menu: <xref linkend='MenuItem:%s'/></simpara></listitem>" % menuitem.parent.path()
    if menuitem.callback:
        fname, mname = menuitem.getcallbackname()
        print >> file, "  <listitem><simpara>"
        print >> file, "   Callback: function <function>%s</function> in module <filename>%s</filename>" % (fname, mname)
        print >> file, "  </simpara></listitem>"
    print >> file, "  <listitem><simpara>"
    print >> file, "    Threadability: <constant>%s</constant>" % \
          menuitem.threadable
    print >> file, "  </simpara></listitem>"
    if menuitem.options:
        print >> file, "  <listitem><simpara>"
        print >> file, "   Options:"
        for key, val in menuitem.options.items():
            print >> file, " <varname>%s</varname>=<constant>%s</constant>" %(key, `val`)
        print >> file, "  </simpara></listitem>"

    menuitem.xmlParams(file)

    print >> file, "   </itemizedlist>"
    print >> file, " </refsect1>" # details section

    print >> file, " <refsect1>"
    print >> file, "  <title>Description</title>"
    try:
        print >> file, "  %s" % getDiscussion(menuitem)
    except AttributeError:
        print >> file, "  <para>MISSING DISCUSSION: %s</para>" % path
    print >> file, " </refsect1>"
    print >> file, "</refentry>"

###################        

def xmlmenudump(file):

    # Clear global dictionaries, in case this isn't the first time
    # this function has been run.
    global enumdict
    global regclassdict
    regclassdict = {}
    enumdict = {}

    print >> file, "<chapter id='Chapter:Reference'><title>Reference</title>"

    print >> file, """

    <section id="Section:Reference:HowTo">
      <title>How to use this Chapter</title>
      <para>
      
      This chapter consists of a set of reference pages for some of
      the important objects that appear in &oof2; scripts. Since all
      &oof2; operations can be scripted, these reference pages are the
      penultimate source for details on how everything works in
      &oof2;.<footnote><para>The ultimate source is the code itself,
      naturally.</para></footnote>
      </para>
      <para>
      Each &oof2; operation, and each line in an &oof2; script, is a
      single command from the &oof2; <link
      linkend='MenuItem:OOF'>menus</link>.  The menus are
      hierarchical, and the reference page for each menu item contains
      a link to page for its parent menu.
      <tip><para><emphasis>Read the parent
      page!</emphasis> Often it contains useful information that
      applies to all of the commands in the menu.</para></tip>
      </para>
      <para>
      The same advice applies to the pages for the <link
      linkend='Section:RegisteredClasses'><classname>RegisteredClass</classname></link>
      objects. A <classname>RegisteredClass</classname> <link
      linkend='Section:RegisteredBaseClasses'>base class</link>
      describes a <emphasis>category</emphasis> of object which is
      used as an argument in menu commands.  For example, a command
      that creates a boundary condition will have an argument whose
      value must be one of the members of the <xref
      linkend='RegisteredClass:BC'/> category.  Each base class
      contains many different <emphasis>subclasses</emphasis>,
      representing different varieties of things in the base class
      category.  For example, the <xref linkend='RegisteredClass:BC'/>
      class contains <xref linkend='RegisteredClass:DirichletBC'/> and
      <xref linkend='RegisteredClass:NeumannBC'/>, and other boundary
      condition types.  Each subclass has its own reference page,
      which contains a link to the base class's page.  Read both
      pages!  The base class page often contains important information
      relevant to all of the subclasses.
      </para>

    </section>

    """

    ## Add other sections defined elsewhere
    otherSections.sort()
    for ordering, otherSectionCB in otherSections:
        otherSectionCB(file)

    ########

    print >> file, "<section id='Section:OtherObjects'>"
    print >> file, " <title>Other Objects</title>"
    print >> file, """ <para>

    This section covers objects that can occur in &oof2; commands but
    aren't included in the above sections, for various reasons.

    </para>"""

    objDocs.apply2(function=printObjDocs, postfunc=postPrintObjDocs, file=file)
    print >> file, "</section>"         # end of other objects section


    print >> file, "</chapter>"

def mainMenuSection(file):
    # The section containing the main menu is handled differently from
    # all the other menus.  Its id is MenuItem:OOF so that
    # automatically generated references to root menu go to it.
    print >> file, "<section id='MenuItem:OOF' xreflabel='The Main OOF Menu'>"
    print >> file, "  <title>Menus</title>"

    from ooflib.common.IO import mainmenu      # delayed, to avoid import loop
    dumpMenu(file, mainmenu.OOF, toplevel=1)
    print >> file, "</section>"         # end of menu item listing

addSection(mainMenuSection, 0)

def regClassSection(file):
    ## RegisteredClasses

    for regclass in otherregclasses:
        processRegClass(regclass)
    
    print >> file, "<section id='Section:RegisteredClasses'>"
    print >> file, " <title>Registered Classes</title>"
    print >> file, """<para>

Many command arguments in &oof2; require the user to choose one of a
set of related objects.  These sets are called
<classname>RegisteredClasses</classname>, because the objects are
constructed from <classname>Registrations</classname>, stored in a
<classname>Registry</classname>, which provide the information needed
to create the objects.  All of that is completely irrelevant to you,
the &oof2; user, but helps to explain the title of this section.
</para>

<para> Section <xref linkend='Section:RegisteredBaseClasses'/> lists
the <classname>RegisteredClasses</classname> and the choices
(subclasses) available for each class.  Section <xref
linkend='Section:RegisteredSubclasses'/> describes the subclasses and
lists the parameters required to create the objects.  Some subclasses
may be members of more than one
<classname>RegisteredClass</classname>.

    </para>"""
    regclassnames = regclassdict.keys()
    regclassnames.sort()
    registrationdict = {}
    print >> file, "<section id='Section:RegisteredBaseClasses'>"
    print >> file, " <title>Base RegisteredClasses</title>"
    print >> file, " <itemizedlist spacing='compact'>"

    ## List of RegisteredClass base classes
    for regclassname in regclassnames:
        regclass = regclassdict[regclassname]
        try:
            tip = getHelp(regclass)
        except AttributeError:
            tip = "MISSING TIP STRING: %s" % regclassname
        print >> file, " <listitem><simpara>"
        print >> file, "  <xref linkend='%s'/> -- %s" % (regclassID(regclass),\
                                                         tip)
        print >> file, " </simpara></listitem>"        
    print >> file, " </itemizedlist>"

    ## Reference pages for each base class
    for regclassname in regclassnames:
        regclass = regclassdict[regclassname]
        print >> file, " <refentry xreflabel='%s' id='%s' role='RegisteredClass'>" % \
              (stripPtr(regclassname), regclassID(regclass))
        print >> file, "  <refnamediv>"
        print >> file, "   <refname>%s</refname>" % stripPtr(regclassname)
        try:
            tip = getHelp(regclass)
        except AttributeError:
            tip = "MISSING TIP STRING: %s" % regclassname
        print >> file, "   <refpurpose>%s</refpurpose>" % tip
        print >> file, "  </refnamediv>"
        print >> file, "  <refsect1>"
        print >> file, "   <title>Subclasses</title>"
        print >> file, """   <para>
        Subclasses are listed as they appear in the GUI and (in
        parentheses) as they appear in scripts.
        </para>"""
        print >> file, "   <itemizedlist spacing='compact'>"
        # Don't sort... registrations are listed in the order in which
        # they appear in the GUI.
        for reg in regclass.registry:
            registrationdict[reg.subclass.__name__] = reg
            try:
                tip = getHelp(reg)
            except AttributeError:
                tip = "MISSING TIP STRING: %s" % reg.subclass.__name__
            print >> file, "   <listitem><simpara>"
            print >> file, "    <link linkend='%s'>%s (<classname>%s</classname>)</link> -- %s" % \
                  (registrationID(reg), reg.name(), reg.subclass.__name__, tip)
            print >> file, "   </simpara></listitem>"
        print >> file, "   </itemizedlist>"        
        print >> file, "  </refsect1>"
        print >> file, "  <refsect1>"
        print >> file, "   <title>Description</title>"
        try:
            print >> file, "    %s" % getDiscussion(regclass)
        except AttributeError:
            print >> file, "<para>MISSING DISCUSSION: %s</para>" \
                  % stripPtr(regclassname)
        print >> file, "  </refsect1>"
        print >> file, " </refentry>"
    print >> file, "</section>"

    subclassnames = registrationdict.keys()
    subclassnames.sort()

    print >> file, "<section id='Section:RegisteredSubclasses'>"
    print >> file, " <title>Subclasses</title>"

    ## List of subclasses
    print >> file, " <itemizedlist spacing='compact'>"
    for name in subclassnames:
        reg = registrationdict[name]
        print >> file, "  <listitem><simpara>"
        try:
            tip = getHelp(reg)
        except AttributeError:
            tip = "MISSING TIP STRING: %s" % name
        print >> file, "    <xref linkend='%s'/> -- %s" % \
              (registrationID(reg), tip)
        print >> file, "  </simpara></listitem>"
    print >> file, " </itemizedlist>"

    ## Reference page for each subclass
    for name in subclassnames:
        reg = registrationdict[name]
        print >> file, " <refentry xreflabel='%s' id='%s' role='Registration'>"\
              % (name, registrationID(reg))
        print >> file, "  <refnamediv>"
        print >> file, "    <refname>%s (%s)</refname>" % (reg.name(), name)
        try:
            tip = getHelp(reg)
        except AttributeError:
            tip = "MISSING TIP STRING: %s" % name
        print >> file, "     <refpurpose>%s</refpurpose>" % tip
        print >> file, "  </refnamediv>"

        print >> file, "  <refsynopsisdiv><simpara>"
        args = string.join(['<varname>%s</varname>' % p.name
             for p in reg.params], ',')
        print >> file, "   <classname>%s</classname>(%s)" % (name, args)
        print >> file, "  </simpara></refsynopsisdiv>"
        
        print >> file, "  <refsect1>"
        print >> file, "    <title>Details</title>"
        print >> file, "    <itemizedlist>"
        print >> file, "     <listitem><simpara>"
        print >> file, "      Base class%s:"%("es"*(len(reg.registeredclasses)>1))
        for regclass in reg.registeredclasses:
            print >> file, "      <link linkend='%s'><classname>%s</classname></link>" \
            % (regclassID(regclass), regclass.__name__)
        print >> file, "     </simpara></listitem>"
        if reg.params:
            print >> file, "     <listitem><para>"
            print >> file, "      Parameters:"
            print >> file, "      <variablelist>"
            for param in reg.params:
                print >> file, "       <varlistentry>"
                print >> file, "        <term><varname>%s</varname></term>" \
                      % param.name
                print >> file, "         <listitem>"
                try:
                    tip = getHelp(param)
                except AttributeError:
                    tip = "MISSING TIP STRING: %s:%s" % (name, param.name)
                print >> file, "          <simpara>%s <emphasis>Type</emphasis>: %s</simpara>" \
                      % (tip, param.valueDesc())
                print >> file, "         </listitem>"
                print >> file, "       </varlistentry>"
            print >> file, "      </variablelist>" # end of parameter list
            print >> file, "     </para></listitem>"
        print >> file, "    </itemizedlist>" # end of Details list
        print >> file, "  </refsect1>" # end of Details section
        print >> file, "  <refsect1>"
        print >> file, "   <title>Description</title>"
        try:
            print >> file, "   %s" % getDiscussion(reg)
        except AttributeError:
            print >> file,     "<para>MISSING DISCUSSION: %s</para>" % name
        print >> file, "  </refsect1>"
        print >> file, " </refentry>"

    print >> file, "</section>"         # end of registered subclasses

    print >> file, "</section>"         # end of registered classes section

# This section has a large ordering value so that it comes *after* any
# section that calls process_param, ensuring that all RegisteredClass
# definitions have been found.

addSection(regClassSection, ordering=1000)

def enumSection(file):
    print >> file, "<section id='Section:Enums'>"
    print >> file, " <title>Enumerated Types</title>"
    print >> file, """ <para>

    Many command arguments in &oof2; require the user to choose from a
    small set of predetermined constant values, called
    <classname>Enums</classname>.  These <classname>Enums</classname>
    differ from <link
    linkend='Section:RegisteredClasses'><classname>RegisteredClasses</classname></link>
    in that they are much simpler objects, and never require any
    parameters.  This section describes all of the
    <classname>Enum</classname> classes and lists their allowed
    values.
    </para>

    <para>

     In the GUI, <classname>Enum</classname> parameters are chosen
     from a pull-down menu.  In scripts, <classname>Enum</classname>
     parameters can be set to the <emphasis>name</emphasis> of the
     <classname>Enum</classname> object, in quotation marks.
     For example, this documentation was generated by
     <blockquote><simpara><userinput>
       <link linkend='MenuItem:OOF.Help.API_Listing'>
        OOF.Help.API_Listing</link>(filename='oof2_api.xml',
        format=<link linkend='Enum:MenuDumpFormat'>'xml'</link>)
      </userinput></simpara></blockquote>
      Here, <varname>format</varname> is a parameter that requires an
      object from the <xref linkend='Enum:MenuDumpFormat'/> class.
    
    </para>"""

    enumnames = enumdict.keys()
    enumnames.sort()

    print >> file, "<itemizedlist spacing='compact'>"
    for enumname in enumnames:
        enumclass = enumdict[enumname]
        try:
            tip = getHelp(enumclass)
        except AttributeError:
            tip = "MISSING ENUM TIP STRING: %s" % enumname
        print >> file, "<listitem><simpara>"
        print >> file, " <xref linkend='Enum:%s'/> -- %s" % (enumname, tip)
        print >> file, "</simpara></listitem>"        
    print >> file, "</itemizedlist>"
    
    for enumname in enumnames:
        enumclass = enumdict[enumname]
        print >> file, " <refentry xreflabel='%s' id='Enum:%s' role='Enum'>" \
              % (enumname, enumname)
        print >> file, "  <refnamediv>"
        print >> file, "   <refname>%s</refname>" % enumname
        try:
            tip = getHelp(enumclass)
        except AttributeError:
            tip = "MISSING ENUM TIP STRING: %s" % enumname
        print >> file, "   <refpurpose>%s</refpurpose>" % tip
        print >> file, "  </refnamediv>"        

        print >> file, " <refsect1>"
        print >> file, "  <title>Description</title>"
        try:
            print >> file, "  %s" % getDiscussion(enumclass)
        except AttributeError:
            print >> file, "<para>MISSING ENUM DISCUSSION: %s</para>" % enumname
        print >> file, " </refsect1>"
        print >> file, " <refsect1>"
        print >> file, "  <title>Values</title>"
        print >> file, "  <itemizedlist spacing='compact'>"
        for name in enumclass.names:
            try:
                helpstr = ": " + enumclass.helpdict[name]
            except KeyError:
                helpstr = ""
            print >> file, "   <listitem><simpara>"
            print >> file, "   <userinput>%s</userinput>%s" % (name, helpstr)
            print >> file, "   </simpara></listitem>"
        print >> file, "  </itemizedlist>"
            
        print >> file, "  </refsect1>"
        print >> file, "</refentry>"
    print >> file, "</section>"         # end of enum section

# This section has a large ordering value so that it comes *after* any
# section that calls process_param, ensuring that all Enum definitions
# have been found.

addSection(enumSection, ordering=1001)

    
def printObjDocs(path, obj, file):
    if obj is not None:
        print >> file, getDiscussion(obj)
    else:
        # obj is None, meaning that this is a meta section.  Print toc.
        if path:                        # no path means we're at the top level
            print >> file, "<section id='Object:%s'>" % path
            print >> file, "  <title>%s</title>" % path
        print >> file, "  <itemizedlist spacing='compact'>"
        node = objDocs[path]
        for subnode in node.nodes:
            print >> file, "<listitem><simpara>"
            print >> file,  "<link linkend='Object:%(name)s'>%(name)s</link>" \
                  % {'name':subnode.name}
            print >> file, "</simpara></listitem>"
        print >> file, "  </itemizedlist>"

def postPrintObjDocs(path, obj, file):
    if obj is None:
        if path:
            print >> file, "</section> <!-- %s -->" % path

###############################

XMLObjectDoc('list', loadFile('DISCUSSIONS/common/object/list.xml'))
