from cwscript.expression.base import ScriptExpression

# Blocks are the only "static" expression type,
# which cannot be evaluated on its own at runtime

class BlockExpression (ScriptExpression):

	def __init__(self, line, expression_list):

		super().__init__(line)
		self._expression_list = expression_list

	def run_statement(self, index):

		if (index < len(self._expression_list)):
			print("Running", self._expression_list[index])

	def size(self):

		return len(self._expression_list)