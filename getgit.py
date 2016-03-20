import subprocess
proc = subprocess.Popen(['git', 'symbolic-ref', '--short', 'HEAD'],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdoutdata, stderrdata = proc.communicate()
if stderrdata:
    print "Failed to get git branch name"
    print stderrdata
    gitbranch = ""
else:
    print type(stdoutdata)
    print "->>%s<<-" % stdoutdata.strip()
