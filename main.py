import sys

from cwscript.program import Program
from cwscript import rules

if (__name__ == '__main__'):

	# Optionally provide a file to use (from command line)
	# Otherwise, use test file

	if (len(sys.argv) < 2):
		code = open('test.cw').read()
		debug = True
	else:
		code = open(sys.argv[1]).read()
		debug = False

	# Continue execution until evaluator runs out of expressions

	program = Program(code, debug)
	while (program.run_next()):
		pass
	print("[Program finished with exit code %s]" % program.get_exit_code())