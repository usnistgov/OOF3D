# -*- python -*-
# $RCSfile: analyze.py,v $
# $Revision: 1.69.4.12 $
# $Author: langer $
# $Date: 2014/08/01 17:38:01 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Objects for performing operations on data.  These include writing
# data to a file, taking averages and standard deviations, and so
# forth.  The data to which this should be done is specified by means
# of an output.

from ooflib.SWIG.common import ooferror
from ooflib.SWIG.engine import outputval
from ooflib.common import debug
#from ooflib.common import parallel_enable
from ooflib.common import registeredclass
from ooflib.common import utils
from ooflib.common.IO import formatchars
from ooflib.common.IO import oofmenu
from ooflib.common.IO import xmlmenudump
from ooflib.engine import analysissample
import math
import string
import types

## TODO 3.1: For direct output, it would be useful to have separate output
## files for each time step.  Perhaps if the output file name
## contained '%n', the '%n' could be replaced with the time step number.
## Or '%t' could be replaced with the time.


# Parent class for all "Data Operation" objects, i.e. things which do
# things to outputs, like writing them gridwise to files,
# evaluating them along cross-sections, and so forth.

# Data operation objects need to specify at registration time
# whether they are "direct" or not -- a "direct" operation is one
# for which the value of the output at a given sample is directly
# output to the user.  Statistical operations are not direct.

class DataOperation(registeredclass.RegisteredClass):
    registry = []
    tip='Post-processing data operations'
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/dataoperation.xml')

    def shortrepr(self):
        return self.getRegistration().name()

# When the DataOperation functions are called, the dofs in the mesh
# have already been set to the appropriate time.  The menu items (in
# analyzemenu.py and meshbdyanalysis.py) take care of setting the
# data.  The time value is passed through to these functions just so
# that it can be included in the output.

###############

# A DataOperation that prints its results on a single line in the
# output file.

class OneLineDataOperation(DataOperation):
    def columnNames(self, output, sampling):
        names = self.colNames(output)
        if showTime():
            return ["time"] + names
        return names

    def printResults(self, time, results, destination):
        if showTime():
            print >> destination, time, 
        for x in results:
            print >> destination, x,
        print >> destination

    def colNames(self, output):
        raise ooferror.ErrPyProgrammingError(
            "OneLineDataOperation subclass %s forgot to define colNames()" 
            % self.__class__.__name__)

################

settingsmenu = formatchars.settingsmenu

def showTime():
    return settingsmenu.Show_Time.value

def _dummy(*args, **kwargs):
    pass
    
settingsmenu.addItem(oofmenu.CheckOOFMenuItem(
    'Show_Time',
    value=True,
    callback=_dummy,
    help="Show or hide the time column in output files."
))
    
############################ MPI #########################################

## TODO 3.1: The MPI-enabled functions here have not been updated for
## doing time-dependent analysis.  They're commented out so that
## they're not mistaken for working code.

# if parallel_enable.enabled():
#     from ooflib.SWIG.common import mpitools
#     #Only frontend (rank 0) writes directly to destination
#     def _DirectOutput_call_frontend(output,domain,sampling,
#                                     destination):
#         otype = _ocheck(output)
        
#         header = sampling.get_col_names()
#         sampling.make_samples(domain)
#         sep_string = getSeparator()

#         # "olist" is a list of tuples of the form (sample, value).
#         olist = sampling.evaluate(domain, output, otype)
#         if otype == types.FloatType:
#             output_header = header + ["Value"]
#         else:
#             # Pull the label list from the first value of the first
#             # tuple in the list.
#             output_header = header + olist[0][1].label_list()

#         print >> destination, getCommentChar() + \
#               sep_string.join(output_header)

#         if otype == types.FloatType:
#             # For floating-point values, iterate over the list, and
#             # just use the repr of the (possibly multiple) values.

#             for (s,v) in olist:
#                 tags = s.columnData(header)
#                 if len(tags)==1:
#                     print >> destination, \
#                           sep_string.join(tags[0]+[`v`])
#                 else:
#                     for (tag, vstring) in zip(tags, [`val` for val in v]):
#                         print >> destination, \
#                               sep_string.join(tag+[vstring])
#         else: # otype == outputval.OutputValPtr
#             # For the OutputVal case, use value_list to get the
#             # list of floats, and join them up.
#             for (s,v) in olist:
#                 tags = s.columnData(header)
#                 if len(tags)==1:
#                     vlist = v.value_list()
#                     print >> destination, \
#                           sep_string.join(tags[0] + [`x` for x in vlist])
#                 else: # Multiple values -- do above for each tag-val pair.
#                     for (tag, val) in zip(tags, v):
#                         vlist = val.value_list()
#                         print >> destination, \
#                               sep_string.join(tag + [`x` for x in vlist])
#         #Get output from other processes
#         for proc in range(mpitools.Size()):
#             if proc!=0:
#                 print >> destination, "(From remote process %d:)" % proc
#                 print >> destination, mpitools.Recv_String(proc)
        
#     def _DirectOutput_call_backend(output,domain,sampling,
#                                    destination):
#         otype = _ocheck(output)
        
#         header = sampling.get_col_names()
#         sampling.make_samples(domain)
#         sep_string = getSeparator()

#         # "olist" is a list of tuples of the form (sample, value).
#         olist = sampling.evaluate(domain, output, otype)
#         if otype == types.FloatType:
#             output_header = header + ["Value"]
#         else:
#             # Pull the label list from the first value of the first
#             # tuple in the list.
#             output_header = header + olist[0][1].label_list()

#         #print >> destination, comment_character + \
#         #      string.join(output_header, sep_string)
#         outputstringlist=[getCommentChar() + sep_string.join(output_header)]
#         if otype == types.FloatType:
#             # For floating-point values, iterate over the list, and
#             # just use the repr of the (possibly multiple) values.

#             for (s,v) in olist:
#                 tags = s.columnData(header)
#                 if len(tags)==1:
#                     #print >> destination, \
#                     #      string.join(tags[0]+[`v`], sep_string)
#                     outputstringlist.append(
#                         sep_string.join(tags[0]+[`v`])
#                         )
#                 else:
#                     for (tag, vstring) in zip(tags, [`val` for val in v]):
#                         #print >> destination, \
#                         #      string.join(tag+[vstring], sep_string)
#                         outputstringlist.append(
#                             sep_string.join(tag+[vstring])
#                             )
#         else: # otype == outputval.OutputValPtr
#             # For the OutputVal case, use value_list to get the
#             # list of floats, and join them up.
#             for (s,v) in olist:
#                 tags = s.columnData(header)
#                 if len(tags)==1:
#                     vlist = v.value_list()
#                     #print >> destination, \
#                     #      string.join(tags[0] + [`x` for x in vlist],
#                     #                  sep_string)
#                     outputstringlist.append(
#                         sep_string.join(tags[0] + [`x` for x in vlist]))
#                 else: # Multiple values -- do above for each tag-val pair.
#                     for (tag, val) in zip(tags, v):
#                         vlist = val.value_list()
#                         #print >> destination, \
#                         #      string.join(tag + [`x` for x in vlist],
#                         #                  sep_string)
#                         outputstringlist.append(
#                             sep_string.join(tag + [`x` for x in vlist]))
#         #Send output to front end (process/rank 0)
#         mpitools.Send_String('\n'.join(outputstringlist),0)

#     def _AverageOutput_call_frontend(output, domain, sampling, destination):

#         otype = _ocheck(output)

#         if not sampling.make_samples(domain):
#             return                      # no samples!
#         integralsum = None
#         areasum = 0.0

#         # The following line relies on the fact that integrate does
#         # not evaluate its 'output' arg when power==0 and
#         # otype==FloatType.
#         for v in sampling.integrate(domain, None, types.FloatType, power=0):
#             areasum += v[1]

#         for v in sampling.integrate(domain, output, otype):
#             if integralsum is not None:
#                 integralsum += v[1]
#             else:
#                 integralsum = v[1]

#         result = integralsum/areasum

#         totalintegralsum=integralsum
#         totalareasum=areasum
#         if otype==types.FloatType:
#             print >> destination, getCommentChar() + " Value"
#             print >> destination, `result`
#             #Collect the result from remote processes
#             for proc in range(mpitools.Size()):
#                 if proc!=0:
#                     totalintegralsum+=mpitools.Recv_Double(proc)
#                     totalareasum+=mpitools.Recv_Double(proc)
#         else:
#             sep_string = getSeparator()
#             output_header = result.label_list()
#             print >> destination, getCommentChar() + \
#                 sep_string.join(output_header)
#             print >> destination, \
#                 sep_string.join([`x` for x in result.value_list()])
#         #Get output from other processes
#         for proc in range(mpitools.Size()):
#             if proc!=0:
#                 print >> destination, "(From remote process %d:)" % proc
#                 print >> destination, mpitools.Recv_String(proc)
#         print >> destination, "Average value over union of subdomains: %s" % \
#               `totalintegralsum/totalareasum`

#     def _AverageOutput_call_backend(output, domain, sampling, destination):

#         otype = _ocheck(output)

#         if not sampling.make_samples(domain):
#             return                      # no samples!
#         integralsum = None
#         areasum = 0.0

#         # The following line relies on the fact that integrate does
#         # not evaluate its 'output' arg when power==0 and
#         # otype==FloatType.
#         for v in sampling.integrate(domain, None, types.FloatType, power=0):
#             areasum += v[1]

#         for v in sampling.integrate(domain, output, otype):
#             if integralsum is not None:
#                 integralsum += v[1]
#             else:
#                 integralsum = v[1]

#         result = integralsum/areasum

#         outputstringlist=[]
#         if otype==types.FloatType:
#             outputstringlist.append(getCommentChar() + " Value")
#             outputstringlist.append(`result`)
#             mpitools.Send_Double(integralsum,0)
#             mpitools.Send_Double(areasum,0)
#         else:
#             sep_string = getSeparator()
#             output_header = result.label_list()
#             outputstringlist.append(getCommentChar() + 
#                                     sep_string.join(output_header))
#             outputstringlist.append(
#                 sep_string.join([`x` for x in result.value_list()]))
#         #Send output to front end (process/rank 0)
#         mpitools.Send_String('\n'.join(outputstringlist),0)

#     def _StdDevOutput_call_frontend(output, domain, sampling, destination):

#         otype = _ocheck(output)

#         if not sampling.make_samples(domain):
#             return
#         integralsum = None
#         areasum = 0.0
#         squaresum = None
#         # The following line relies on the fact that integrate does
#         # not evaluate its 'output' arg when power==0 and
#         # otype==FloatType.
#         for v in sampling.integrate(domain, None, types.FloatType, power=0):
#             areasum += v[1]
            
#         for v in sampling.integrate(domain, output, otype, power=1):
#             if integralsum is None:
#                 integralsum = v[1]
#             else:
#                 integralsum += v[1]

#         for v in sampling.integrate(domain, output, otype, power=2):
#             if squaresum is None:
#                 squaresum = v[1]
#             else:
#                 squaresum += v[1]


#         # Need different kinds of square roots depending on the
#         # output type.
#         if otype == types.FloatType:
#             result = math.sqrt( abs( (squaresum/areasum) -
#                                 (integralsum/areasum)**2 ) )
#             print >> destination, getCommentChar() + " Value"
#             print >> destination, `result`

#         elif otype == outputval.OutputValPtr:
#             avgsquared = (integralsum/areasum)
#             avgsquared.component_square()
#             squaredavg = (squaresum/areasum)
#             result = (squaredavg-avgsquared)
#             result.component_sqrt()

#             sep_string = getSeparator()
#             output_header = result.label_list()
#             print >> destination, getCommentChar() + \
#                 sep_string.join(output_header)
#             print >> destination, \
#                 sep_string.join([`x` for x in result.value_list()])
#         #Get output from other processes
#         for proc in range(mpitools.Size()):
#             if proc!=0:
#                 print >> destination, "(From remote process %d:)" % proc
#                 print >> destination, mpitools.Recv_String(proc)

#     def _StdDevOutput_call_backend(output, domain, sampling, destination):

#         otype = _ocheck(output)

#         if not sampling.make_samples(domain):
#             return
#         integralsum = None
#         areasum = 0.0
#         squaresum = None
#         # The following line relies on the fact that integrate does
#         # not evaluate its 'output' arg when power==0 and
#         # otype==FloatType.
#         for v in sampling.integrate(domain, None, types.FloatType, power=0):
#             areasum += v[1]
            
#         for v in sampling.integrate(domain, output, otype, power=1):
#             if integralsum is None:
#                 integralsum = v[1]
#             else:
#                 integralsum += v[1]

#         for v in sampling.integrate(domain, output, otype, power=2):
#             if squaresum is None:
#                 squaresum = v[1]
#             else:
#                 squaresum += v[1]

#         outputstringlist=[]
#         # Need different kinds of square roots depending on the
#         # output type.
#         if otype == types.FloatType:
#             result = math.sqrt( abs( (squaresum/areasum) -
#                                 (integralsum/areasum)**2 ) )
#             outputstringlist.append(getCommentChar() + " Value")
#             outputstringlist.append(`result`)
#         elif otype == outputval.OutputValPtr:
#             avgsquared = (integralsum/areasum)
#             avgsquared.component_square()
#             squaredavg = (squaresum/areasum)
#             result = (squaredavg-avgsquared)
#             result.component_sqrt()

#             sep_string = getSeparator()
#             output_header = result.label_list()
#             outputstringlist.append(getCommentChar() + \
#                                     sep_string.join(output_header))
#             outputstringlist.append(
#                 sep_string.join([`x` for x in result.value_list()]))
#         #Send output to front end (process/rank 0)
#         mpitools.Send_String('\n'.join(outputstringlist),0)
# # end if parallel_enable.enabled()

###############################################################################

# The most basic, a direct-output class that just writes out the data
# at all the samples.

class DirectOutput(DataOperation):
    def columnNames(self, output, sampling):
        return sampling.get_col_names() + output.columnNames()
    def __call__(self, time, output, domain, sampling, destination):
        # if parallel_enable.enabled():
        #     if mpitools.Rank()==0:
        #         _DirectOutput_call_frontend(output,domain,sampling,
        #                                     destination)
        #     else:
        #         _DirectOutput_call_backend(output,domain,sampling,
        #                                     destination)
        #     return

        # "olist" is a list or iterable of tuples of the form (sample,
        # value).
        olist = sampling.evaluate(domain, output)
        header = sampling.get_col_names()

        if showTime():
            destination.comment("time:", `time`)
            
        for (s,v) in olist:
            tags = sampling.columnData(header, s)
            if len(tags)==1:
                for t in tags[0]: # tags[0] is a list of strings
                    print >> destination, t,
                for x in v.value_list():
                    print >> destination, x,
                print >> destination
            else: # Multiple values -- do above for each tag-val pair.
                for (tag, val) in zip(tags, v):
                    for t in tag:
                        print >> destination, t,
                    for x in val.value_list():
                        print >> destination, x,
                    print >> destination

# "Direct Output" is special, in that the corresponding auto-generated
# menu item is used directly in the meshcstoolboxGUI code -- if the
# name is changed here, it should be changed there also.
              
directOutput = registeredclass.Registration(
    'Direct Output', DataOperation, DirectOutput, 
    ordering=0,
    params=[],
    tip="Write the data values directly.",
    direct=True,
    sampling=(analysissample.DiscreteSampleSet,),
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/directoutput.xml'))

##############

# There are constraints on the output types of the output objects that
# can be processed by these functions -- they must either be Floats,
# or they must be composite objects for which __add__ and __sub__
# operate component-wise, __mul__ and __div__ take scalar operands,
# and for which point-wise operations "component_square" and
# "component_sqrt" are defined.  This is currently true of all
# OutputValPtr subclasses, including SymmMatrix3.

class RangeOutput(OneLineDataOperation):
    def __call__(self, time, output, domain, sampling, destination):
        olist = sampling.evaluate(domain, output)
        vmin = None
        vmax = None
        for sample, value in olist:
            assert value is not None
            v = value.value()
            if vmin is None or vmin > v:
                vmin = v
            if vmax is None or vmax < v:
                vmax = v
        self.printResults(time, [vmin, vmax], destination)
    def colNames(self, output):
        cnames = output.columnNames()
        return ["min "+x for x in cnames] + ["max " +x for x in cnames]

registeredclass.Registration(
    "Range",
    DataOperation,
    RangeOutput,
    ordering=1,
    direct=False, 
    sampling=(analysissample.DiscreteSampleSet,),
    tip="Print the min and max values of the data over the domain.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/range.xml'))

#######

class AverageAndDeviation(OneLineDataOperation):
    def __call__(self, time, output, domain, sampling, destination):
        # areasum, integralsum, squaresum = _getMoments(sampling, domain, output,
        #                                               (0,1,2))

        integrals = sampling.integrateWithExponents(domain, output, (0, 1, 2))
        area = integrals[0].value_list()[0] # a float
        mean = integrals[1]/area    # an OutputVal
        avgsquared = mean.clone()
        avgsquared.component_square()
        squaredavg = integrals[2]/area
        deviation = squaredavg - avgsquared
        deviation.component_abs()
        deviation.component_sqrt()
        self.printResults(
            time,
            utils.flatten(zip(mean.value_list(), deviation.value_list())),
            destination)
    def colNames(self, output):
        return utils.flatten(
            ["average of "+name, "standard deviation of " +name]
            for name in output.columnNames())

registeredclass.Registration(
    "Average and Deviation",
    DataOperation,
    AverageAndDeviation,
    2,
    direct=False,
    sampling=(analysissample.SampleSet,),
    tip="Print the average and standard deviation of the samples.",
    discussion=xmlmenudump.loadFile(
        "DISCUSSIONS/engine/menu/averagedeviation.xml"))

########

class IntegrateOutput(OneLineDataOperation):
    def __call__(self, time, output, domain, sampling, destination):
        # (integral,) = _getMoments(sampling, domain, output, (1,))
        integral = sampling.integrate(domain, output)
        self.printResults(time, integral.value_list(), destination)
    def colNames(self, output):
        return ["integral of "+name for name in output.columnNames()]

registeredclass.Registration(
    "Integral",
    DataOperation,
    IntegrateOutput,
    3.5,
    direct=False,
    sampling=(analysissample.ContinuumSampleSet,),
    tip="Integrate the data over the area or volume of the samples.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/integrate.xml'))

########

# Integrates the output over each sample, and normalizes by the
# power=0 version.

class AverageOutput(OneLineDataOperation):
    def __call__(self, time, output, domain, sampling, destination):

        # if parallel_enable.enabled():
        #     if mpitools.Rank()==0:
        #         _AverageOutput_call_frontend(output,domain,sampling,
        #                                     destination)
        #     else:
        #         _AverageOutput_call_backend(output,domain,sampling,
        #                                     destination)
        #     return

        # areasum, integralsum = _getMoments(sampling, domain, output, (0, 1))
        integrals = sampling.integrateWithExponents(domain, output, (0, 1))
        area = integrals[0].value_list()[0]
        result = integrals[1]/area
        self.printResults(time, result.value_list(), destination)
    def colNames(self, output):
        return ["average of "+name for name in output.columnNames()]
     
registeredclass.Registration(
    "Average",
    DataOperation,
    AverageOutput,
    3,
    direct=False,
    sampling=(analysissample.SampleSet,),
    tip="Average the data over all the samples.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/average.xml')
    )

#######

# Standard deviation, square root of the integral of ( (x-<x>)^2 ),
# which is of course (<x^2>-<x>^2)^(1/2)

class StdDevOutput(OneLineDataOperation):
    def __call__(self, time, output, domain, sampling, destination):

        # if parallel_enable.enabled():
        #     if mpitools.Rank()==0:
        #         _StdDevOutput_call_frontend(output,domain,sampling,
        #                                     destination)
        #     else:
        #         _StdDevOutput_call_backend(output,domain,sampling,
        #                                     destination)
        #     return

        # areasum, integralsum, squaresum = _getMoments(sampling, domain, output,
        #                                               (0,1,2))
        integrals = sampling.integrateWithExponents(domain, output, (0, 1, 2))
        area = integrals[0].value_list()[0]
        avgsquared = integrals[1]/area
        avgsquared.component_square()
        squaredavg = integrals[2]/area
        result = squaredavg - avgsquared
        result.component_sqrt()
        self.printResults(time, result.value_list(), destination)
    def colNames(self, output):
        return ["standard deviation of "+name for name in output.columnNames()]

registeredclass.Registration(
    "Standard Deviation",
    DataOperation,
    StdDevOutput,
    4,
    direct=False,
    sampling=(analysissample.SampleSet,),
    tip="Compute the standard deviation of the data over the samples.",
    discussion=xmlmenudump.loadFile("DISCUSSIONS/engine/menu/deviation.xml"))

    
#########################

