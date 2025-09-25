from cwscript.literal.base import ScriptLiteral

# Blocks are the only "static" literal, which cannot be
# evaluated on its own at runtime

class BlockLiteral (ScriptLiteral):

	def __init__(self, line, expression_list):

		super().__init__(line)
		self._expression_list = expression_list

	def print_ast(self, nesting):

		super().print_ast(nesting)
		for expression in self._expression_list:
			expression.print_ast(nesting + 1)