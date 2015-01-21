# -*- python -*-
# $RCSfile: boundarymenu.py,v $
# $Revision: 1.31.12.1 $
# $Author: langer $
# $Date: 2013/11/08 20:44:57 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Builds the boundary menu from the registrations in the
# BoundaryModifier class.


from ooflib.engine import boundarybuilder
from ooflib.engine import boundarymodifier
from ooflib.engine import skeletoncontext
from ooflib.engine.IO import skeletonmenu
from ooflib.engine.IO import skeletongroupparams
from ooflib.common import debug
from ooflib.common import utils
from ooflib.common.IO import oofmenu
from ooflib.common.IO import mainmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import xmlmenudump
from ooflib.SWIG.common import switchboard
import types



boundarymenu = skeletonmenu.skeletonmenu.addItem(mainmenu.OOFMenuItem(
    'Boundary',
    cli_only=1,
    help='Tools for creating and manipulating Skeleton boundaries.',
    discussion="""<para>
    The <command>OOF.Skeleton.Boundary</command> menu contains tools
    for creating and modifying &skel; <link
    linkend='Section:Concepts:Skeleton:Boundary'> boundaries</link>.
    The tools for creating and manipulating &mesh; <link
    linkend='Section:Concepts:Mesh:BoundaryCondition'><emphasis>boundary
    conditions</emphasis></link> are in <xref
    linkend='MenuItem:OOF.Mesh.Boundary_Conditions'/>.
    </para>"""
    ))

####  Boundary deletion.

def _deleteCB(menuitem, skeleton, boundary):
    skelctxt = skeletoncontext.skeletonContexts[skeleton]
    skelctxt.removeBoundary(boundary)

boundarymenu.addItem(oofmenu.OOFMenuItem(
    "Delete",
    callback=_deleteCB,
    help="Delete a boundary from a Skeleton.",
    params=[boundarybuilder.skeletonparam,
            skeletongroupparams.SkeletonBoundaryParameter('boundary',
                                                  tip="Boundary to be removed.")
            ],
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/boundary_delete.xml')
    ))

### Boundary renaming

def _renameCB(menuitem, skeleton, boundary, name):
    skelctxt = skeletoncontext.skeletonContexts[skeleton]
    skelctxt.renameBoundary(boundary, name)

boundarymenu.addItem(oofmenu.OOFMenuItem(
    "Rename",
    callback=_renameCB,
    help="Rename a Skeleton boundary.",
    params=[boundarybuilder.skeletonparam,
            skeletongroupparams.SkeletonBoundaryParameter('boundary',
                                                  tip="Boundary to be renamed."),
            parameter.StringParameter('name', tip="New name.")],
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/boundary_rename.xml')
    ))

### Boundary construction, very important...

def _constructCB(menuitem, skeleton, name, constructor):
    skelctxt = skeletoncontext.skeletonContexts[skeleton]
    constructor(skelctxt, name)

#Uniqueness of boundary names is built into boundarybuilder.nameparam
boundarymenu.addItem(oofmenu.OOFMenuItem(
    "Construct",
    callback=_constructCB,
    help="Construct a new boundary in a skeleton and in the associated meshes.",
    params = [boundarybuilder.skeletonparam,
              boundarybuilder.nameparam,
              parameter.RegisteredParameter("constructor",
                                            boundarybuilder.BoundaryConstructor,
                                            tip="Which method to use.")
              ],
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/boundary_construct.xml')))

### Boundary modification.

def _modifyCB(self, skeleton, boundary, modifier):
    skelctxt = skeletoncontext.skeletonContexts[skeleton]
    modifier(skelctxt, boundary)
    switchboard.notify("redraw")

boundarymenu.addItem(oofmenu.OOFMenuItem(
    "Modify",
    callback=_modifyCB,
    help="Add or remove nodes or edges from a boundary.",
    params=[boundarybuilder.skeletonparam,
            skeletongroupparams.SkeletonBoundaryParameter('boundary',
                                               tip="Boundary to be modified."),
            boundarymodifier.BoundaryModifierParameter('modifier',
                                                  tip=parameter.emptyTipString)
            ],
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/boundary_modify.xml')
    ))
            
