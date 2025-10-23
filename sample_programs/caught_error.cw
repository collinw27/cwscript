
try
{
	++1;
}
catch .e
{
	if (getd .e 'type' '' == 'invalid_type')
	{
		print .e;
	}
	||
	{
		throw .e;
	};
};
print "Finished";