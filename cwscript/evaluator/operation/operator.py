from cwscript.evaluator.operation.base import *
from cwscript.evaluator.operation.base import _ArgRequest as ArgRequest
from cwscript.evaluator.value import *

# Helper methods for arithmetic

def _is_float_op(value_1, value_2):

	return (isinstance(value_1, FloatValue) or isinstance(value_2, FloatValue))

# Add two numeric values
# Later, will also support list concatenation
# Uses integer arithmetic unless float is present
# Assumes inputs are valid

def _op_add(evaluator, operand_1, operand_2):

	if (_is_float_op(operand_1, operand_2)):
		return FloatValue(evaluator, operand_1.get_value() + operand_2.get_value())
	else:
		return IntValue(evaluator, operand_1.get_value() + operand_2.get_value())

# Uses integer arithmetic unless float is present
# Assumes inputs are valid

def _op_subtract(evaluator, operand_1, operand_2):

	if (_is_float_op(operand_1, operand_2)):
		return FloatValue(evaluator, operand_1.get_value() - operand_2.get_value())
	else:
		return IntValue(evaluator, operand_1.get_value() - operand_2.get_value())

class OperatorChain (StackBasicOperation):

	pass

class OperatorIndex (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('op_1', ContainerValue),
			ArgRequest('op_2', ScriptValue)
		]

	def _finish(self, evaluator, args):

		if (isinstance(args[0], ObjectValue)):
			evaluator.assert_type(args[1], StringValue)
			return VariableValue(evaluator, args[0], args[1].get_value())
		elif (isinstance(args[0], ListValue)):
			evaluator.assert_type(args[1], IntValue)
			return VariableValue(evaluator, args[0], args[1].get_value())
		else:
			raise RuntimeError("Invalid container")

class OperatorCall (StackBasicOperation):

	pass

class OperatorExponent (StackBasicOperation):

	pass

class OperatorMultiply (StackBasicOperation):

	pass

class OperatorFloatDivide (StackBasicOperation):

	pass

class OperatorIntDivide (StackBasicOperation):

	pass

class OperatorModulus (StackBasicOperation):

	pass

class OperatorAdd (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('op_1', NumericValue),
			ArgRequest('op_2', NumericValue)
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

		return BoolValue(evaluator, args[0].is_equal(evaluator, args[1]))

class OperatorAnd (StackBasicOperation):

	pass

class OperatorOr (StackBasicOperation):

	pass

class OperatorAssign (StackBasicOperation):

	def _define_args(self):

		return [
			ArgRequest('op_1', VariableValue, False),
			ArgRequest('op_2', ScriptValue)
		]

	def _finish(self, evaluator, args):

		args[0].set_var_value(evaluator, args[1])
		return args[0]

class OperatorAssignAdd (StackBasicOperation):

	pass

class OperatorAssignSubtract (StackBasicOperation):

	pass

class OperatorAssignMultiply (StackBasicOperation):

	pass

class OperatorAssignFloatDivide (StackBasicOperation):

	pass

class OperatorAssignIntDivide (StackBasicOperation):

	pass

class OperatorAssignModulus (StackBasicOperation):

	pass

class OperatorAssignExponent (StackBasicOperation):

	pass

class OperatorNegative (StackBasicOperation):

	pass

class OperatorNot (StackBasicOperation):

	pass

class OperatorIncrement (StackBasicOperation):

	pass

class OperatorDecrement (StackBasicOperation):

	pass

class OperatorInvert (StackBasicOperation):

	pass