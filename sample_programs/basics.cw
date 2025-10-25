
# Literals & printing

print null;
print 1;
print 1.0;
print "string";

# Instead of separating arguments with spaces, parentheses are also allowed

print(1);
print(max(1)(2));

# Variables

.a = 1;
print .a;
.a += 2;
print .a;
# print .b = error

# Lists

print "\nTesting lists:";
print [1, 4, 9];
print range 10;
print adv_range 0 30 10;

.l = [1];
append .l 2;
.l += [3];
print .l;
pop .l -1;
print .l;

# Objects, indexing, and scopes

print "\nTesting objects:";
.obj = new {
	.name = "Test object";
	.value = 40;
};

print .obj;
print .obj.name;
print(.obj : 'name');
print(local : 'obj' : 'name');
print(global : 'obj' : 'name');

print getd .obj 'a' 0;
print getd .obj 'value' 0;

# Control flow

print "\nTesting control flow:";
if (1 < 2)
{
	print "True!";
};
if (false)
{
	print "If body executing";
}
else
{
	print "Else body executing";
};

print(true else false); # Cursed behavior that comes from `else` being treated as logical OR

# Loops

print "\nTesting while loop:";
.i = 10;
while (.i > 0)
{
	--.i;
	print .i;
};
.i = 10;
while true
{
	if (.i <= 0) break;
	print --.i;
};

print "\nTesting for loop:";
for .i in range 8
{
	print .i;
};

# Functions

print "\nTesting functions:";
function .add [.a, .b]
{
	return (.a + .b);
};
print call .add [1, 5];

print call lambda [.a, .b] {return (.a * .b);} [3, 4]; # Unusual syntax, but works
print call lambda [.a, .b] return (.a * .b) [3, 4];

# Sample of math statements

print "\nTesting math statements:";
print max 1 2;
print sign -1.5;
print(5 / 4);
print(5 // 4);
print(1 + 2);
print(1.0 + 2);
print sin pi;

# Exception handling

try
{
	clamp 0 2 1;
}
catch .e
{
	if (getd .e 'type' '' == 'invalid_argument')
	{
		print "Invalid argument passed to `clamp`";
	}
	else
	{
		throw .e;
	};
};