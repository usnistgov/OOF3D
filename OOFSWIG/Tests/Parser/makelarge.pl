print "%module huge\n";
print "int foobar(int);\n";
print "/*\n";
for ($i = 0; $i < 10000; $i++) {
    print "This is a very long comment $i.\n";
}

print "*/\n";

