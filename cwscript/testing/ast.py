from cwscript.parser.ast import *

def print_ast(obj):

	_print_ast(obj, 0)

def _print_ast(obj, nesting):

	# print("> ", obj)
	if (isinstance(obj, ASTValue)):
		dtype = ["block", "null", "bool", "int", "float", "string", "variable", "list"][obj._dtype]
		print('  ' * nesting + f'VALUE {dtype}')
	else:
		print('  ' * nesting + f'OP {obj._operation}')

	if (obj._dtype == ASTNode.TYPE_BLOCK):
		for expression in obj._value:
			_print_ast(expression, nesting + 1)
	elif (obj._dtype == ASTNode.TYPE_LIST):
		for value in obj._value:
			_print_ast(value, nesting + 1)
	elif (isinstance(obj, ASTOperation)):
		for arg in obj._args.values():
			_print_ast(arg, nesting + 1)