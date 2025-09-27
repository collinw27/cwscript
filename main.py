import sys

from cwscript.code_runner import CodeRunner

if (__name__ == '__main__'):

	if (len(sys.argv) < 2):
		code = open('test.cw').read()
	else:
		code = open(sys.argv[1]).read()
	print(code)
	print()
	code_runner = CodeRunner(code)