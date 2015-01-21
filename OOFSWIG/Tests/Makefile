parser::
	@cd Parser; $(MAKE)

doc::	
	@cd Doc; $(MAKE)

huge::	
	@cd Parser; $(MAKE) huge

build::
	@cd Build; $(MAKE)

errors::
	@cd Errors; $(MAKE)

all:	parser doc build errors huge

clean::
	@cd Parser; $(MAKE) clean
	@cd Build; $(MAKE) clean
	@cd Errors; $(MAKE) clean
	@cd Doc; $(MAKE) clean

