from cwscript.expression.statement.base import *

class BinaryOperatorExpression (StatementExpression):

	def __init__(self, line, inputs):

		super().__init__(line)
		self._operand_1 = inputs['operand_1']
		self._operand_2 = inputs['operand_2']

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

	pass

class OperatorSubtractExpression (BinaryOperatorExpression):

	pass

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

	pass

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
