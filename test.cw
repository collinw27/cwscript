
print (1 + 2 - 3);
.a = 2;
print (.a + 3);

if 0 {print "Failed";};
if true {print "Succeeded";};

.func = function [.a, .b] {
	print (.a + .b);
};

# Make sure function scopes are removed

.c = 1;
print (.func -> [3, 1 + 2]);
.func -> [3, 1 + 2];
.func -> [3, 1 + 2];
print .c;