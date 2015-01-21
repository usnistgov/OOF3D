# -*- python -*-
# $RCSfile: oof_getopt.py,v $
# $Revision: 1.4.18.1 $
# $Author: langer $
# $Date: 2014/09/27 22:33:53 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

## This module is a modified version from the public library.
## This version ignores undeclared options because we want internal MPI
## options to be ignored and processed by MPI_Init() without raising an
## exception. The modified module assumes that MPI-generated options are
## appended at the end of the list. If the options were appended at the
## beginning of the list, this module will not work because the moment
## an unrecognized option with an argument is passed everything that
## follows will be ignored, even valid options.

"""Parser for command line options.

This module helps scripts to parse the command line arguments in
sys.argv.  It supports the same conventions as the Unix getopt()
function (including the special meanings of arguments of the form `-'
and `--').  Long options similar to those supported by GNU software
may be used as well via an optional third argument.  This module
provides a single function and an exception:

getopt() -- Parse command line options
GetoptError -- exception (class) raised with 'opt' attribute, which is the
option involved with the exception.
"""

# Long option support added by Lars Wirzenius <liw@iki.fi>.

# Gerrit Holl <gerrit@nl.linux.org> moved the string-based exceptions
# to class-based exceptions.

__all__ = ["GetoptError","error","getopt"]

class GetoptError(Exception):
    opt = ''
    msg = ''
    def __init__(self, msg, opt):
        self.msg = msg
        self.opt = opt
        Exception.__init__(self, msg, opt)

    def __str__(self):
        return self.msg

error = GetoptError # backward compatibility

def getopt(args, shortopts, longopts = []):
    """getopt(args, options[, long_options]) -> opts, args

    Parses command line options and parameter list.  args is the
    argument list to be parsed, without the leading reference to the
    running program.  Typically, this means "sys.argv[1:]".  shortopts
    is the string of option letters that the script wants to
    recognize, with options that require an argument followed by a
    colon (i.e., the same format that Unix getopt() uses).  If
    specified, longopts is a list of strings with the names of the
    long options which should be supported.  The leading '--'
    characters should not be included in the option name.  Options
    which require an argument should be followed by an equal sign
    ('=').

    The return value consists of two elements: the first is a list of
    (option, value) pairs; the second is the list of program arguments
    left after the option list was stripped (this is a trailing slice
    of the first argument).  Each option-and-value pair returned has
    the option as its first element, prefixed with a hyphen (e.g.,
    '-x'), and the option argument as its second element, or an empty
    string if the option has no argument.  The options occur in the
    list in the same order in which they were found, thus allowing
    multiple occurrences.  Long and short options may be mixed.

    """

    opts = []
    if type(longopts) == type(""):
        longopts = [longopts]
    else:
        longopts = list(longopts)
    while args and args[0].startswith('-') and args[0] != '-':
        ## Here every option that starts with - or -- is parsed.
        ## Parsing stops when something does NOT start with -
        ## or --.
        if args[0] == '--':
            args = args[1:]
            break
        if args[0].startswith('--'):
            ## long options are parsed
            opts, args = do_longs(opts, args[0][2:], longopts, args[1:])
        else:
            ## shorts options are parsed
            opts, args = do_shorts(opts, args[0][1:], shortopts, args[1:])
    ## When parsing ends, return parsed options
    return opts, args

def do_longs(opts, opt, longopts, args):
    try:
        ## try to find the option that has a =
        i = opt.index('=')
    except ValueError:
        ## if not found, option does not take arguments
        optarg = None
    else:
        ## if found assign to variables
        opt, optarg = opt[:i], opt[i+1:]
    ## here we check that opt IS a valid option
    ## has_arg = -1: invalid option
    ## has_arg =  0: valid option with NO arguments
    ## has_arg =  1: valid option with arguments
    has_arg, opt = long_has_args(opt, longopts)
    ## print "has_arg, opt, optarg", has_arg, opt, optarg, "\n"
    if has_arg>0:
        ## detected option MUST have arguments
        ## print "if has_arg>0:", has_arg
        if optarg is None: ## check for arguments
            ## print opt, args, has_arg
            if args is None or len(args)<1: ## if option does not have arguments, raise Exception
                ## print " if args is None:", opt, arg, args
                raise GetoptError('option --%s requires argument' % opt, opt)
            else:
                ## if option does in fact have arguments, then
                ## option is well formed, and option is returned
                optarg, args = args[0], args[1:]
                opts.append(('--' + opt, optarg or ''))
                return opts, args
        else:
            ## if detected option is an argument free option
            ## just return it 
            ## print " else", opts, args
            opts.append(('--' + opt, optarg or ''))
            return opts, args
    if has_arg<0: ## invalid options are NOT appended, thus ignored.
        ## opts.append(('', ''))
        ## print "if has_arg<0:"
        ## print opts, args
        return opts, args
    if has_arg == 0: ## options with NO arguments are appended and passed
        ## print "if has_arg == 0:", opts, optarg
        opts.append(('--' + opt, optarg ))
        return opts, args
    elif optarg:
        ## if option should not have an option, but an option
        ## found, then this must be a mistake, and an Exception is raised
        raise GetoptError('option --%s must not have an argument' % opt, opt)
    opts.append(('--' + opt, optarg or ''))
    return opts, args

# Return:
#   has_arg?
#   full option name
def long_has_args(opt, longopts):
    ## if the option, a.k.a., opt, starts the same way a valid option
    ## select the possibility
    possibilities = [o for o in longopts if o.startswith(opt)]
    if not possibilities:
        ## raise GetoptError('option --%s not recognized' % opt, opt)
        ## print opt
        return -1, opt
    # Is there an exact match?
    if opt in possibilities:
        return 0, opt
    elif opt + '=' in possibilities:
        return 1, opt
    # No exact match, so better be unique.
    if len(possibilities) > 1:
        # XXX since possibilities contains all valid continuations, might be
        # nice to work them into the error msg
        ## raise GetoptError('option --%s not a unique prefix' % opt, opt)
        return -1, opt
    assert len(possibilities) == 1
    unique_match = possibilities[0]
    has_arg = unique_match.endswith('=')
    ## print "has_arg = unique_match.endswith('=')", has_arg
    if has_arg>0:
        unique_match = unique_match[:-1]
    return has_arg, unique_match

def do_shorts(opts, optstring, shortopts, args):
    while optstring != '':
        opt, optstring = optstring[0], optstring[1:]
        if short_has_arg(opt, shortopts)>0:
            if optstring == '':
                if not args:
                    raise GetoptError('option -%s requires argument' % opt,
                                      opt)
                optstring, args = args[0], args[1:]
            optarg, optstring = optstring, ''
        elif short_has_arg(opt, shortopts)<0:
            optarg = ''
            ## opt = ''
        else:
            optarg = ''
        opts.append(('-' +opt, optarg))
    return opts, args

def short_has_arg(opt, shortopts):
    for i in range(len(shortopts)):
        if opt == shortopts[i] != ':':
            return shortopts.startswith(':', i+1)
    ## raise GetoptError('option -%s not recognized' % opt, opt)
    return -1 ## ignore unrecognized argument

if __name__ == '__main__':
    import sys
    print getopt(sys.argv[1:], "a:b", ["alpha=", "beta"])
