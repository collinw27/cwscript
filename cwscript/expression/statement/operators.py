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

class OperatorChainExpression (BinaryOperatorExpression):

	pass

class OperatorIndexExpression (BinaryOperatorExpression):

	def get_stack(self, runner, value_type, eval_vars):

		return [
			StackValueRequest(self._operand_1, ContainerValue),
			StackValueRequest(self._operand_2, ScriptValue),
			StackOperation(self, 2, value_type, eval_vars)
		]

	@staticmethod
	def evaluate(runner, args):

		if (isinstance(args[0], ObjectValue)):
			runner.assert_type(args[1], StringValue)
			return VariableValue(runner, args[0], args[1].get_value())
		elif (isinstance(args[0], ListValue)):
			runner.assert_type(args[1], IntValue)
			return VariableValue(runner, args[0], args[1].get_value())
		else:
			raise RuntimeError("Invalid container")

class OperatorCallExpression (BinaryOperatorExpression):

	def get_stack(self, runner, value_type, eval_vars):

		return [
			StackValueRequest(self._operand_1, FunctionValue),
			StackValueRequest(self._operand_2, ListValue),
			StackInterruptableOperation(self, 2, value_type, eval_vars)
		]

	@staticmethod
	def evaluate_special(runner, args, state):

		if (state.get('waiting', True)):

			state['waiting'] = False
			func = args[0]
			arg_values = args[1].get_list()

			# The number of arguments must match the number of parameters in the definition

			parameters = func.get_parameters(runner)
			if (len(parameters) != len(arg_values)):
				raise CWRuntimeError("Wrong number of arguments for function call", runner.get_line())

			# Create a new variable scope, and initialize the function's variables within it

			scope = ObjectValue(runner)
			scope.set_field(runner, '~RET', NullValue(runner))
			for i in range(len(parameters)):
				scope.set_field(runner, parameters[i], arg_values[i])
			runner.add_function_scope(scope)

			# Run the function's body

			return StackBlock(func.get_body())

		else:

			runner.pop_function_scope()
			return NullValue(runner)

	# Handle an interrupt by returning return value

	@staticmethod
	def handle_interrupt_special(runner, interrupt, state):

		# Handle return as expected

		if (isinstance(interrupt, ReturnInterrupt)):
			runner.handle_interrupt()
			return interrupt.value

		# Continue & break cannot propogate past function scope

		elif (isinstance(interrupt, ContinueInterrupt)):
			raise CWRuntimeError("Invalid use of continue", runner.get_line())
		elif (isinstance(interrupt, BreakInterrupt)):
			raise CWRuntimeError("Invalid use of break", runner.get_line())

		# Otherwise, let another expression handle it

		return NullValue(runner)

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

	def get_stack(self, runner, value_type, eval_vars):

		return [
			StackValueRequest(self._operand_1, NumericValue),
			StackValueRequest(self._operand_2, NumericValue),
			StackOperation(self, 2, value_type, eval_vars)
		]

	@staticmethod
	def evaluate(runner, args):

		return _op_add(runner, args[0], args[1])

class OperatorSubtractExpression (BinaryOperatorExpression):

	def get_stack(self, runner, value_type, eval_vars):

		return [
			StackValueRequest(self._operand_1, NumericValue),
			StackValueRequest(self._operand_2, NumericValue),
			StackOperation(self, 2, value_type, eval_vars)
		]

	@staticmethod
	def evaluate(runner, args):
		
		return _op_subtract(runner, args[0], args[1])

class OperatorGreaterExpression (BinaryOperatorExpression):

	def get_stack(self, runner, value_type, eval_vars):

		return [
			StackValueRequest(self._operand_1, NumericValue),
			StackValueRequest(self._operand_2, NumericValue),
			StackOperation(self, 2, value_type, eval_vars)
		]

	@staticmethod
	def evaluate(runner, args):
		
		return BoolValue(runner, args[0].get_value() > args[1].get_value())

class OperatorLessExpression (BinaryOperatorExpression):

	def get_stack(self, runner, value_type, eval_vars):

		return [
			StackValueRequest(self._operand_1, NumericValue),
			StackValueRequest(self._operand_2, NumericValue),
			StackOperation(self, 2, value_type, eval_vars)
		]

	@staticmethod
	def evaluate(runner, args):
		
		return BoolValue(runner, args[0].get_value() < args[1].get_value())

class OperatorGreaterEqualExpression (BinaryOperatorExpression):

	def get_stack(self, runner, value_type, eval_vars):

		return [
			StackValueRequest(self._operand_1, NumericValue),
			StackValueRequest(self._operand_2, NumericValue),
			StackOperation(self, 2, value_type, eval_vars)
		]

	@staticmethod
	def evaluate(runner, args):
		
		return BoolValue(runner, args[0].get_value() >= args[1].get_value())

class OperatorLessEqualExpression (BinaryOperatorExpression):

	def get_stack(self, runner, value_type, eval_vars):

		return [
			StackValueRequest(self._operand_1, NumericValue),
			StackValueRequest(self._operand_2, NumericValue),
			StackOperation(self, 2, value_type, eval_vars)
		]

	@staticmethod
	def evaluate(runner, args):
		
		return BoolValue(runner, args[0].get_value() <= args[1].get_value())

class OperatorEqualExpression (BinaryOperatorExpression):

	def get_stack(self, runner, value_type, eval_vars):

		return [
			StackValueRequest(self._operand_1, ScriptValue),
			StackValueRequest(self._operand_2, ScriptValue),
			StackOperation(self, 2, value_type, eval_vars)
		]

	@staticmethod
	def evaluate(runner, args):
		
		return BoolValue(runner, args[0].is_equal(runner, args[1]))

class OperatorUnequalExpression (BinaryOperatorExpression):

	def get_stack(self, runner, value_type, eval_vars):

		return [
			StackValueRequest(self._operand_1, ScriptValue),
			StackValueRequest(self._operand_2, ScriptValue),
			StackOperation(self, 2, value_type, eval_vars)
		]

	@staticmethod
	def evaluate(runner, args):
		
		return BoolValue(runner, not args[0].is_equal(runner, args[1]))

class OperatorAndExpression (BinaryOperatorExpression):

	pass

class OperatorOrExpression (BinaryOperatorExpression):

	pass

class OperatorAssignExpression (BinaryOperatorExpression):

	def get_stack(self, runner, value_type, eval_vars):

		return [
			StackValueRequest(self._operand_1, VariableValue, False),
			StackValueRequest(self._operand_2, ScriptValue),
			StackOperation(self, 2, value_type, eval_vars)
		]	

	@staticmethod
	def evaluate(runner, args):

		args[0].set_var_value(runner, args[1])
		return args[0]

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
