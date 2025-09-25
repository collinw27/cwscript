from cwscript.literal.expression.base import *

class PrintExpression (ExpressionLiteral):

	def __init__(self, line, inputs):

		super().__init__(line)
		self._value = inputs['value']

	def print_ast(self, nesting):

		super().print_ast(nesting)
		self._value.print_ast(nesting + 1)

class MaxExpression (ExpressionLiteral):

	def __init__(self, line, inputs):

		super().__init__(line)
		self._value_1 = inputs['value_1']
		self._value_2 = inputs['value_2']

	def print_ast(self, nesting):

		super().print_ast(nesting)
		self._value_1.print_ast(nesting + 1)
		self._value_2.print_ast(nesting + 1)

class IfStatementExpression (ExpressionLiteral):

	def __init__(self, line, inputs):

		super().__init__(line)
		self._condition = inputs['condition']
		self._body = inputs['body']

	def print_ast(self, nesting):

		super().print_ast(nesting)
		self._condition.print_ast(nesting + 1)
		self._body.print_ast(nesting + 1)

class DoStatementExpression (ExpressionLiteral):

	def __init__(self, line, inputs):

		super().__init__(line)
		self._body = inputs['body']

	def print_ast(self, nesting):

		super().print_ast(nesting)
		self._body.print_ast(nesting + 1)

class ContainerPopExpression (ExpressionLiteral):

	def __init__(self, line, inputs):

		super().__init__(line)
		self._index = inputs['index']
		self._container = inputs['container']

	def print_ast(self, nesting):

		super().print_ast(nesting)
		self._index.print_ast(nesting + 1)
		self._container.print_ast(nesting + 1)