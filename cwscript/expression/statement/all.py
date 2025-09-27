from cwscript.expression.statement.base import *

class PrintStatement (StatementExpression):

	def __init__(self, line, inputs):

		super().__init__(line)
		self._value = inputs['value']

	def print_ast(self, nesting):

		super().print_ast(nesting)
		self._value.print_ast(nesting + 1)

class MaxStatement (StatementExpression):

	def __init__(self, line, inputs):

		super().__init__(line)
		self._value_1 = inputs['value_1']
		self._value_2 = inputs['value_2']

	def print_ast(self, nesting):

		super().print_ast(nesting)
		self._value_1.print_ast(nesting + 1)
		self._value_2.print_ast(nesting + 1)

class IfStatementStatement (StatementExpression):

	def __init__(self, line, inputs):

		super().__init__(line)
		self._condition = inputs['condition']
		self._body = inputs['body']

	def print_ast(self, nesting):

		super().print_ast(nesting)
		self._condition.print_ast(nesting + 1)
		self._body.print_ast(nesting + 1)

class DoStatementStatement (StatementExpression):

	def __init__(self, line, inputs):

		super().__init__(line)
		self._body = inputs['body']

	def print_ast(self, nesting):

		super().print_ast(nesting)
		self._body.print_ast(nesting + 1)

class ContainerPopStatement (StatementExpression):

	def __init__(self, line, inputs):

		super().__init__(line)
		self._index = inputs['index']
		self._container = inputs['container']

	def print_ast(self, nesting):

		super().print_ast(nesting)
		self._index.print_ast(nesting + 1)
		self._container.print_ast(nesting + 1)