from math import trunc

from cwscript.evaluator.operation.base import *
from cwscript.evaluator.operation.base import _ArgRequest as ArgRequest
from cwscript.evaluator.value import *

# Helper function for arithmetic
# Many functions use integer arithmetic unless float is present
# Bools act as though they were integers

def _is_float_op(value_1, value_2):

	return (isinstance(value_1, FloatValue) or isinstance(value_2, FloatValue))

def _binary_op_class(value_1, value_2):

	return FloatValue if (isinstance(value_1, FloatValue) or isinstance(value_2, FloatValue)) else IntValue

def _prefix_op_class(value):

	return FloatValue if (isinstance(value, FloatValue)) else IntValue

# Add two numeric values
# Also supports string and list concatenation
# Uses integer arithmetic unless float is present
# Assumes inputs are valid

def _op_add(evaluator, op_1, op_2):

	if (isinstance(op_1, NumericValue)):
		evaluator.assert_type(op_2, NumericValue)
		return _binary_op_class(op_1, op_2)(evaluator, op_1.get_value() + op_2.get_value())
	elif (isinstance(op_1, StringValue)):
		evaluator.assert_type(op_2, StringValue)
		return StringValue(evaluator, op_1.get_value() + op_2.get_value())
	elif (isinstance(op_1, ListValue)):
		evaluator.assert_type(op_2, ListValue)
		return ListValue(evaluator, op_1.get_list() + op_2.get_list())
	else:
		evaluator.unmatched_type_error(op_1, [NumericValue, StringValue, ListValue])

# Uses integer arithmetic unless float is present
# Assumes inputs are valid

def _op_subtract(evaluator, op_1, op_2):

	return _binary_op_class(op_1, op_2)(evaluator, op_1.get_value() - op_2.get_value())

def _op_multiply(evaluator, op_1, op_2):

	return _binary_op_class(op_1, op_2)(evaluator, op_1.get_value() * op_2.get_value())

# Float divide always returns a float,
# even if an integer result doesn't lose precision

def _op_float_divide(evaluator, op_1, op_2):

	if (op_2.get_value() == 0):
		raise CatchableError('zero_division', "Division by zero")
	return FloatValue(evaluator, op_1.get_value() / op_2.get_value())

# Int divide (unsurprisingly) always returns an int
# Any decimal result is truncated towards 0

def _op_int_divide(evaluator, op_1, op_2):

	if (op_2.get_value() == 0):
		raise CatchableError('zero_division', "Division by zero")
	return IntValue(evaluator, trunc(op_1.get_value() / op_2.get_value()))

# Float modulus is allowed
# Luckily, this is natively supported by Python

def _op_modulus(evaluator, op_1, op_2):

	if (op_2.get_value() == 0):
		raise CatchableError('zero_division', "Division by zero")
	return _binary_op_class(op_1, op_2)(evaluator, op_1.get_value() % op_2.get_value())

# Unlike other operations, two integers return a float if
# the exponent is <0

def _op_exponent(evaluator, op_1, op_2):

	if (op_1.get_value() == 0 and op_2.get_value() < 0):
		raise CatchableError('zero_division', "Division by zero")
	if (_is_float_op(op_1, op_2)):
		return FloatValue(evaluator, op_1.get_value() ** op_2.get_value())
	else:
		if (op_2.get_value() >= 0):
			return IntValue(evaluator, op_1.get_value() ** op_2.get_value())
		else:
			return FloatValue(evaluator, op_1.get_value() ** op_2.get_value())

# Accepts containers or strings
# Containers return a VariableValue, and can therefore be used
# to modify the given index
# Strings on the other hand can only read, and thus return a string

class OperatorIndex (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('op_1', ScriptValue),
			ArgRequest('op_2', ScriptValue)
		]

	def _finish(self, evaluator, args):

		if (isinstance(args[0], ObjectValue)):
			evaluator.assert_type(args[1], StringValue)
			return VariableValue(evaluator, args[0], [args[1].get_value()])
		elif (isinstance(args[0], ListValue)):
			evaluator.assert_type(args[1], IntegerValue)
			return VariableValue(evaluator, args[0], [args[1].get_value()])
		elif (isinstance(args[0], StringValue)):
			evaluator.assert_type(args[1], IntegerValue)
			string = args[0].get_value()
			index = args[1].get_value()
			if not (-len(string) <= index < len(string)):
				raise CatchableError('invalid_index', "String index %s out of bounds" % index)
			return StringValue(evaluator, string[index])
		else:
			evaluator.unmatched_type_error(args[0], [StringValue, ContainerValue])

class OperatorExponent (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('op_1', NumericValue),
			ArgRequest('op_2', NumericValue)
		]

	def _finish(self, evaluator, args):

		return _op_exponent(evaluator, args[0], args[1])

class OperatorMultiply (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('op_1', NumericValue),
			ArgRequest('op_2', NumericValue)
		]

	def _finish(self, evaluator, args):

		return _op_multiply(evaluator, args[0], args[1])

class OperatorFloatDivide (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('op_1', NumericValue),
			ArgRequest('op_2', NumericValue)
		]

	def _finish(self, evaluator, args):

		return _op_float_divide(evaluator, args[0], args[1])

class OperatorIntDivide (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('op_1', NumericValue),
			ArgRequest('op_2', NumericValue)
		]

	def _finish(self, evaluator, args):

		return _op_int_divide(evaluator, args[0], args[1])

class OperatorModulus (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('op_1', NumericValue),
			ArgRequest('op_2', NumericValue)
		]

	def _finish(self, evaluator, args):

		return _op_modulus(evaluator, args[0], args[1])

class OperatorAdd (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('op_1', ScriptValue),
			ArgRequest('op_2', ScriptValue)
		]

	def _finish(self, evaluator, args):

		return _op_add(evaluator, args[0], args[1])

class OperatorSubtract (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('op_1', NumericValue),
			ArgRequest('op_2', NumericValue)
		]

	def _finish(self, evaluator, args):

		return _op_subtract(evaluator, args[0], args[1])

class OperatorGreater (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('op_1', NumericValue),
			ArgRequest('op_2', NumericValue)
		]

	def _finish(self, evaluator, args):

		return BoolValue(evaluator, args[0].get_value() > args[1].get_value())

class OperatorLess (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('op_1', NumericValue),
			ArgRequest('op_2', NumericValue)
		]

	def _finish(self, evaluator, args):

		return BoolValue(evaluator, args[0].get_value() < args[1].get_value())

class OperatorGreaterEqual (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('op_1', NumericValue),
			ArgRequest('op_2', NumericValue)
		]

	def _finish(self, evaluator, args):

		return BoolValue(evaluator, args[0].get_value() >= args[1].get_value())

class OperatorLessEqual (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('op_1', NumericValue),
			ArgRequest('op_2', NumericValue)
		]

	def _finish(self, evaluator, args):

		return BoolValue(evaluator, args[0].get_value() <= args[1].get_value())

class OperatorEqual (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('op_1', ScriptValue),
			ArgRequest('op_2', ScriptValue)
		]

	def _finish(self, evaluator, args):

		return BoolValue(evaluator, args[0].is_equal(evaluator, args[1]))

class OperatorUnequal (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('op_1', ScriptValue),
			ArgRequest('op_2', ScriptValue)
		]

	def _finish(self, evaluator, args):

		return BoolValue(evaluator, not args[0].is_equal(evaluator, args[1]))

class OperatorSame (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('op_1', ScriptValue),
			ArgRequest('op_2', ScriptValue)
		]

	def _finish(self, evaluator, args):

		return BoolValue(evaluator, args[0].is_same(evaluator, args[1]))

class OperatorNotSame (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('op_1', ScriptValue),
			ArgRequest('op_2', ScriptValue)
		]

	def _finish(self, evaluator, args):

		return BoolValue(evaluator, not args[0].is_same(evaluator, args[1]))

# Since logical operators need to handle short-circuit evaluation,
# they define their own implentation of StackOperation

class OperatorAnd (StackOperation):

	def __init__(self, args, line, value_type, eval_vars):

		super().__init__(line, value_type, eval_vars)
		self._args = args
		self._step = 0

	def _evaluate(self, evaluator, last_value):

		if (self._step == 0):
			evaluator.request_value(self._args['op_1'], ScriptValue)
		elif (self._step == 1):
			if (not last_value.to_bool(evaluator)):
				return BoolValue(evaluator, False)
			else:
				evaluator.request_value(self._args['op_2'], ScriptValue)
		else:
			return BoolValue(evaluator, last_value.to_bool(evaluator))
		self._step += 1

# Due to the nature of short circuit evaluation, OR can also be used
# as an equivalent to if-else
# if (){block_1} || {block_2}; will only run block_2 if block_1 is not run
# This can be chained an arbitrary number of times:
# if (){} || if (){} || if (){} || {};
# In the lexer, `else` is quitely replaced with `||`

class OperatorOr (StackOperation):

	def __init__(self, args, line, value_type, eval_vars):

		super().__init__(line, value_type, eval_vars)
		self._args = args
		self._step = 0

	def _evaluate(self, evaluator, last_value):

		if (self._step == 0):
			evaluator.request_value(self._args['op_1'], ScriptValue)
		elif (self._step == 1):
			if (last_value.to_bool(evaluator)):
				return BoolValue(evaluator, True)
			else:
				evaluator.request_value(self._args['op_2'], ScriptValue)
		else:
			return BoolValue(evaluator, last_value.to_bool(evaluator))
		self._step += 1

class OperatorAssign (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('op_1', VariableValue, False),
			ArgRequest('op_2', ScriptValue)
		]

	def _finish(self, evaluator, args):

		args[0].set_var_value(evaluator, args[1])
		return args[0]

# Type checking performed in _op add to also support concatenation

class OperatorAssignAdd (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('op_1', VariableValue, False),
			ArgRequest('op_2', ScriptValue)
		]

	def _finish(self, evaluator, args):

		current = args[0].get_var_value(evaluator)
		args[0].set_var_value(evaluator, _op_add(evaluator, current, args[1]))
		return args[0]

class OperatorAssignSubtract (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('op_1', VariableValue, False),
			ArgRequest('op_2', NumericValue)
		]

	def _finish(self, evaluator, args):

		current = evaluator.assert_type(args[0].get_var_value(evaluator), NumericValue)
		args[0].set_var_value(evaluator, _op_subtract(evaluator, current, args[1]))
		return args[0]

class OperatorAssignMultiply (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('op_1', VariableValue, False),
			ArgRequest('op_2', NumericValue)
		]

	def _finish(self, evaluator, args):

		current = evaluator.assert_type(args[0].get_var_value(evaluator), NumericValue)
		args[0].set_var_value(evaluator, _op_multiply(evaluator, current, args[1]))
		return args[0]

class OperatorAssignFloatDivide (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('op_1', VariableValue, False),
			ArgRequest('op_2', NumericValue)
		]

	def _finish(self, evaluator, args):

		current = evaluator.assert_type(args[0].get_var_value(evaluator), NumericValue)
		args[0].set_var_value(evaluator, _op_float_divide(evaluator, current, args[1]))
		return args[0]

class OperatorAssignIntDivide (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('op_1', VariableValue, False),
			ArgRequest('op_2', NumericValue)
		]

	def _finish(self, evaluator, args):

		current = evaluator.assert_type(args[0].get_var_value(evaluator), NumericValue)
		args[0].set_var_value(evaluator, _op_int_divide(evaluator, current, args[1]))
		return args[0]

class OperatorAssignModulus (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('op_1', VariableValue, False),
			ArgRequest('op_2', NumericValue)
		]

	def _finish(self, evaluator, args):

		current = evaluator.assert_type(args[0].get_var_value(evaluator), NumericValue)
		args[0].set_var_value(evaluator, _op_modulus(evaluator, current, args[1]))
		return args[0]

class OperatorAssignExponent (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('op_1', VariableValue, False),
			ArgRequest('op_2', NumericValue)
		]

	def _finish(self, evaluator, args):

		current = evaluator.assert_type(args[0].get_var_value(evaluator), NumericValue)
		args[0].set_var_value(evaluator, _op_exponent(evaluator, current, args[1]))
		return args[0]

class OperatorNegative (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('op', NumericValue)
		]

	def _finish(self, evaluator, args):

		return _prefix_op_class(args[0])(evaluator, args[0].get_value() * -1)

class OperatorNot (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('op', ScriptValue)
		]

	def _finish(self, evaluator, args):

		return BoolValue(evaluator, not args[0].to_bool(evaluator))

class OperatorIncrement (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('op', VariableValue, False)
		]

	def _finish(self, evaluator, args):

		current = evaluator.assert_type(args[0].get_var_value(evaluator), NumericValue)
		args[0].set_var_value(evaluator, _prefix_op_class(current)(evaluator, current.get_value() + 1))
		return args[0]

class OperatorDecrement (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('op', VariableValue, False)
		]

	def _finish(self, evaluator, args):

		current = evaluator.assert_type(args[0].get_var_value(evaluator), NumericValue)
		args[0].set_var_value(evaluator, _prefix_op_class(current)(evaluator, current.get_value() - 1))
		return args[0]

class OperatorInvert (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('op', VariableValue, False)
		]

	def _finish(self, evaluator, args):

		args[0].set_var_value(evaluator, BoolValue(evaluator, not args[0].get_var_value(evaluator).to_bool(evaluator)))
		return args[0]