from cwscript.expression.base import ScriptExpression

# Blocks are the only "static" expression type,
# which cannot be evaluated on its own at runtime

class BlockExpression (ScriptExpression):

	def __init__(self, line, expression_list):

		super().__init__(line)
		self._expression_list = expression_list