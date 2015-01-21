# -*- python -*-
# $RCSfile: words.py,v $
# $Revision: 1.17.2.3 $
# $Author: langer $
# $Date: 2014/09/19 20:36:29 $


# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.common import utils
from ooflib.common.IO import oofmenu
from ooflib.common.IO import mainmenu
import string
import sys

words = {}

words['Credits'] = """
OOF3D was written at the National Institute of Standards and Technology in Gaithersburg, Maryland, USA, by Valerie R. Coffman, Stephen A. Langer, Andrew C.E. Reid, Yannick Congo, Gunay Dogan, and Lucianna Kiffer.

OOF3D includes a lot of code from OOF2.  Contributors have included R. Edwin Garcia, Rhonald C. Lua, Seung-Ill Haan, and Eric Ma.

OOF2 is a product of the NIST Information Technology Laboratory and the Center for Theoretical and Computational Materials Science in the NIST Material Measurement Laboratory.

Thanks to Ed Fuller, W. Craig Carter, Panos Charalambides, Zi-Kui Liu, and Andy Roosen for their support.

OOF3D incorporates software written elsewhere, which is listed in the Copyright section.  We are grateful to the authors of those programs and libraries for making their work available.
"""

####################

words['Disclaimer'] = """
This software is provided by NIST as a public service. You may use, copy and distribute copies of the software in any medium, provided that you keep intact this entire notice. You may improve, modify and create derivative works of the software or any portion of the software, and you may copy and distribute such modifications or works. Modified works should carry a notice stating that you changed the software and should note the date and nature of any such change. Please explicitly acknowledge the National Institute of Standards and Technology as the source of the software.

The software is expressly provided "AS IS". NIST MAKES NO WARRANTY OF ANY KIND, EXPRESS, IMPLIED, IN FACT OR ARISING BY OPERATION OF LAW, INCLUDING, WITHOUT LIMITATION, THE IMPLIED WARRANTY OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, NON-INFRINGEMENT AND DATA ACCURACY. NIST NEITHER REPRESENTS NOR WARRANTS THAT THE OPERATION OF THE SOFTWARE WILL BE UNINTERRUPTED OR ERROR-FREE, OR THAT ANY DEFECTS WILL BE CORRECTED. NIST DOES NOT WARRANT OR MAKE ANY REPRESENTATIONS REGARDING THE USE OF THE SOFTWARE OR THE RESULTS THEREOF, INCLUDING BUT NOT LIMITED TO THE CORRECTNESS, ACCURACY, RELIABILITY, OR USEFULNESS OF THE SOFTWARE.

You are solely responsible for determining the appropriateness of using and distributing the software and you assume all risks associated with its use, including but not limited to the risks and costs of program errors, compliance with applicable laws, damage to or loss of data, programs or equipment, and the unavailability or interruption of operation. This software is not intended to be used in any situation where a failure could cause risk of injury or damage to property. The software was developed by NIST employees. NIST employee contributions are not subject to copyright protection within the United States.
"""

####################

words['Copyright'] = """
OOF3D was produced by NIST, an agency of the U.S. government, and by statute is not subject to copyright in the United States.  However, to facilitate maintenance we ask that before distributing modified versions of this software, you first contact the authors at oof_manager@nist.gov.

-*- -*- -*- -*-

Programs and libraries written elsewhere and incorporated in OOF2 have their own copyright and licensing terms, which are summarized below.  For details, see the listed URLs, or (where applicable) the full copyright statements in the OOF source code distribution.

Python:  The Python programming language (http://www.python.org) copyright is held by the Python Software Foundation.  Python is freely redistributable.  Its license may be found at http://www.python.org/license.html.  OOF2 requires Python version 2.3 or later.

GTK+:  The GTK+ graphics toolkit (http://www.gtk.org) is licensed under the GNU LGPL (http://www.gnu.org/copyleft/lesser.html).  OOF2 currently requires GTK+ version 2.6 and libgnomecanvas2 version 2.6 or later.

VTK:  VTK (http://www.vtk.org) is an open-source toolkit licensed under the BSD license.

IML++ and SparseLib++:  The IML++ library of iterative matrix methods in C++ and the SparseLib++ library for sparse matrix computations are available from NIST at http://math.nist.gov/iml++/ and http://math.nist.gov/sparselib++/.  They are freely redistributable.

LAPACK:  The LAPACK linear algebra library is freely available at http://www.netlib.org/lapack/.  Its copyright terms are at http://www.netlib.org/lapack/faq.html#1.2.

"""

##############################

def _fancyprint(menuitem):
#    width = utils.screenwidth()
    width = 80
    print >> sys.stderr, string.join(utils.format(words[menuitem.data], width),
                                     "\n")

def xmlify(text):
    lines = text.split('\n')
    xmllines = []
    for line in lines:
        if line:
            xmllines.append("<para>" + line + "</para>")
    return string.join(xmllines, '\n')

for key in words.keys():
    help = key + " information."
    menuitem = mainmenu.OOF.addItem(oofmenu.OOFMenuItem(
        key,
        callback=_fancyprint,
        cli_only=1,
        help=help,
        discussion=xmlify(words[key])
        ))
    menuitem.data = key
