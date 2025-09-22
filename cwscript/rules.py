from cwscript.constants import *

def _define_expression(e_name, arg_count):

	global _expressions
	_expressions[e_name] = arg_count

def _define_op_group(l_to_r, operators):

	global _op_groups
	global _binary_ops
	_op_groups.append([l_to_r, operators])
	_binary_ops += operators.split(' ')

def _define_prefix_op(operator):

	global _prefix_ops
	_prefix_ops.append(operator)

def get_op_strings():

	return _binary_ops + _prefix_ops

def is_binary_op(op_string):

	return op_string in _binary_ops

def is_prefix_op(op_string):

	return op_string in _prefix_ops

def check_group_symbols(first, last):

	return OPENING_GROUPINGS.index(first) == CLOSING_GROUPINGS.index(last)

def assert_type(value, value_type):

	if (not isinstance(value, value_type)):
		raise RuntimeError("Type assertion failed for type %s" % value_type)
	return value

# Store definitions for operators and expressions

_expressions = {}
_define_expression('print', 1)
_define_expression('max', 2)

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