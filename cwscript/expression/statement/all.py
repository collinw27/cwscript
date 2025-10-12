from cwscript.expression.statement.base import *
from cwscript.expression.dynamic import *
from cwscript.value import *

class PrintStatement (StatementExpression):

	def __init__(self, line, inputs):

		super().__init__(line)
		self._value = inputs['value']

	def get_stack(self, runner, value_type, eval_vars):

		return [
			StackValueRequest(self._value, ScriptValue),
			StackOperation(self, 1, value_type, eval_vars)
		]

	@staticmethod
	def evaluate(runner, args):

		print(args[0].to_string(runner))
		return NullValue(runner)

class MaxStatement (StatementExpression):

	def __init__(self, line, inputs):

		super().__init__(line)
		self._value_1 = inputs['value_1']
		self._value_2 = inputs['value_2']

	def get_stack(self, runner, value_type, eval_vars):

		return [
			StackValueRequest(self._value_1, NumericValue),
			StackValueRequest(self._value_2, NumericValue),
			StackOperation(self, 2, value_type, eval_vars)
		]

	@staticmethod
	def evaluate(runner, args):

		return args[0] if (args[0].get_value() > args[1].get_value()) else args[1]

class IfStatement (StatementExpression):

	def __init__(self, line, inputs):

		super().__init__(line)
		self._condition = inputs['condition']
		self._body = inputs['body']

	def get_stack(self, runner, value_type, eval_vars):

		# Runs regardless of conditional, need short-circuit evaluation to fix

		return [
			StackValueRequest(self._condition, ScriptValue),
			StackInterruptableOperation(self, 1, value_type, eval_vars, {'block': self._body})
		]

	@staticmethod
	def evaluate(runner, args, state):

		if (args[0].to_bool(runner) and state.get('waiting', True)):
			state['waiting'] = False
			return StackBlock(state['block'])
		else:
			return IntValue(runner, int(args[0].to_bool(runner)))

class DoStatement (StatementExpression):

	def __init__(self, line, inputs):

		super().__init__(line)
		self._body = inputs['body']

	def get_stack(self, runner, value_type, eval_vars):

		# An InterruptableOperation isn't used since the block
		# is run once and unconditionally, so no setup is needed

		return [
			StackBlock(self._body),
			StackOperation(self, 0, value_type, eval_vars)
		]

	@staticmethod
	def evaluate(runner, args):

		return IntValue(runner, 1)

# In the previous iteration of this project
# functions were automatically 'bound' to the current object
# Since I'm not sure how 'binding' functions will work in the future,
# they're left out of this class for now

class FunctionStatement (StatementExpression):

	def __init__(self, line, inputs):

		super().__init__(line)
		self._parameters = inputs['parameters']
		self._body = inputs['body']

	def get_stack(self, runner, value_type, eval_vars):

		# Parsing the function parameters is weird because it's essentially a hack
		# In the definition, you write the parameters as a list:
		# [.param_a, .param_b, .param_c]
		# But due to the nature of expressions, the list is evaluated at the time
		# of the function declaration, so these variables names are technically bound
		# to the scope that this statement is run within

		# Instead, the parameters are stored as strings and passed to the FunctionValue
		# A special method of ListExpression is used to do this
		# Since there's no possibility of nested expressions, these can all be evaluated
		# in this function call without being passed to `evaluate()`, just like a literal

		if (not isinstance(self._parameters, ListExpression)):
			raise CWRuntimeError("Could not evaluate function parameter list", self._parameters.get_line())
		parameters = self._parameters.eval_as_parameters(runner)
		return [StackValue(runner.assert_type(FunctionValue(runner, parameters, self._body), value_type))]