from cwscript.expression.statement.base import *
from cwscript.value import *

# Helper methods for arithmetic

def _is_all_int(value_1, value_2):

	return (isinstance(value_1, IntValue) and isinstance(value_2, IntValue))

# Add two numeric values
# Later, will also support list concatenation
# Uses integer arithmetic unless float is present
# Assumes inputs are valid

def _op_add(runner, operand_1, operand_2):

	if (_is_all_int(operand_1, operand_2)):
		return IntValue(runner, operand_1.get_value() + operand_2.get_value())
	else:
		return FloatValue(runner, operand_1.get_value() + operand_2.get_value())

# Uses integer arithmetic unless float is present
# Assumes inputs are valid

def _op_subtract(runner, operand_1, operand_2):

	if (_is_all_int(operand_1, operand_2)):
		return IntValue(runner, operand_1.get_value() - operand_2.get_value())
	else:
		return FloatValue(runner, operand_1.get_value() - operand_2.get_value())

class BinaryOperatorExpression (StatementExpression):

	def __init__(self, line, inputs):

		super().__init__(line)
		self._operand_1 = inputs['operand_1']
		self._operand_2 = inputs['operand_2']

	def _evaluate(self, runner, eval_vars):

		return NullValue(runner)

class OperatorChainExpression (BinaryOperatorExpression):

	pass

class OperatorIndexExpression (BinaryOperatorExpression):

	pass

class OperatorCallExpression (BinaryOperatorExpression):

	pass

class OperatorExponentExpression (BinaryOperatorExpression):

	pass

class OperatorMultiplyExpression (BinaryOperatorExpression):

	pass

class OperatorFloatDivideExpression (BinaryOperatorExpression):

	pass

class OperatorIntDivideExpression (BinaryOperatorExpression):

	pass

class OperatorModulusExpression (BinaryOperatorExpression):

	pass

class OperatorAddExpression (BinaryOperatorExpression):

	def _evaluate(self, runner, eval_vars):
		
		operand_1 = self._operand_1.evaluate(runner, NumericValue)
		operand_2 = self._operand_2.evaluate(runner, NumericValue)
		return _op_add(runner, operand_1, operand_2)

class OperatorSubtractExpression (BinaryOperatorExpression):

	def _evaluate(self, runner, eval_vars):
		
		operand_1 = self._operand_1.evaluate(runner, NumericValue)
		operand_2 = self._operand_2.evaluate(runner, NumericValue)
		return _op_subtract(runner, operand_1, operand_2)

class OperatorGreaterExpression (BinaryOperatorExpression):

	pass

class OperatorLessExpression (BinaryOperatorExpression):

	pass

class OperatorGreaterEqualExpression (BinaryOperatorExpression):

	pass

class OperatorLessEqualExpression (BinaryOperatorExpression):

	pass

class OperatorEqualExpression (BinaryOperatorExpression):

	pass

class OperatorUnequalExpression (BinaryOperatorExpression):

	pass

class OperatorAndExpression (BinaryOperatorExpression):

	pass

class OperatorOrExpression (BinaryOperatorExpression):

	pass

class OperatorAssignExpression (BinaryOperatorExpression):

	def _evaluate(self, runner, eval_vars):

		operand_1 = self._operand_1.evaluate(runner, VariableValue, False)
		operand_2 = self._operand_2.evaluate(runner, ScriptValue)
		operand_1.set_var_value(runner, operand_2)
		return operand_1

class OperatorAssignAddExpression (BinaryOperatorExpression):

	pass

class OperatorAssignSubtractExpression (BinaryOperatorExpression):

	pass

class OperatorAssignMultiplyExpression (BinaryOperatorExpression):

	pass

class OperatorAssignFloatDivideExpression (BinaryOperatorExpression):

	pass

class OperatorAssignIntDivideExpression (BinaryOperatorExpression):

	pass

class OperatorAssignModulusExpression (BinaryOperatorExpression):

	pass

class OperatorAssignExponentExpression (BinaryOperatorExpression):

	pass

class PrefixOperatorExpression (StatementExpression):

	def __init__(self, line, inputs):

		super().__init__(line)
		self._operand = inputs['operand']

	def _evaluate(self, runner, eval_vars):
		
		return NullValue(runner)

class OperatorNegativeExpression (PrefixOperatorExpression):

	pass

class OperatorNotExpression (PrefixOperatorExpression):

	pass

class OperatorIncrementExpression (PrefixOperatorExpression):

	pass

class OperatorDecrementExpression (PrefixOperatorExpression):

	pass

class OperatorInvertExpression (PrefixOperatorExpression):

	pass
