
try
{
	.f = function [.a]
	{
		print .a;
		throw new {};
	};
	call .f [1];
}
catch .e
{
	print .e;
	print local;
};