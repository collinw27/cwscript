from cwscript.constants import *
from cwscript.expression import *

# Importing the `expression` package here means that we cannot use
# `rules` in any files that deal with expressions
# This is not a problem for now, since `rules` is mostly useful
# for the lexer/parser, but in the case that expressions do need this
# in the future, the statement/operator definitions should be moved
# to a separate file to avoid importing `expression` here

# EXPRESSIONS

# Expression arguments are formatted as "name|type"
# Expression arguments can take 3 categories of inputs:
# 1) '*':      Dynamic expressions (expressions, statements, operations)
# 2) 'block':  Block statements (the only type of static statement)
# 3) '_':      Keywords (specific to statement definition)

ARG_DYNAMIC = 0
ARG_BLOCK = 1
ARG_KEYWORD = 2

def _define_statement(root, arguments, statement_class):

	global _statements, _statement_args
	_statements[root] = statement_class
	_statement_args[root] = []
	for arg in arguments:
		name, type_ = arg.split(': ')
		type_ = ['*', 'block', '_'].index(type_)
		_statement_args[root].append((name, type_))

def is_statement(root):

	return (root in _statements)

def get_statement_class(root):

	return _statements[root]

def get_arg_count(root):

	return len(_statement_args[root])

# Returns (name, ARG type)

def get_arg(root, index):

	return _statement_args[root][index]

_statements = {}
_statement_args = {}

# print [value: string]
_define_statement('print', ['value: *'], PrintStatement)
# max [value_1: int|float] [value_2: int|float]
_define_statement('max', ['value_1: *', 'value_2: *'], MaxStatement)
# if [condition: *] [body: block]
_define_statement('if', ['condition: *', 'body: block'], IfStatement)
# do [body: block]
_define_statement('do', ['body: block'], DoStatement)

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