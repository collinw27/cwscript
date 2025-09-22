from cwscript.literal._base import ScriptLiteral

class BlockLiteral (ScriptLiteral):

	def __init__(self, line, expression_list):

		super().__init__(line)
		self._expression_list = expression_list

	@staticmethod
	def parse(line, string):

		pass