from cwscript.expression.statement.base import *
from cwscript.expression.dynamic import *
from cwscript.value import *

class PrintStatement (StatementExpression):

	def __init__(self, line, inputs):

		super().__init__(line)
		self._value = inputs['value']

	def _evaluate(self, runner, eval_vars):

		print(self._value.evaluate(runner, ScriptValue).to_string(runner))
		return NullValue(runner)

class MaxStatement (StatementExpression):

	def __init__(self, line, inputs):

		super().__init__(line)
		self._value_1 = inputs['value_1']
		self._value_2 = inputs['value_2']

	def _evaluate(self, runner, eval_vars):

		value_1 = self._value_1.evaluate(runner, NumericValue)
		value_2 = self._value_2.evaluate(runner, NumericValue)
		return value_1 if (value_1.get_value() > value_2.get_value()) else value_2

class IfStatement (StatementExpression):

	def __init__(self, line, inputs):

		super().__init__(line)
		self._condition = inputs['condition']
		self._body = inputs['body']

	def _evaluate(self, runner, eval_vars):

		condition = self._condition.evaluate(runner, ScriptValue).to_bool(runner)

		# Only run the body if the condition is true
		# Return a bool representing whether the body was run or not

		if (condition):
			runner.push_block(self._body)
		return IntValue(runner, int(condition))

class DoStatement (StatementExpression):

	def __init__(self, line, inputs):

		super().__init__(line)
		self._body = inputs['body']

	# Evaluating simply runs the block

	def _evaluate(self, runner, eval_vars):

		runner.push_block(self._body)
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

	def _evaluate(self, runner, eval_vars):

		# Parsing the function parameters is weird because it's essentially a hack
		# In the definition, you write the parameters as a list:
		# [.param_a, .param_b, .param_c]
		# But due to the nature of expressions, the list is evaluated at the time
		# of the function declaration, so these variables names are technically bound
		# to the scope that this statement is run within

		# Instead, the parameters are stored as strings and passed to the FunctionValue
		# A special method of ListExpression is used to do this

		if (not isinstance(self._parameters, ListExpression)):
			raise CWRuntimeError("Could not evaluate function parameter list", self._parameters.get_line())
		parameters = self._parameters.eval_as_parameters(runner)
		return FunctionValue(runner, parameters, self._body)