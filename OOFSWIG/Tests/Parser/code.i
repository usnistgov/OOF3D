%module code

// See if SWIG properly handles someone putting code after a declaration

int fact(int n) {
	if (n <= 1) return 1;
	else return n*fact(n-1);
}


