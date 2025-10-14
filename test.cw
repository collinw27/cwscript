
.print_add = function [.a, .b] {
	print (.a + .b);
};

call .print_add [3, 5];

.func = function [.a]
{
	.a = (.a + 5);
	return .a;
	print "This should never print";
};

print (5 + call .func [10]);

print "\nFor-break test:";
for .i in [2, 4, 6, 8]
{
	if (.i > 4)
	{
		break;
	};
	print .i;
};

print "\nWhile-break test:";
.j = 0;
while true
{
	.j = (.j + 1);
	if (.j > 10)
	{
		break;
	};
	print .j;
};

print "\nFor-continue test:";
for .i in [2, 4, 6, 8]
{
	if (.i == 4)
	{
		continue;
	};
	print .i;
};

print "\nWhile-continue test:";
.j = 0;
while (.j <= 10)
{
	.j = (.j + 1);
	if (.j < 5)
	{
		continue;
	};
	print .j;
};

{
	print "\nBlocks can now be run by themselves.";
};