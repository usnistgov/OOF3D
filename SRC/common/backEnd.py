# -*- python -*-
# $RCSfile: backEnd.py,v $
# $Revision: 1.13.18.1 $
# $Author: langer $
# $Date: 2014/09/27 22:33:46 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 
import sys
from ooflib.common import debug
from ooflib.common import utils
from ooflib.common.IO import mainmenu
from ooflib.common.IO import menuparser
from ooflib.common.IO import parallelmainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO import socket2me

import ooflib.common.initialize
import ooflib.engine.initialize
import ooflib.image.initialize


def back_end():
    ## debug.fmsg()
    ## listen to messages from front end
    message_source = socket2me.getSocketInput() ## assumes already initialized
    parser = menuparser.MenuParser(message_source, mainmenu.OOF.LoadData, menuparser.MenuParser.mode_binary)
    parser.run() ## executes messages passed from the front-end through an message_source object
    
