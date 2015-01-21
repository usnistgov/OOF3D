# -*- python -*-
# $RCSfile: analyzemenu.py,v $
# $Revision: 1.40.2.10 $
# $Author: langer $
# $Date: 2014/11/05 16:54:36 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 


from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import enum
from ooflib.common import parallel_enable
from ooflib.common import utils
from ooflib.common.IO import automatic
from ooflib.common.IO import datafile
from ooflib.common.IO import filenameparam
from ooflib.common.IO import mainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import placeholder
from ooflib.common.IO import reporter
from ooflib.common.IO import whoville
from ooflib.common.IO import xmlmenudump
from ooflib.engine import analysisdomain
from ooflib.engine import analysissample
from ooflib.engine import namedanalysis
from ooflib.engine.IO import analyze
from ooflib.engine.IO import meshparameters
from ooflib.engine.IO import output
from ooflib.engine.IO import outputdestination
import ooflib.engine.mesh
import sys

ops_menu = oofmenu.OOFMenuItem(
    "Analyze",
    secret=1,
    help="Compute properties of the solution.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/analyze.xml'))

mainmenu.OOF.Mesh.addItem(ops_menu)

## OOF.LoadData.IPC.Analyze
if parallel_enable.enabled():
    from ooflib.common.IO import parallelmainmenu
    ipcops_menu = parallelmainmenu.ipcmenu.addItem(
        oofmenu.OOFMenuItem('Analyze', secret=1, no_log=1)
        )

# Parameters to all the menu items.

mesh_param =  whoville.WhoParameter(
    'mesh', ooflib.engine.mesh.meshes,
    tip="The mesh on which to compute the output")

time_param = placeholder.TimeParameter(
    'time', tip='Time at which to perform the analysis.')

output_param = output.ValueOutputParameter(
    'data', tip="The output data source.")

domain_param = parameter.RegisteredParameter(
    'domain', analysisdomain.Domain,
    tip="Where on the mesh to compute the data.")

sample_param = parameter.RegisteredParameter(
    'sampling', analysissample.SampleSet,
    tip="How to sample the domain.")

destination_param = outputdestination.OutputDestinationParameter(
    'destination',
    value=outputdestination.msgWindowOutputDestination,
    tip='Where the data should be written.')

common_analysis_params = [mesh_param,
                          time_param,
                          output_param, 
                          domain_param,
                          sample_param,
                          destination_param]

def printHeaders(destination, operation, data, domain, sampling):
    destination.comment("Operation:", operation.shortrepr())
    destination.comment("Output:", data.shortrepr())
    destination.comment("Domain:", domain.shortrepr())
    destination.comment("Sampling:", sampling.shortrepr())
    destination.comment("Columns:")
    for i, colname in enumerate(operation.columnNames(data, sampling)):
        destination.comment("%d."%(i+1), colname)
    

def _ops_callback(menuitem, mesh, time, data, domain, sampling, destination,
                  **kwargs):
    if parallel_enable.enabled():
        menuitem.ipcmenu(mesh=mesh,data=data,domain=domain,sampling=sampling,
                         destination=destination)
        return

    operation = menuitem.data()  # data is a DataOperation Registration 

    # Set the mesh in the domain, then run the operation.
    domain.set_mesh(mesh)

    domain.read_lock()          # acquires Mesh's read lock.
    try:
        # The domain has all the mesh data, so we don't have to pass that data.
        meshctxt = ooflib.engine.mesh.meshes[mesh]
        meshctxt.precompute_all_subproblems()
        t = meshctxt.getTime(time) # converts '<latest>' to time, if needed
        meshctxt.restoreCachedData(t)
        destination.open()
        try:
            if sampling.make_samples(domain):
                printHeaders(destination, operation, data, domain, sampling)
                # Do the calculation
                operation(t, data, domain, sampling, destination)
            else:
                reporter.warn("Analysis domain is empty! No output produced.")
        finally:
            meshctxt.releaseCachedData()
            destination.close()
    finally:
        domain.read_release()
        # domain holds a reference to the mesh, and since it's a
        # Parameter value, the command history holds a reference to
        # domain.  We need to clear the mesh reference so that the
        # mesh can be destroyed when everybody else is done with it.
        domain.set_mesh(None)
        sampling.clearSamples()

def _rewind(menuitem, filename):
    outputdestination.rewindStream(filename)

# def _ipcops_callback(menuitem, mesh, time, data, domain, sampling, destination,
#                      **kwargs):
#     # "destination" is a file name, or "automatic" -- use
#     # destinationparam.get_file to convert it to a file handle.
#     outfile = destinationparam.get_file(destination)

#     callable = menuitem.data()

#     # Then set the mesh in the domain, and run the operation.
#     domain.set_mesh(mesh)

#     domain.read_lock()
#     try:
#         # The domain has all the mesh data, so we don't have to pass that data.
#         meshctxt = ooflib.engine.mesh.meshes[mesh]
#         t = meshctxt.getTime(time)
#         callable(t, data, domain, sampling, outfile)
#         outfile.flush()
#     finally:
#         domain.read_release()
#         domain.set_mesh(None)

# Create a menu item for each registered object in the DataOperation
# class.
def makemenu(menu_base):
    menu_base.clearSubMenu()
    for r in analyze.DataOperation.registry:
        help = getattr(r, "tip", None)
        new_item = oofmenu.OOFMenuItem(
            utils.space2underscore(r.name()),
            callback = _ops_callback,
            params = common_analysis_params + r.params,
            help=help,
            discussion=r.discussion)
        new_item.data = r
        menu_base.addItem(new_item)
    ops_menu.addItem(oofmenu.OOFMenuItem(
        'Rewind',
        callback=_rewind,
        params=[filenameparam.FileNameParameter(
                'filename',
                tip='The name of the output file.')],
        help="Overwrite the data currently in an output file.",
        discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/rewind.xml')
        ))



if parallel_enable.enabled():
    def ipcmakemenu(menu_base,ipcmenu_base):
        menu_base.clearSubMenu()
        ipcmenu_base.clearSubMenu()
        for r in analyze.DataOperation.registry:
            try:
                help = r.tip
            except KeyError:
                help = None
            new_item = oofmenu.OOFMenuItem(
                utils.space2underscore(r.name()),
                callback = _ops_callback,
                params = common_analysis_params + r.params,
                help=help,
                discussion=r.discussion)
            new_ipcitem=ipcmenu_base.addItem(
                oofmenu.OOFMenuItem(
                utils.space2underscore(r.name()),
                callback = _ipcops_callback,
                threadable = oofmenu.PARALLEL_THREADABLE,
                params = common_analysis_params + r.params)
                )
            new_ipcitem.data=r
            # Introduce new data member into new_item (data),
            # corresponding to the ipc item that is to be called in
            # parallel
            new_item.ipcmenu=new_ipcitem
            new_item.data = r
            menu_base.addItem(new_item)
    ipcmakemenu(ops_menu,ipcops_menu)
    switchboard.requestCallback(analyze.DataOperation, ipcmakemenu,
                                ops_menu, ipcops_menu)
else:
    makemenu(ops_menu)
    switchboard.requestCallback(analyze.DataOperation, makemenu, ops_menu)

##############################

# Operations on Named Analyses, used in ScheduledOutputs

namedanalysismenu = mainmenu.OOF.addItem(oofmenu.OOFMenuItem(
        'Named_Analysis',
        help="Create analysis operations that can be saved and invoked by name",
        cli_only=1))

def _nameAnalysis(menuitem, name,  operation, data, domain, sampling):
    namedanalysis.NamedAnalysis(name, operation, data, domain, sampling)
    switchboard.notify("named analyses changed")

namedanalysismenu.addItem(oofmenu.OOFMenuItem(
    "Create",
    callback=_nameAnalysis,
    params=[parameter.AutomaticNameParameter(
                'name',
                resolver=namedanalysis.nameResolver,
                value=automatic.automatic,
                tip="The name of the analysis."),
            parameter.RegisteredParameter(
                'operation', analyze.DataOperation,
                tip="How to handle the data."),
            output_param,
            domain_param,
            sample_param],
    help="Assign a name to a set of analysis parameters.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/newnamedanal.xml')
))

# The data file command for loading a named analysis uses the same
# callback as the command for naming it.

mainmenu.OOF.LoadData.addItem(oofmenu.OOFMenuItem(
    'NamedAnalysis',
    callback=_nameAnalysis,
    params=[parameter.StringParameter('name',tip=parameter.emptyTipString),
            parameter.RegisteredParameter('operation', analyze.DataOperation,
                                          tip="The analysis operation."),
            output_param,
            domain_param,
            sample_param],
    help="Assign a name to a set of analysis parameters.  Used internally in data files.",
    discussion="<para>Create a Named Analysis.</para>"
))

def _deleteAnalysis(menuitem, name):
    namedanalysis.getNamedAnalysis(name).destroy()
    switchboard.notify("named analyses changed")

namedanalysismenu.addItem(oofmenu.OOFMenuItem(
    "Delete",
    callback=_deleteAnalysis,
    params=[namedanalysis.AnalysisNameParameter(
                'name', tip='Name of the analysis operation to delete.')],
    help="Delete a named set of analysis parameters.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/delnamedanal.xml')
    ))

def saveAnalysisDef(dfile, analysisname):
    analysis = namedanalysis.getNamedAnalysis(analysisname)
    dfile.startCmd(mainmenu.OOF.LoadData.NamedAnalysis)
    dfile.argument('name', analysisname)
    dfile.argument('operation', analysis.operation)
    dfile.argument('data', analysis.data)
    dfile.argument('domain', analysis.domain)
    dfile.argument('sampling', analysis.sampling)
    dfile.endCmd()

def _saveAnalysisDefs(menuitem, filename, mode, format, names):
    dfile = datafile.writeDataFile(filename, mode.string(), format)
    for analysisname in names:
        saveAnalysisDef(dfile, analysisname)
    dfile.close()

namedanalysismenu.addItem(oofmenu.OOFMenuItem(
    "SaveAnalysisDefs",
    callback=_saveAnalysisDefs,
    params=[
        filenameparam.WriteFileNameParameter('filename',
                                             tip='Name of the file.'),
        filenameparam.WriteModeParameter(
                'mode', tip="'w' to (over)write, 'a' to append."),
        enum.EnumParameter('format', datafile.DataFileFormat, datafile.ASCII,
                           tip="Format of the file."),
        namedanalysis.AnalysisNamesParameter('names',
                               tip="Names of the analyses to be saved.")],
    help="Save the definitions of named analysis operations to a file.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/saveanal.xml')
    ))

