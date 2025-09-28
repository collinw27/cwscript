from cwscript.expression.base import ScriptExpression

# Blocks are the only "static" expression type,
# which cannot be evaluated on its own at runtime

class BlockExpression (ScriptExpression):

	def __init__(self, line, expression_list):

		super().__init__(line)
		self._expression_list = expression_list

	def run_expression(self, index, runner):

		if (index < len(self._expression_list)):
			print("Running", self._expression_list[index])
			self._expression_list[index].evaluate(runner, None)

	def get_expression_line(self, index):

		return self._expression_list[index].get_line()

	def size(self):

		return len(self._expression_list)