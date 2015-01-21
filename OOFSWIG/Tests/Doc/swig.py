# This file was created automatically by SWIG.
import swigc
class AClassPtr :
    def __init__(self,this):
        self.this = this
        self.thisown = 0
    def foo(self):
        """   This is a comment for the foo member function   
"""
        val = swigc.AClass_foo(self.this)
        return val
    def __setattr__(self,name,value):
        if name == "a" :
            swigc.AClass_a_set(self.this,value)
            return
        self.__dict__[name] = value
    def __getattr__(self,name):
        if name == "a" : 
            return swigc.AClass_a_get(self.this)
        raise AttributeError,name
    def __repr__(self):
        return "<C AClass instance>"
class AClass(AClassPtr):
    """   This comment should be attached to the class definition   
"""
    def __init__(self,this):
        self.this = this






#-------------- FUNCTION WRAPPERS ------------------

def foo(arg0):
    """   This is a comment before a function   
"""
    val = swigc.foo(arg0)
    return val

def bar(arg0):
    """   This is a 
   multiline comment
   appearing before
   a function
"""
    val = swigc.bar(arg0)
    return val

def grok(arg0):
    """   This is a comment for grok   
"""
    val = swigc.grok(arg0)
    return val

def frob(arg0):
    """   Comment before function frob   
"""
    val = swigc.frob(arg0)
    return val

def decl(arg0,arg1,arg2,arg3,arg4,arg5):
    """   This is a comment before a multiline declaration   
"""
    val = swigc.decl(arg0,arg1,arg2,arg3,arg4,arg5)
    return val



#-------------- VARIABLE WRAPPERS ------------------

ENUM1 = swigc.ENUM1
ENUM2 = swigc.ENUM2
ENUM3 = swigc.ENUM3
ENUM4 = swigc.ENUM4
cvar = swigc.cvar
