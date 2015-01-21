// This file tests objective C parsing

%module foo

// A simple class

@interface foo1 : Object {
double a;
int    b;
}

- (int) bar1: (double) a;
+ (void) bar2;
- bar3;
+ new;
- free;
- private$member;           // Test $ in a name

- spam1 : (int) a with:(double) b andWith: (char *) c;
+ spam2 : (int) a with:(double) b andWith: (char *) c;

@end

// A simple class (with no base)

@interface foo2 {
double a;
double b;
}

- (int) bar1: (double) a;
@end

// A class with protocols

@interface foo3 : Object <proto1, proto2, proto3 > {
double a,b;
}

- (int) bar1: (double) a;
@end

// The following declarations should be ignored entirely

@implementation Foo

... a bunch of stuff

@end

@protocol Foo

... a bunch of stuff

@end

// A category

@interface foo1 (category1)

- more1;
- (int) more2 : (double) a;

@end

// Test some inheritance

@interface inherit1 : foo1 {
@public
int a,b,c;
}

- (int) base1;
- (double) base2 : (int) a;

@end

// Renamed members

@interface rname : Object {
@public
int a,b,c;
%name(myd) double d;
}

%name(myname) - (int) oldname : (double) a : (int) b;

@end

// Added methods 

@interface added : Object {
}

%addmethods {
- (double) added1 : (double) a : (double) b {
	return (a+b);
  }
+ (int) addi : (int) a : (int) b {
   	return (a+b);
}
}

@end


// a separated addmethods

%addmethods foo1 {
- (double) added2 : (double) a {
    return -a;
  }
}

@class cls1, cls2, cls3;


// Check proto-typed datatypes

void proto1(id<Proto1> a, id<Proto2> b, id<Proto3,Proto4,Proto5> c);
