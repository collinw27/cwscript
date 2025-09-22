from cwscript.constants import *

# Expressions

def _define_expression(e_name, arg_count):

	global _expressions
	_expressions[e_name] = arg_count

def is_expression(e_name):

	return (e_name in _expressions)

def get_arg_count(e_name):

	return _expressions[e_name]

_expressions = {}
_define_expression('print', 1)
_define_expression('max', 2)
_define_expression('if', 2)
_define_expression('do', 1)

# Operators

def _define_op_group(l_to_r, operators):

	global _op_groups
	global _binary_ops
	_op_groups.append([l_to_r, operators.split(' ')])
	_binary_ops += operators.split(' ')

def _define_prefix_op(operator):

	global _prefix_ops
	_prefix_ops.append(operator)

# Returns series of (l_to_r, operators)

def get_op_groups():

	return _op_groups

def get_op_strings():

	return _binary_ops + _prefix_ops

def is_binary_op(op_string):

	return op_string in _binary_ops

def is_prefix_op(op_string):

	return op_string in _prefix_ops

_binary_ops = []
_op_groups = []
_define_op_group(True, '??')
_define_op_group(True, ': ->')
_define_op_group(True, '**')
_define_op_group(True, '* / // %')
_define_op_group(True, '+ -')
_define_op_group(True, '> < >= <= == !=')
_define_op_group(True, '&&')
_define_op_group(True, '||')
_define_op_group(False, '= += -= *= /= //= %= **=')

_prefix_ops = []
_define_prefix_op('-')
_define_prefix_op('!')
_define_prefix_op('++')
_define_prefix_op('--')
_define_prefix_op('!!')

# Misc

def check_group_symbols(first, last):

	return OPENING_GROUPINGS.index(first) == CLOSING_GROUPINGS.index(last)

def assert_type(value, value_type):

	if (not isinstance(value, value_type)):
		raise RuntimeError("Type assertion failed for type %s" % value_type)
	return value