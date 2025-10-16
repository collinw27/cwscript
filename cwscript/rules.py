from cwscript.constants import *
from cwscript.evaluator.operation import *

# Importing the `operation` package here means that we cannot use
# `rules` in any files that deal with statements/operations
# This is not a problem for now, since `rules` is mostly useful
# for the lexer/parser, but in the case that operators do need this
# in the future, the statement/operator definitions should be moved
# to a separate file to avoid importing `operation` here

# STATEMENTS

# Statement arguments are formatted as "name|is_keyword"

def _define_statement(root, arguments, statement_class):

	global _statements, _statement_args
	_statements[root] = statement_class
	_statement_args[root] = []
	for arg in arguments:
		is_keyword = '|KEYWORD' in arg
		name = arg[:-8] if is_keyword else arg
		_statement_args[root].append((name, is_keyword))

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
_define_statement('print', ['value'], PrintStatement)
# local
_define_statement('local', [], LocalScopeStatement)
# global
_define_statement('global', [], GlobalScopeStatement)
# if [condition: *] [body: block]
_define_statement('if', ['condition', 'body'], IfStatement)
# while [condition: *] [body: block]
_define_statement('while', ['condition', 'body'], WhileLoopStatement)
# for [iterator: var] in [list: list] [body: block]
_define_statement('for', ['iterator', 'in|KEYWORD', 'list', 'body'], ForLoopStatement)
# continue [value: *]
_define_statement('continue', [], ContinueStatement)
# break [value: *]
_define_statement('break', [], BreakStatement)
# len [value: string|container]
_define_statement('len', ['value'], LengthStatement)
# slice [value: string|list] [start: int] [end: int]
_define_statement('slice', ['value', 'start', 'end'], SliceStatement)
# slice_after [value: string|list] [start: int] [end: int]
_define_statement('slice_after', ['value', 'start'], SliceAfterStatement)
# find [source: string|container] [value: *]
_define_statement('find', ['source', 'value'], FindStatement)
# replace [source: string] [old: string] with [new: string]
_define_statement('replace', ['source', 'old', 'with|KEYWORD', 'new'], StringReplaceStatement)
# upper [source: string]
_define_statement('upper', ['source'], StringUpperCaseStatement)
# lower [source: string]
_define_statement('lower', ['source'], StringLowerCaseStatement)
# merge [list_1: list] [list_2: list]
_define_statement('merge', ['list_1', 'list_2'], ListMergeStatement)
# pop [source: container] [index: *]
_define_statement('pop', ['source', 'index'], ContainerPopStatement)
# range [end: int]
_define_statement('range', ['end'], RangeStatement)
# adv_range [end: int]
_define_statement('adv_range', ['start', 'end', 'step'], AdvancedRangeStatement)
# function [parameters: list] [body: block]
_define_statement('function', ['parameters', 'body'], FunctionStatement)
# return [value: *]
_define_statement('return', ['value'], ReturnStatement)
# call [function: function] [args: list]
_define_statement('call', ['function', 'args'], CallStatement)
# object [body: block]
_define_statement('object', ['body'], ObjectStatement)
# o_keys [object: object]
_define_statement('o_keys', ['object'], ObjectKeysStatement)
# o_values [object: object]
_define_statement('o_values', ['object'], ObjectValuesStatement)
# max [value_1: int|float] [value_2: int|float]
_define_statement('max', ['value_1', 'value_2'], MaxStatement)
# min [value_1: int|float] [value_2: int|float]
_define_statement('min', ['value_1', 'value_2'], MinStatement)

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
_define_op_group(True, ':', [OperatorIndex])
_define_op_group(True, '**', [OperatorExponent])
_define_op_group(True, '* / // %', [OperatorMultiply, OperatorFloatDivide, OperatorIntDivide, OperatorModulus])
_define_op_group(True, '+ -', [OperatorAdd, OperatorSubtract])
_define_op_group(True, '> < >= <= == !=', [OperatorGreater, OperatorLess, OperatorGreaterEqual, OperatorLessEqual, OperatorEqual, OperatorUnequal])
_define_op_group(True, '&&', [OperatorAnd])
_define_op_group(True, '||', [OperatorOr])
_define_op_group(False, '= += -= *= /= //= %= **=', [OperatorAssign, OperatorAssignAdd, OperatorAssignSubtract, OperatorAssignMultiply, OperatorAssignFloatDivide, OperatorAssignIntDivide, OperatorAssignModulus, OperatorAssignExponent])

_prefix_ops = {}
_define_prefix_op('-', OperatorNegative)
_define_prefix_op('!', OperatorNot)
_define_prefix_op('++', OperatorIncrement)
_define_prefix_op('--', OperatorDecrement)
_define_prefix_op('!!', OperatorInvert)

# MISC

def check_group_symbols(first, last):

	return OPENING_GROUPINGS.index(first) == CLOSING_GROUPINGS.index(last)