from cwscript.code_runner import CodeRunner

if (__name__ == '__main__'):

	file = 'test.cw'
	code = open(file).read()
	print(code)
	code_runner = CodeRunner(code)