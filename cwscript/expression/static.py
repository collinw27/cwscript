from cwscript.expression.base import ScriptExpression
from cwscript.value import *

# Blocks are the only "static" expression type,
# which cannot be evaluated on its own at runtime

class BlockExpression (ScriptExpression):

	def __init__(self, line, expression_list):

		super().__init__(line)
		self._expression_list = expression_list

	# Returns None if out of bounds

	def get_expression(self, index):

		return self._expression_list[index] if index < len(self._expression_list) else None