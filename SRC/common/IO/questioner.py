# -*- python -*-
# $RCSfile: questioner.py,v $
# $Revision: 1.3.10.1 $
# $Author: langer $
# $Date: 2014/09/27 22:34:02 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Ask a question of the user, allowing him or her to choose from a set
# of strings.  Returns the string chosen.

def questionerCLI(question, *answers, **kwargs):
    try:
        default = kwargs['default']
    except KeyError:
        default = None
        defaultstr = ''
        responses = answers
    else:
        defaultstr = '[%s] ' % default
        if default not in answers:
            responses = answers + (default,)
    result = None
    while not result:
        inp = raw_input('%s %s: %s' % (question, responses, defaultstr))
#         print '-->%s<--' % inp
        if inp:
            if inp in responses:
                result = inp
            else:
                # Look for a unique match
                nletters = len(inp)
                for answer in responses:
                    if answer[:nletters] == inp:
                        if result:          # second match!
                            result = None
                            break
                        else:
                            result = answer
        else:
            result = default
    return result
    



# questioner may be redefined if the GUI is loaded
questioner = questionerCLI
