# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from generics import *

def _getStatusText():
    textviewer = gtklogger.findWidget('OOF3D:FE Mesh Page:Pane:MeshInfo:info')
    buffer = textviewer.get_buffer()
    return buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter())
    
def FEMeshPageInfoCheck(status=None, nodes=None, elements=None):
    if status is None:
      return _getStatusText() == "No mesh!"
    else:
      return _getStatusText() == "Status: %s\n\
No. of Nodes:	%s\n\
No. of Elements: 	%d\n\
Tetrahedron element:	TET4_4 (%d)\n\
Quadrilateral element:	Q4_4 (0)\n\
Triangle element:	T3_3 (0)\n\
Line element:	D2_2 (0)\n\
Time:	0.0\n\
Data Cache Type: Memory\n\
Data Cache Size: 0 time steps\n" % (status, nodes, elements, elements)

def subproblemsCheck(names):
    return names == [x.name() for x in treeViewColValues('OOF3D:FE Mesh Page:Pane:Subproblems:SubproblemScroll:SubproblemList', 0)]

def subproblemsSelectedCheck(name):
    return name == treeViewSelectCheck('OOF3D:FE Mesh Page:Pane:Subproblems:SubproblemScroll:SubproblemList', 0).name()

def FEMeshPageCheck1():
    return sensitizationCheck({ 'New':1,
				'Rename':0,
				'Copy':0,
				'Delete':0,
				'Save':0
				},
			       base='OOF3D:FE Mesh Page')
		
def FEMeshPageCheck2():
    return sensitizationCheck({ 'New':1,
				'Rename':1,
				'Copy':1,
				'Delete':1,
				'Save':1
				},
			       base='OOF3D:FE Mesh Page')
			       
def FEMeshPageSubproblemsCheck0():
    return sensitizationCheck({ 'Pane:Subproblems:New':0,
				'Pane:Subproblems:Rename':0,
				'Pane:Subproblems:Edit':0,
				'Pane:Subproblems:Copy':0,
				'Pane:Subproblems:Info':0,
				'Pane:Subproblems:Delete':0
				},
			       base='OOF3D:FE Mesh Page')
			       
def FEMeshPageSubproblemsCheck1():
    return sensitizationCheck({ 'Pane:Subproblems:New':1,
				'Pane:Subproblems:Rename':0,
				'Pane:Subproblems:Edit':0,
				'Pane:Subproblems:Copy':0,
				'Pane:Subproblems:Info':0,
				'Pane:Subproblems:Delete':0
				},
			       base='OOF3D:FE Mesh Page')
			       
def FEMeshPageOperationsCheck0():
    return sensitizationCheck({ 'Pane:ElementOps:Method':1,
				'Pane:ElementOps:Prev':0,
				'Pane:ElementOps:OK':0,
				'Pane:ElementOps:Next':0
				},
			       base='OOF3D:FE Mesh Page')
			       
def FEMeshPageOperationsCheck1():
    return sensitizationCheck({ 'Pane:ElementOps:Method':1,
				'Pane:ElementOps:Prev':0,
				'Pane:ElementOps:OK':1,
				'Pane:ElementOps:Next':0
				},
			       base='OOF3D:FE Mesh Page')
    
def MeshNewDialogCheck0():
    okbutton = gtklogger.findWidget('Dialog-Create a new mesh:gtk-ok')
    return ((okbutton.get_property('sensitive') == True) and
           chooserCheck('Dialog-Create a new mesh:element_types:Map', ('1','2',)) and
           chooserCheck('Dialog-Create a new mesh:element_types:Func', ('1','2',)) and
           chooserCheck('Dialog-Create a new mesh:element_types:Tetrahedron element', ('TET4_4',)) and
           chooserCheck('Dialog-Create a new mesh:element_types:Quadrilateral element', ('Q4_4',)) and
           chooserCheck('Dialog-Create a new mesh:element_types:Triangle element', ('T3_3',)) and
           chooserCheck('Dialog-Create a new mesh:element_types:Line element', ('D2_2',)))
           
def MeshSubproblemNewDialogCheck0(*subproblems):
    okbutton = gtklogger.findWidget('Dialog-Create a new subproblem:gtk-ok')
    return ((okbutton.get_property('sensitive') == True) and
           chooserCheck('Dialog-Create a new subproblem:subproblem:Chooser', subproblems))

def MeshSubproblemNewDialogCheck1(*subproblems):
    okbutton = gtklogger.findWidget('Dialog-Create a new subproblem:gtk-ok')
    return ((okbutton.get_property('sensitive') == False) and
           chooserCheck('Dialog-Create a new subproblem:subproblem:Chooser', subproblems))

def MeshSubproblemNewDialogSelectEntireMesh0():
    okbutton = gtklogger.findWidget('Dialog-Create a new subproblem:gtk-ok')
    return ((okbutton.get_property('sensitive') == True) and
           chooserStateCheck('Dialog-Create a new subproblem:subproblem:Chooser', 'EntireMesh'))
           
def MeshSubproblemNewDialogSelectEntireMesh1():
    okbutton = gtklogger.findWidget('Dialog-Create a new subproblem:gtk-ok')
    return ((okbutton.get_property('sensitive') == False) and
           chooserStateCheck('Dialog-Create a new subproblem:subproblem:Chooser', 'EntireMesh'))
           
def MeshSubproblemNewDialogSelectMaterial0(selected):
    okbutton = gtklogger.findWidget('Dialog-Create a new subproblem:gtk-ok')
    return ((okbutton.get_property('sensitive') == True) and
           chooserStateCheck('Dialog-Create a new subproblem:subproblem:Material:material', selected))
           
def MeshSubproblemNewDialogSelect1():
    okbutton = gtklogger.findWidget('Dialog-Create a new subproblem:gtk-ok')
    return ((okbutton.get_property('sensitive') == False))        
           
def MeshSubproblemNewDialogSelectGroup0(selected):
    okbutton = gtklogger.findWidget('Dialog-Create a new subproblem:gtk-ok')
    return ((okbutton.get_property('sensitive') == True) and
           chooserStateCheck('Dialog-Create a new subproblem:subproblem:VoxelGroup:group', selected))
           
           
def MeshSubproblemNewDialogSelectUnion0(one, another):
    okbutton = gtklogger.findWidget('Dialog-Create a new subproblem:gtk-ok')
    return ((okbutton.get_property('sensitive') == True) and
           chooserStateCheck('Dialog-Create a new subproblem:subproblem:Union:one', one) and
           chooserStateCheck('Dialog-Create a new subproblem:subproblem:Union:another', another))

def MeshSubproblemNewDialogSelectIntersection0(one, another):
    okbutton = gtklogger.findWidget('Dialog-Create a new subproblem:gtk-ok')
    return ((okbutton.get_property('sensitive') == True) and
           chooserStateCheck('Dialog-Create a new subproblem:subproblem:Intersection:one', one) and
           chooserStateCheck('Dialog-Create a new subproblem:subproblem:Intersection:another', another))
           
def MeshSubproblemNewDialogSelectXor0(one, another):
    okbutton = gtklogger.findWidget('Dialog-Create a new subproblem:gtk-ok')
    return ((okbutton.get_property('sensitive') == True) and
           chooserStateCheck('Dialog-Create a new subproblem:subproblem:Xor:one', one) and
           chooserStateCheck('Dialog-Create a new subproblem:subproblem:Xor:another', another))
           
def MeshSubproblemNewDialogSelectComplement0(selected):
    okbutton = gtklogger.findWidget('Dialog-Create a new subproblem:gtk-ok')
    return ((okbutton.get_property('sensitive') == True) and
           chooserStateCheck('Dialog-Create a new subproblem:subproblem:Complement:complement_of', selected))
           
def MeshSubproblemEditDialogSelectEntireMesh0():
    okbutton = gtklogger.findWidget('Dialog-Edit Subproblem definition:gtk-ok')
    return ((okbutton.get_property('sensitive') == True) and
           chooserStateCheck('Dialog-Edit Subproblem definition:subproblem:Chooser', 'EntireMesh'))
           
def MeshSubproblemEditDialogSelectEntireMesh1():
    okbutton = gtklogger.findWidget('Dialog-Edit Subproblem definition:gtk-ok')
    return ((okbutton.get_property('sensitive') == False) and
           chooserStateCheck('Dialog-Edit Subproblem definition:subproblem:Chooser', 'EntireMesh'))
