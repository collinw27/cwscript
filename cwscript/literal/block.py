from cwscript.literal._base import ScriptLiteral

class BlockLiteral (ScriptLiteral):

	def __init__(self, expression_list):

		super()
		self._expression_list = expression_list

	@staticmethod
	def parse(string):

		pass