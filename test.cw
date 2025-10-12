
.func = function [.a]
{
	.a = (.a + 2);
	return .a;
	print "This should never print";
};

print (5 + .func -> [1]);

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