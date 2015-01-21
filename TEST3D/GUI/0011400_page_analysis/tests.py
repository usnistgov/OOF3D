# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.4 $
# $Author: langer $
# $Date: 2014/09/27 22:35:13 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from generics import *

def SetOutputCheck(number=0, outputs=None):
    return (chooserCheck('OOF3D:Analysis Page:top:Output:Outputs:Outputs_'+str(number), outputs))
    
def SetParameterCheck(output=None, parameters=None):
    return (chooserCheck('OOF3D:Analysis Page:top:Output:Outputs:Parameters:'+output, parameters))
    
def SetTypeCheck(typeos=None):
    return (chooserCheck('OOF3D:Analysis Page:top:Output:Outputs:Parameters:type:Chooser', typeos))
    
def SetMinuendParameterCheck(output=None, parameters=None):
    return (chooserCheck('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:'+output, parameters))
    
def SetMinuendTypeCheck(typeos=None):
    return (chooserCheck('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:type:Chooser', typeos))
    
def SetMinuendSubtrahendParameterCheck(output=None, parameters=None):
    return (chooserCheck('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:Parameters:'+output, parameters))
    
def SetMinuendSubtrahendTypeCheck(typeos=None):
    return (chooserCheck('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:Parameters:type:Chooser', typeos))
    
def SetSubtrahendCheck(number=0, subtrahends=None):
    return (chooserCheck('OOF3D:Analysis Page:top:Output:Outputs:Parameters:subtrahend:subtrahend_'+str(number), subtrahends))
    
def SetMinuendSubtrahendCheck(number=0, subtrahends=None):
    return (chooserCheck('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:subtrahend_'+str(number), subtrahends))

def SetMinuendCheck(number=0, minuends=None):
    return (chooserCheck('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:minuend_'+str(number), minuends))
    
def SetDomainCheck(domains=None):
    return (chooserCheck('OOF3D:Analysis Page:top:Domain:DomainRCF:Chooser', domains))
    
def SetDomainParametersSimpleCheck(domain=None, parameter=None, selections=None):
    return (chooserCheck('OOF3D:Analysis Page:top:Domain:DomainRCF:'+domain+':'+parameter, selections))
    
def SetDomainParametersChooserCheck(domain=None, parameter=None, selections=None):
    return (chooserCheck('OOF3D:Analysis Page:top:Domain:DomainRCF:'+domain+':'+parameter+':Chooser', selections))
    
def SetSamplingCheck(samplings=None):
    if samplings == None:
       samplingbutton = gtklogger.findWidget('OOF3D:Analysis Page:bottom:Sampling:Sampling:Chooser')
       return ((samplingbutton.get_property('sensitive') == False))
    else:
       return (chooserCheck('OOF3D:Analysis Page:bottom:Sampling:Sampling:Chooser', samplings))
    
def SetOperationCheck(operations=None):
    return (chooserCheck('OOF3D:Analysis Page:bottom:Operation:OperationRCF:Chooser', operations))
    
def SetOutputSelect(number=0, output=None):
    return (chooserStateCheck('OOF3D:Analysis Page:top:Output:Outputs:Outputs_'+str(number), output))
    
def SetParameterSelect(output=None, parameter=None):
    return (chooserStateCheck('OOF3D:Analysis Page:top:Output:Outputs:Parameters:'+output, parameter))
    
def SetTypeSelect(typeo=None):
    return (chooserStateCheck('OOF3D:Analysis Page:top:Output:Outputs:Parameters:type:Chooser', typeo))
    
def SetMinuendParameterSelect(output=None, parameter=None):
    return (chooserStateCheck('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:'+output, parameter))
    
def SetMinuendTypeSelect(typeo=None):
    return (chooserStateCheck('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:type:Chooser', typeo)) 
    
def SetMinuendSubtrahendParameterSelect(output=None, parameters=None):
    return (chooserStateCheck('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:Parameters:'+output, parameters))
    
def SetMinuendSubtrahendTypeSelect(typeos=None):
    return (chooserStateCheck('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:Parameters:type:Chooser', typeos))
    
def SetSubtrahendSelect(number=0, subtrahend=None):
    return (chooserStateCheck('OOF3D:Analysis Page:top:Output:Outputs:Parameters:subtrahend:subtrahend_'+str(number), subtrahend))
    
def SetMinuendSubtrahendSelect(number=0, subtrahend=None):
    return (chooserStateCheck('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:Parameters:subtrahend:subtrahend_'+str(number), subtrahend))
    
def SetMinuendSelect(number=0, minuend=None):
    return (chooserStateCheck('OOF3D:Analysis Page:top:Output:Outputs:Parameters:minuend:minuend_'+str(number), minuend))
    
def SetDomainSelect(domain=None):
    return (chooserStateCheck('OOF3D:Analysis Page:top:Domain:DomainRCF:Chooser', domain))
    
def SetDomainParametersSimpleSelect(domain=None, parameter=None, selection=None):
    return (chooserStateCheck('OOF3D:Analysis Page:top:Domain:DomainRCF:'+domain+':'+parameter, selection))
    
def SetDomainParametersChooserSelect(domain=None, parameter=None, selection=None):
    return (chooserStateCheck('OOF3D:Analysis Page:top:Domain:DomainRCF:'+domain+':'+parameter+':Chooser', selection))
    
def SetSamplingSelect(sampling=None):
    return (chooserStateCheck('OOF3D:Analysis Page:bottom:Sampling:Sampling:Chooser', sampling))
    
def SetOperationSelect(operation=None):
    return (chooserStateCheck('OOF3D:Analysis Page:bottom:Operation:OperationRCF:Chooser', operation))
