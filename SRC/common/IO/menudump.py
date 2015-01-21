# -*- python -*-
# $RCSfile: menudump.py,v $
# $Revision: 1.20.18.1 $
# $Author: langer $
# $Date: 2014/09/27 22:34:01 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.common import debug
from ooflib.common import enum
from ooflib.common import utils
from ooflib.common.IO import mainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
import string


indent =  "      "
indent2 = "           "

paramdict = {}                          # all parameter types that are used
regclassdict = {}                       # Every registered class we see.
enumdict = {}                           # All Enum types that are used

def textdumper(menuitem, file):
    if menuitem.items or menuitem.getOption('no_doc'):
        return                      # skip submenus, only do actual commands
    print >> file, menuitem.path()
    if menuitem.callback:
        funcname, modulename = menuitem.getcallbackname()
        print >> file, indent, "callback: Function '%s' in module '%s'" % \
              (funcname, modulename)
    if menuitem.helpstr:
        print >> file, indent, "help:", menuitem.helpstr
    else:
        print >> file, indent, "MISSING HELP STRING."
    if menuitem.secret:
        print >> file, indent, "secret:", menuitem.secret
    print >> file, indent, "threadability:", menuitem.threadable
    if menuitem.options:
        print >> file, indent, "options:",
        for key,val in menuitem.options.items():
            print >> file, key, "=", val,
        print >> file
    if menuitem.params:
        print >> file, indent, "Parameters:"
        for param in menuitem.params:
            tip = param.tip or "MISSING TIP"
            print >> file, indent2, "'%s'\t%s\t%s" \
                  %(param.name, param.classRepr(), tip)
            add_params(param)
    print >> file
            # v = param.valueRepr()
            # if v:
            #     paramdict[param.classRepr()] = v


# Recursively add parameters amd registered classes to the dictionaries.
def add_params(param):
    global enumdict
    global paramdict
    global regclassdict
    
    v = param.valueRepr()
    if v:
        paramdict[param.classRepr()] = param
    # Check for RegisteredParameters
    try:
        rlist = param.registry
    except AttributeError:
        pass
    else:
        for r in rlist:
            regclassdict[r.subclass.__name__] = r
            for p in r.params:
                add_params(p)
    # Check for EnumParameters
    if isinstance(param, enum.EnumParameter):
        enumdict[param.enumclass] = 1


def textmenudump(file):
    global paramdict
    global enumdict
    paramdict = {}
    enumdict = {}
    mainmenu.OOF.apply(textdumper, file)
    
    print >> file, "\n\n------------ Registered Classes -------------\n"
    rlist = regclassdict.items()
    rlist.sort()
    for rname, reg in rlist:
        basenames = [regclass.__name__ for regclass in reg.registeredclasses]
        print >> file, indent, rname, "(%s)"%string.join(basenames,",")
        if reg.tip:
            print >> file, indent, "tip:", reg.tip
        else:
            print >> file, indent, "MISSING TIP STRING."
        for p in reg.params:
            print >> file, indent2, "'%s'\t%s" % (p.name, p.classRepr())
        print >> file

    print >> file, "\n\n------------ Enum Classes ------------\n"
    elist = enumdict.keys()
    elist.sort()
    for enum in elist:
        print >> file, indent, enum.__name__
        for name in enum.names:
            try:
                helpstr = enum.helpdict[name]
                print >> file, indent2, name, ": ", helpstr
            except KeyError:
                print >> file, indent2, name, ": MISSING HELP STRING"
        print >> file

    print >> file, "\n\n------------ Parameter Classes ------------\n"
    plist = paramdict.items()
    plist.sort()
    for name, p in plist:
        print >> file, indent, name #, v
        if p.tip:
            print >> file, indent2, "tip:", p.tip
        else:
            print >> file, indent2, "MISSING TIP STRING"
        vlist = string.split(p.valueRepr(), '\n')
        for vv in vlist:
            print >> file, indent2, vv
        print >> file
    file.close()


########################

class MenuDumpFormat(enum.EnumClass("text", "xml")):
    tip = "File formats for the &oof2; API dump."
    discussion = """<para>
    <classname>MenuDumpFormat</classname> objects are used by <xref
    linkend='MenuItem:OOF.Help.API_Listing'/> to specify the output
    format.
    </para>"""

from ooflib.common.IO import xmlmenudump

def menudump(menuitem, filename, format):
    file = open(filename, 'w')
    if file:
        try:
            if format=="text":
                textmenudump(file)
            elif format=="xml":
                xmlmenudump.xmlmenudump(file)
        finally:
            file.close()

mainmenu.OOF.Help.addItem(oofmenu.OOFMenuItem(
    'API_Listing',
    callback=menudump,
    threadable = oofmenu.UNTHREADABLE,
    params=[
    parameter.StringParameter('filename', 'oof2_api.txt', tip="File name."),
    enum.EnumParameter('format', MenuDumpFormat, value="text",
                       tip="Format for the api listing, 'text' or 'xml'.")
    ],
    help="Create a verbose listing of all OOF menu commands.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/common/menu/api_listing.xml')
    ))
