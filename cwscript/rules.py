from cwscript.constants import *
from cwscript.literal import *

# Importing the `literal` package here means that we cannot use
# `rules` in any files that deal with literals
# This is not a problem for now, since `rules` is mostly useful
# for the lexer/parser, but in the case that literals do need this
# in the future, the expression/operator definitions should be moved
# to a separate file to avoid importing `literal` here

# EXPRESSIONS

# Expression arguments are formatted as "name|type"
# Expression arguments can take 3 categories of inputs:
# 1) '*':      Dynamic literals (literals, expressions, operations)
# 2) 'block':  Block literals (the only type of static literal)
# 3) '_':      Keywords (specific to expression definition)

ARG_DYNAMIC = 0
ARG_BLOCK = 1
ARG_KEYWORD = 2

def _define_expression(root, arguments, expression_class):

	global _expressions, _expression_args
	_expressions[root] = expression_class
	_expression_args[root] = []
	for arg in arguments:
		name, type_ = arg.split(': ')
		type_ = ['*', 'block', '_'].index(type_)
		_expression_args[root].append((name, type_))

def is_expression(root):

	return (root in _expressions)

def get_expression_class(root):

	return _expressions[root]

def get_arg_count(root):

	return len(_expression_args[root])

# Returns (name, ARG type)

def get_arg(root, index):

	return _expression_args[root][index]

_expressions = {}
_expression_args = {}

# print [value: string]
_define_expression('print', ['value: *'], PrintExpression)
# max [value_1: int|float] [value_2: int|float]
_define_expression('max', ['value_1: *', 'value_2: *'], MaxExpression)
# if [condition: *] [body: block]
_define_expression('if', ['condition: *', 'body: block'], IfStatementExpression)
# do [body: block]
_define_expression('do', ['body: block'], DoStatementExpression)
# pop [index: int] from [container: *]
_define_expression('pop', ['index: *', 'from: _', 'container: *'], ContainerPopExpression)

# OPERATORS

def _define_op_group(l_to_r, operators, operator_classes):

	global _op_groups
	global _binary_ops
	_op_groups.append([l_to_r, operators.split(' ')])
	for i, op_string in enumerate(operators.split(' ')):
		_binary_ops[op_string] = operator_classes[i]

def _define_prefix_op(operator, operator_class):

	global _prefix_ops
	_prefix_ops[operator] = operator_class

# Returns series of (l_to_r, operators)

def get_op_groups():

	return _op_groups

def get_op_strings():

	return list(_binary_ops.keys()) + list(_prefix_ops.keys())

def is_binary_op(op_string):

	return op_string in _binary_ops.keys()

def is_prefix_op(op_string):

	return op_string in _prefix_ops.keys()

def get_binary_op_class(op_string):

	return _binary_ops[op_string]

def get_prefix_op_class(op_string):

	return _prefix_ops[op_string]

_binary_ops = {}
_op_groups = []
_define_op_group(True, '??', [OperatorChainExpression])
_define_op_group(True, ': ->', [OperatorIndexExpression, OperatorCallExpression])
_define_op_group(True, '**', [OperatorExponentExpression])
_define_op_group(True, '* / // %', [OperatorMultiplyExpression, OperatorFloatDivideExpression, OperatorIntDivideExpression, OperatorModulusExpression])
_define_op_group(True, '+ -', [OperatorAddExpression, OperatorSubtractExpression])
_define_op_group(True, '> < >= <= == !=', [OperatorGreaterExpression, OperatorLessExpression, OperatorGreaterEqualExpression, OperatorLessEqualExpression, OperatorEqualExpression, OperatorUnequalExpression])
_define_op_group(True, '&&', [OperatorAndExpression])
_define_op_group(True, '||', [OperatorOrExpression])
_define_op_group(False, '= += -= *= /= //= %= **=', [OperatorAssignExpression, OperatorAssignAddExpression, OperatorAssignSubtractExpression, OperatorAssignMultiplyExpression, OperatorAssignFloatDivideExpression, OperatorAssignIntDivideExpression, OperatorAssignModulusExpression, OperatorAssignExponentExpression])

_prefix_ops = {}
_define_prefix_op('-', OperatorNegativeExpression)
_define_prefix_op('!', OperatorNotExpression)
_define_prefix_op('++', OperatorIncrementExpression)
_define_prefix_op('--', OperatorDecrementExpression)
_define_prefix_op('!!', OperatorInvertExpression)

# MISC

def check_group_symbols(first, last):

	return OPENING_GROUPINGS.index(first) == CLOSING_GROUPINGS.index(last)

def assert_type(value, value_type):

	if (not isinstance(value, value_type)):
		raise RuntimeError("Type assertion failed for type %s" % value_type)
	return value