# -*- python -*-
# $RCSfile: scheduledoutputmenu.py,v $
# $Revision: 1.5.4.2 $
# $Author: langer $
# $Date: 2014/05/08 14:39:02 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

## Menu items for manipulating scheduled outputs.

from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common.IO import automatic
from ooflib.common.IO import mainmenu
from ooflib.engine.IO import meshIO
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import whoville
from ooflib.common.IO import xmlmenudump
from ooflib.engine.IO import scheduledoutput
from ooflib.engine.IO import outputdestination
from ooflib.engine import outputschedule
import ooflib.engine.mesh
import ooflib.engine.IO.meshmenu # makes sure OOF.Mesh is defined first

outputmenu = mainmenu.OOF.Mesh.addItem(
    oofmenu.OOFMenuItem(
        'Scheduled_Output',
        help="Define output operations to be performed during time evolution calculations.",
        discussion=xmlmenudump.loadFile(
            "DISCUSSIONS/engine/menu/scheduledoutput.xml")))

outputIOmenu = meshIO.meshmenu.addItem(oofmenu.OOFMenuItem(
        'Scheduled_Output',
        help="Scheduled Output operations. Used internally in Mesh data files.",
        discussion='<para>Load <xref linkend="RegisteredClass-ScheduledOutput"/>s from a data file.</para>'
        ))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

def outputNameResolver(param, name):
    if param.automatic():
        output = param.group['output'].value
        basename = automatic.AutomaticName(output.defaultName())
    else:
        basename = name
    mesh = ooflib.engine.mesh.meshes[param.group['mesh'].value]
    return mesh.outputSchedule.uniqueName(basename)

def _newOutput(menuitem, mesh, name, output, scheduletype, schedule,
               destination):
    meshctxt = ooflib.engine.mesh.meshes[mesh]
    meshctxt.begin_writing()
    try:
        meshctxt.outputSchedule.add(name, output)
        output.setSchedule(schedule, scheduletype)
        output.setDestination(destination)
    finally:
        meshctxt.end_writing()
    switchboard.notify("new scheduled output", meshctxt, name)
    

outputmenu.addItem(oofmenu.OOFMenuItem(
    'New',
    callback=_newOutput,
    params=parameter.ParameterGroup(
            whoville.WhoParameter(
                'mesh', ooflib.engine.mesh.meshes,
                tip='Define an output operation on this mesh.'),
            parameter.AutomaticNameParameter(
                'name', resolver=outputNameResolver,
                value=automatic.automatic,
                tip="A name for the new output operation."),
            parameter.RegisteredParameter(
                'output',
                scheduledoutput.ScheduledOutput,
                tip="The output operation."))
    + parameter.ParameterGroup(
        parameter.RegisteredParameter(
            'scheduletype',
            outputschedule.ScheduleType,
            tip='How to interpret the schedule.'),
        outputschedule.OutputScheduleParameter(
            'schedule',
            tip="When to produce the output."))
    + parameter.ParameterGroup(
        outputdestination.OutputDestinationParameter(
            'destination',
            tip="Where the output should go.")),
    help="Create an output operation to be performed during a time evolution.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/newschedout.xml')
    ))

outputIOmenu.addItem(outputmenu.New.clone(
        discussion="<para>Used internally in data files.</para>"
))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

def _copyOutput(menuitem, mesh, source, targetmesh, copy):
    meshctxt = ooflib.engine.mesh.meshes[mesh]
    targetmeshctxt = ooflib.engine.mesh.meshes[targetmesh]
    targetmeshctxt.begin_writing()
    if mesh != targetmesh:
        meshctxt.begin_reading()
    try:
        output = meshctxt.outputSchedule.getByName(source).clone()
        targetmeshctxt.outputSchedule.add(copy, output)
    finally:
        targetmeshctxt.end_writing()
        if mesh != targetmesh:
            meshctxt.end_reading()
    switchboard.notify("scheduled outputs changed", targetmeshctxt)

def copyOutputnameResolver(param, name):
    if param.automatic():
        basename = param.group['source'].value
    else:
        basename = name
    mesh = ooflib.engine.mesh.meshes[param.group['targetmesh'].value]
    return mesh.outputSchedule.uniqueName(basename)

outputmenu.addItem(oofmenu.OOFMenuItem(
    'Copy',
    callback=_copyOutput,
    params=parameter.ParameterGroup(
            whoville.WhoParameter(
                'mesh', ooflib.engine.mesh.meshes,
                tip="Mesh containing the output to be copied."),
            scheduledoutput.ScheduledOutputParameter(
                'source',
                tip="The name of the output to be copied."),
            whoville.WhoParameter(
                'targetmesh', ooflib.engine.mesh.meshes,
                tip="The mesh to which the output should be copied."),
            parameter.AutomaticNameParameter(
                'copy', resolver=copyOutputnameResolver,
                value=automatic.automatic,
                tip="The name to be given to the copied output.")),
    help="Copy an output operation and its schedule and destination.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/copyschedout.xml')
    ))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

def _editOutput(menuitem, mesh, output, new_output,
                new_scheduletype, new_schedule, new_destination):
    meshctxt = ooflib.engine.mesh.meshes[mesh]
    meshctxt.begin_writing()
    try:
        meshctxt.outputSchedule.replace(output, new_output, new_scheduletype,
                                        new_schedule, new_destination)
    finally:
        meshctxt.end_writing()
    switchboard.notify("scheduled outputs changed", meshctxt)

outputmenu.addItem(oofmenu.OOFMenuItem(
    'Edit',
    callback=_editOutput,
    params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString),
            scheduledoutput.ScheduledOutputParameter(
                'output',
                tip='Name of the output being replaced'),
            parameter.RegisteredParameter(
                'new_output', scheduledoutput.ScheduledOutput,
                tip="A new output object."),
            parameter.RegisteredParameter(
                'new_scheduletype',
                outputschedule.ScheduleType,
                tip="How to interpret the schedule."),
            outputschedule.OutputScheduleParameter(
                'new_schedule',
                tip="When to produce the output."),
            outputdestination.OutputDestinationParameter(
                'new_destination',
                tip="Where the output should go.")
            ],
    help="Replace an existing output operation, keeping the same schedule and destination.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/editschedout.xml')
))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

def outputRenameResolver(param, name):
    mesh = ooflib.engine.mesh.meshes[param.group['mesh'].value]
    if param.automatic():
        output = mesh.outputSchedule.getByName(param.group['output'].value)
        basename = automatic.AutomaticName(output.defaultName())
    else:
        basename = name
    return mesh.outputSchedule.uniqueName(basename)

def _renameOutput(menuitem, mesh, output, name):
    meshctxt = ooflib.engine.mesh.meshes[mesh]
    meshctxt.begin_writing()
    try:
        meshctxt.outputSchedule.rename(output, name)
    finally:
        meshctxt.end_writing()
    switchboard.notify("scheduled outputs changed", meshctxt)

outputmenu.addItem(oofmenu.OOFMenuItem(
    'Rename',
    callback=_renameOutput,
    params=parameter.ParameterGroup(
            whoville.WhoParameter(
                'mesh', ooflib.engine.mesh.meshes,
                tip=parameter.emptyTipString),
            scheduledoutput.ScheduledOutputParameter(
                'output',
                tip='Old name of an output.'),
            parameter.AutomaticNameParameter(
                'name', resolver=outputRenameResolver,
                value=automatic.automatic,
                tip='New name for the output.')),
    help="Rename an existing scheduled output operation.",
    discussion=
"""<para>Give a new name to a <link
linkend="Section-Concepts-Outputs-Scheduled">Scheduled
Output</link>.</para>"""
    ))
    
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

def _deleteOutput(menuitem, mesh, output):
    meshctxt = ooflib.engine.mesh.meshes[mesh]
    meshctxt.begin_writing()
    try:
        meshctxt.outputSchedule.remove(output)
    finally:
        meshctxt.end_writing()
    switchboard.notify("scheduled outputs changed", meshctxt)

outputmenu.addItem(oofmenu.OOFMenuItem(
    'Delete',
    callback=_deleteOutput,
    params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString),
            scheduledoutput.ScheduledOutputParameter(
            'output', tip='Name of the output to delete.')
            ],
    help="Delete a scheduled output operation.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/delschedout.xml')
    ))

def _deleteAllOutputs(menuitem, mesh):
    meshctxt = ooflib.engine.mesh.meshes[mesh]
    meshctxt.begin_writing()
    try:
        meshctxt.outputSchedule.removeAll()
    finally:
        meshctxt.end_writing()
    switchboard.notify("scheduled outputs changed", meshctxt)

outputmenu.addItem(oofmenu.OOFMenuItem(
    'DeleteAll',
    callback=_deleteAllOutputs,
    params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString),
            ],
    help="Delete all scheduled output operations.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/menu/delallschedout.xml')
    ))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

def _rewindDestination(menuitem, mesh, output):
    meshctxt = ooflib.engine.mesh.meshes[mesh]
    meshctxt.begin_writing()
    try:
        destination = meshctxt.outputSchedule.getByName(output).destination
        if destination is not None:
            destination.rewind()
    finally:
        meshctxt.end_writing()

outputmenu.addItem(oofmenu.OOFMenuItem(
    'Rewind',
    callback=_rewindDestination,
    params=[
            whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString),
            scheduledoutput.ScheduledOutputParameter(
                'output',
                tip='Name of the output whose destination is being rewound.')
            ],
    help="Rewind the destination file for the given output.",
    discussion=xmlmenudump.loadFile(
            'DISCUSSIONS/engine/menu/rewscheduleddest.xml')
    ))

def _rewindDestinations(menuitem, mesh):
    meshctxt = ooflib.engine.mesh.meshes[mesh]
    meshctxt.begin_writing()
    try:
        for output in meshctxt.outputSchedule.outputs:
            if output.destination is not None:
                output.destination.rewind()
    finally:
        meshctxt.end_writing()

outputmenu.addItem(oofmenu.OOFMenuItem(
    'RewindAll',
    callback=_rewindDestinations,
    params=[
            whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString)
            ],
    help="Rewind all output destinations.",
    discussion=xmlmenudump.loadFile(
            'DISCUSSIONS/engine/menu/rewalldests.xml')
    ))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

def _enableOutput(menuitem, mesh, output, enable):
    meshctxt = ooflib.engine.mesh.meshes[mesh]
    meshctxt.begin_writing()
    try:
        meshctxt.outputSchedule.getByName(output).activate(enable)
    finally:
        meshctxt.end_writing()
    switchboard.notify("scheduled outputs changed", meshctxt)

outputmenu.addItem(oofmenu.OOFMenuItem(
    'Enable',
    callback=_enableOutput,
    params=[
        whoville.WhoParameter(
                'mesh', ooflib.engine.mesh.meshes,
                tip=parameter.emptyTipString),
        scheduledoutput.ScheduledOutputParameter(
                'output', tip='Name of the output.'),
        parameter.BooleanParameter(
                'enable', value=True, default=True,
                tip='True if output is enabled, false otherwise.')],
    help="Enable or disable a scheduled output operation.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/enableout.xml')
    ))

