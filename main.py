import sys

from cwscript.runner.code_runner import CodeRunner
from cwscript.testing.ast import print_ast

if (__name__ == '__main__'):

	if (len(sys.argv) < 2):
		code = open('test.cw').read()
	else:
		code = open(sys.argv[1]).read()

	code_runner = CodeRunner(code)
	while (True):
		if (not code_runner.run_next()):
			break

	print("[Program finished with exit code 0]")