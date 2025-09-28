from cwscript.expression.statement.base import *
from cwscript.value import *

class PrintStatement (StatementExpression):

	def __init__(self, line, inputs):

		super().__init__(line)
		self._value = inputs['value']

	def _evaluate(self, runner, eval_vars):

		print(self._value.evaluate(runner, ScriptValue).to_string())

class MaxStatement (StatementExpression):

	def __init__(self, line, inputs):

		super().__init__(line)
		self._value_1 = inputs['value_1']
		self._value_2 = inputs['value_2']

class IfStatementStatement (StatementExpression):

	def __init__(self, line, inputs):

		super().__init__(line)
		self._condition = inputs['condition']
		self._body = inputs['body']

class DoStatementStatement (StatementExpression):

	def __init__(self, line, inputs):

		super().__init__(line)
		self._body = inputs['body']

	# Evaluating simply runs the block

	def _evaluate(self, runner, eval_vars):

		runner.push_block(self._body)

class ContainerPopStatement (StatementExpression):

	def __init__(self, line, inputs):

		super().__init__(line)
		self._index = inputs['index']
		self._container = inputs['container']