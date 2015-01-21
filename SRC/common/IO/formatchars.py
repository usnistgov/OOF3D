# -*- python -*-
# $RCSfile: formatchars.py,v $
# $Revision: 1.1.6.2 $
# $Author: langer $
# $Date: 2014/08/01 17:38:00 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Settable parameters controlling the output format

from ooflib.common import enum
from ooflib.common.IO import mainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter

settingsmenu = mainmenu.OOF.Settings.addItem(oofmenu.OOFMenuItem(
    'Output_Formatting',
    help="Formatting options for post-processing analysis output."))

# The menuitems just set the parameter values, so they just have a
# dummy callback function.

def _dummy(*args, **kwargs):
    pass

class Separator(enum.EnumClass("space", "comma", "tab")):
    tip="Characters used between columns in output files."
    discussion="""<para>
    The commands in the <xref linkend='MenuItem:OOF.Mesh.Analyze'/>
    menu write columns of data to output files.  The commands have a
    <varname>separator</varname> argument that sets the character that
    divides one column of data from the next.  The
    <classname>Separator</classname> contains all of the allowed
    separators.
    </para>"""

_separator_strings = {
    Separator("space") : " ",
    Separator("comma") : ", ",
    Separator("tab") : "\t"}

separator_param = enum.EnumParameter(
    'separator', Separator,
    'comma', default='comma',
    tip="The character to appear between columns in output.")

def getSeparator():
    return _separator_strings[separator_param.value]

settingsmenu.addItem(oofmenu.OOFMenuItem(
    'Separator',
    callback=_dummy,
    params=[separator_param],
    help="Set the character to appear between columns in output files."
))



comment_char_param = parameter.StringParameter(
    "comment_character", "#", default="#",
    tip="The string used to mark comments in output files.")

def getCommentChar():
    return comment_char_param.value

settingsmenu.addItem(oofmenu.OOFMenuItem(
    'Comment_Character',
    callback=_dummy,
    params=[comment_char_param],
    help="Set the string used to mark comments in output files."
))
