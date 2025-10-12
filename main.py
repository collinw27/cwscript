import sys

from cwscript.runner.code_runner import CodeRunner

if (__name__ == '__main__'):

	if (len(sys.argv) < 2):
		code = open('test.cw').read()
	else:
		code = open(sys.argv[1]).read()

	code_runner = CodeRunner(code)
	while (code_runner.run_next()):
		pass

	print("[Program finished with exit code 0]")