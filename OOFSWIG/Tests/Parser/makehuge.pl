print "%module huge\n";
for ($i = 0; $i < 5000; $i++) {
    print "double func$i(int, double, char *, User *);\n";
}

# Now make a bunch of truly hellacious functions

for ($i = 0; $i < 1000; $i++) {
    print "int lfunc$i(";
    for ($j = 0; $j < $i; $j++) {
	print "double,";
    } 
    print "double);\n";
}

for ($i = 0; $i < 5000; $i++) {
    print "char *var$i;\n";
}

for ($i = 0; $i < 100; $i++) {
    print "#define con$i ";
    for ($j = 0; $j < $i; $j++) {
	print "acon$j + ";
    } 
    print "1\n";
}

