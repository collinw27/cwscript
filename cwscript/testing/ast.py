from cwscript.literal import *

def print_ast(obj):

	_print_ast(obj, 0)

def _print_ast(obj, nesting):

	print(' ' * nesting + str(obj))

	if (isinstance(obj, BlockLiteral)):
		for expression in obj._expression_list:
			_print_ast(expression, nesting + 1)
	elif (isinstance(obj, ExpressionLiteral)):
		for member in obj.__dict__:
			if (member[:1] == '_' and isinstance(obj.__dict__[member], ScriptLiteral)):
				_print_ast(obj.__dict__[member], nesting + 1)