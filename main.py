import sys

from cwscript.program import Program

if (__name__ == '__main__'):

	# Optionally provide a file to use (from command line)
	# Otherwise, use test file

	if (len(sys.argv) < 2):
		code = open('test.cw').read()
	else:
		code = open(sys.argv[1]).read()

	# Continue execution until evaluator runs out of expressions

	program = Program(code)
	while (program.run_next()):
		pass
	print("[Program finished with exit code 0]")