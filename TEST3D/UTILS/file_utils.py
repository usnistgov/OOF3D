# -*- python -*-
# $RCSfile: file_utils.py,v $
# $Revision: 1.1.2.5 $
# $Author: langer $
# $Date: 2014/04/28 20:46:18 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

import math
import os
import re
import sys

# Flag that says whether to generate missing reference data files.
# Should be false unless you really know what you're doing.
generate=False
# Max number to report from one file.
maxerrors = 10

errorcount = 0
filename1 = None
filename2 = None
silent = False

# globals, because we can afford to be quick and dirty here.
def print_header():
    global filename1, filename2, silent
    if not silent:
        print >> sys.stderr, "Error comparing files", \
            os.path.abspath(filename1), os.path.abspath(filename2)

def print_mismatch(line, v1, v2):
    global errorcount
    if errorcount==0:
        print_header()
    if errorcount == maxerrors and not silent:
        print >> sys.stderr, "[Skipping further errors]"
    if errorcount < maxerrors and not silent:
        print >> sys.stderr, "   line %5d: %s != %s" % (line+1, v1, v2)
    errorcount += 1

def print_float_mismatch(line, v1, v2):
    global errorcount
    if errorcount==0:
        print_header()
    if errorcount == maxerrors and not silent:
        print >> sys.stderr, "[Skipping further errors]"
    if errorcount < maxerrors and not silent:
        print >> sys.stderr, \
            "   line %5d: %-16.9g != %-16.9g  (diff=% 8g, % .2g%%)" \
            % (line+1, v1, v2,
               v1-v2,
               100.*(v1-v2)/(0.5*(abs(v1) + abs(v2))))
    errorcount += 1

def print_int_mismatch(line, v1, v2):
    global errorcount
    if errorcount==0:
        print_header()
    if errorcount == maxerrors and not silent:
        print >> sys.stderr, "[Skipping further errors]"
    if errorcount < maxerrors and not silent:
        print >> sys.stderr, "   line %5d: %16d != %16d" % (line+1, v1, v2)
    errorcount += 1

def conversion_error(line, v1, v2):
    global errorcount
    if not errorcount:
        print_header()
    if not silent:
        print >> sys.stderr, ("   line %5d: %s // %s  (conversion error!)"
                              % (line+1, v1, v2))
    errorcount += 1
        
def eof_error(line, filename):
    global errorcount
    if not errorcount:
        print_header()
    if not silent:
        print >> sys.stderr, ("   Line %5d: Premature EOF in file %s!" 
                              % (line+1, filename))
    errorcount += 1

def too_many_lines(filename, nlines):
    global errorcount
    if not errorcount:
        print_header()
    if not silent:
        print >> sys.stderr, ("  Too many lines in file %s!  Expected %d."
                              % (filename, nlines))
    errorcount += 1

def too_few_lines(filename, nlines):
    global errorcount
    if not errorcount:
        print_header()
    if not silent:
        print >> sys.stderr, ("  Too few lines in file %s!  Expected %d."
                              % (filename, nlines))
    errorcount += 1

# set_reference_dir can be called to change the directory in which
# reference files are to be found.  regression.py sets it to the TEST
# directory before cd'ing to the temp directory.  Files named in the
# *second* argument to fp_file_compare are automatically looked for in
# the reference directory.  Reference filenames used by other routines
# should be processed through reference_file() before being used.

referencedir = ''
def set_reference_dir(path):
    global referencedir
    referencedir = path

def reference_file(*args):
    # This does the right thing if referencedir is an empty string.
    return os.path.join(referencedir, *args)

def fp_file_compare(file1, file2, tolerance, comment="#", pdfmode=False,
                    ignoretime=False, quiet=False, nlines=None):
    # file1 is assumed to be in the current directory. file2 is
    # assumed to be in the reference directory.

    # If nlines is not None, this function will expect there to be
    # exactly nlines lines in file1 and at least nlines lines in
    # file2.

    # Regexp for matching floating-point numbers, copied from section
    # 4.2.6 of the Python 2.3 documentation.  The "(...)" group
    # constructs in the original have been replaced by "(?:...)"
    # constructs, as a way of grouping sub-expressions without
    # creating explicit groups in the regexp itself. The explicit
    # groups cause split and match to be annoying.
    floatpattern = re.compile(
        "[-+]?(?:\d+(?:\.\d*)?|\d*\.\d+)(?:[eE][-+]?\d+)?")

    # Pattern for detecting PDF date strings, which should not be
    # compared.  This looks for a non-digit or beginning of a line,
    # followed by exactly 14 digits, followed by 'Z'.
    datepattern = re.compile("(?:\D|^)\d{14}Z")
    # Pattern for detecting the time as printed by datetime.today().
    timepattern = re.compile("\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d\.\d*")

    try:
        file2 = reference_file(file2)
        f2 = open(file2, "r")
    except:
        if generate:
            print >> sys.stderr, "\nMoving file %s to %s.\n" % (file1, file2)
            os.system('cp '+file1+' '+file2)
            return True
        else:
            raise

    f1 = open(file1, "r")

    global errorcount, filename1, filename2, silent
    filename1 = file1           # store in globals
    filename2 = file2
    errorcount = 0
    silent = quiet

    try:
        f1_lineno = -1        # just in case file1 is empty
        for f1_lineno, f1_line in enumerate(f1):
            if nlines is not None and f1_lineno == nlines:
                too_many_lines(filename1, nlines)
            try:
                f2_line = f2.next()
            except StopIteration:
                eof_error(f1_lineno, filename2)
                break
            if comment is not None and f1_line[0] == f2_line[0] == comment:
                continue

            # If we're comparing PDF files, and both lines contain
            # date strings, just go on to the next lines.  This
            # ignores anything else on a line containing dates.  It's
            # not generally true that there's nothing else interesting
            # on date lines, but it is true of the pdf's generated by
            # oof.
            if ((pdfmode and 
                datepattern.search(f1_line) and datepattern.search(f2_line)) or
                (ignoretime and 
                timepattern.search(f1_line) and timepattern.search(f2_line))):
                continue
                
            f1_text_items = floatpattern.split(f1_line)
            f2_text_items = floatpattern.split(f2_line)
            f1_float_items = floatpattern.findall(f1_line)
            f2_float_items = floatpattern.findall(f2_line)

            for (item1, item2) in zip(f1_text_items, f2_text_items):
                if item1.strip() != item2.strip():
                    print_mismatch(f1_lineno, item1, item2)
            
            for(item1, item2) in zip(f1_float_items, f2_float_items):
                try:
                    int1 = int(item1)
                    int2 = int(item2)
                except ValueError:
                    try:
                        float1 = float(item1)
                        float2 = float(item2)
                    except ValueError:
                        conversion_error(f1_lineno, item1, item2)
                    else:
                        diff = abs(float1 - float2)
                        reltol = min(abs(float1), abs(float2))*tolerance
                        # This uses the same tolerance for both absolute
                        # and relative error, which isn't usually a good
                        # idea, but is ok if the numbers being compared
                        # are more or less of order 1.
                        ok = diff < reltol or diff < tolerance
                        if not ok:
                            print_float_mismatch(f1_lineno, float1, float2)
                else: # Integer conversion worked, do comparison.
                    if int1!=int2:
                        print_int_mismatch(f1_lineno, int1, int2)

        # end for f1_lineno, f1_line in enumerate(f1)

        # Is there more to read from file 2?
        try:
            f2_line = f2.next()
        except StopIteration:
            moref2 = False
        else:
            moref2 = True
                        
        if nlines is not None:
            # Check that we read nlines lines, unless we're also done
            # with file 2.  In that case, since the files are the
            # same, the test passes, even if the provided nlines is
            # too large.
            if f1_lineno < nlines-1 and moref2:
                too_few_lines(filename1, nlines)
        else: 
            # nlines is None, so the files must agree exactly.  We're
            # already at the end of file 1.  Check that there's
            # nothing left in file 2.
            if moref2:
                eof_error(f1_lineno, filename1)
        
        if errorcount > 0:
            if not silent:
                print >> sys.stderr, ("%d error%s in file comparison!" %
                                      (errorcount, "s"*(errorcount!=1)))
            return False

        if not silent:
            print >> sys.stderr, "Files", filename1, "and", filename2, "agree."
        return True
    finally:
        f1.close()
        f2.close()

def compare_last(filename, numbers, tolerance=1.e-10):
    # The last line of the given file contains a bunch of numbers
    # separated by commas.  Check that the numbers in the file are
    # within tolerance of the tuple 'numbers'.
    phile = open(filename, "r")
    filenumbers = eval(phile.readlines()[-1])
    if len(numbers) != len(filenumbers):
        print >> sys.stderr, "*** Expected", len(numbers), "numbers.  Got",\
            len(filenumbers)
        return False
    for (x, y) in zip(numbers, filenumbers):
        if math.fabs(x-y) > tolerance:
            print >> sys.stderr, "*** Expected", numbers
            print >> sys.stderr, "***    Found", filenumbers 
            return False
    return True

def binary_file_compare(file1, file2, strict=False):
    # file1 is assumed to be in the current directory. file2 is
    # assumed to be in the reference directory.

    # If strict is False, the beginning of the files are examined, and
    # if they contain a string like "# OOF version *\n", that string
    # is ignored.  This allows files written by different OOF versions
    # to be considered identical.

    try:
        file2 = reference_file(file2)
        f2 = open(file2, "rb")
    except:
        if generate:
            print >> sys.stderr, "\nMoving file %s to %s.\n" % (file1, file2)
            os.system('cp '+file1+' '+file2)
            return True
        else:
            raise

    BUFSIZE = 1024
    vStr = "# OOF version"
    f1 = open(file1, 'rb')
    first = True
    while True:
        b1 = f1.read(BUFSIZE)
        b2 = f2.read(BUFSIZE)
        if first and not strict and b1.startswith(vStr) and b2.startswith(vStr):
            # Check for a comment containing the version number, and ignore it.
            bb1 = b1.split('\n', 1)
            bb2 = b2.split('\n', 1)

            # Compare everything after the first newline.
            if bb1[1] != bb2[1]:
                return False
            if not bb1[1]:
                return True
        else:
            if b1 != b2:
                return False
        if not b1:
            return True
        first = False
        
# remove() should be used to remove a file that a test generated for
# comparison with fp_file_compare.  If fp_file_compare was running
# with generate==True, the file might not exist, but remove() won't
# complain.

def remove(filename):
    try:
        os.remove(filename)
    except:
        if generate:
            pass
        else:
            raise

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
    
if __name__ == "__main__":
    import sys
    import getopt

    tolerance = 0
    pdf = False
    commentchar = '#'

    option_list = ['tolerance=', 'pdf', 'comment', 'max=']
    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'c:t:pm:', option_list)
    except getopt.error, message:
        print message
        sys.exit(2)

    for opt in optlist:
        if opt[0] in ('--tolerance', '-t'):
            tolerance = float(opt[1])
        if opt[0] in ('--pdf', '-p'):
            pdf = True
        if opt[0] in ('--comment', '-c'):
            commentchar = opt[1]
        if opt[0] in ('--max', '-m'):
            maxerrors = int(opt[1])

    ok = fp_file_compare(args[0], args[1], tolerance=tolerance,
                         comment=commentchar, pdfmode=pdf)
    if not ok:
        print 'Files differ.'
        sys.exit(1)
    sys.exit(0)
