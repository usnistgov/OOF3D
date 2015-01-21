all::
	@sh make.sh

huge::
	@sh huge.sh

# Clean up output and diffs, but leave the regr testing files

clean::
	rm -f *~ *_wrap* *.pm *.py *.output *.diff
	rm -f *_regr.perl* *_regr.python* *_regr.tcl* *_regr.guile* huge.i large_header* large_comment*

# Blow away everything except the base-level regression testing files
# This is what I do before a distribution

dist::
	rm -f *~ *_wrap* *.pm *.py *.output *.diff *_regr.*.c

# Destroy everything--includes all regression testing files
# Only use when all other options have become futile...

nuke::
	rm -f *~ *_wrap* *.pm *.py *.output *.diff *_regr* *.msg


