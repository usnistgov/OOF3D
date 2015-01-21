print "%module huge\n";
print "%{\n";
for ($i = 0; $i < 10000; $i++) {
    print "This is a very long header block $i.\n";
}

print "%}\n";
print "int foobar(int);\n";


