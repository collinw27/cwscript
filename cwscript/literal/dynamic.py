from cwscript import rules
from cwscript.literal._base import ScriptLiteral

class DynamicLiteral (ScriptLiteral):

	# Converts a compile-time ScriptLiteral into a runtime-useable ScriptValue

	def evaluate(self, value_type, eval_vars = True):

		pass

	@staticmethod
	def parse(line, string):

		return StringLiteral(line, string)

# For now, parse everything into a string literal
# This allows testing the parser without needing to
# define every possible datatype

class StringLiteral (DynamicLiteral):

	def __init__(self, line, value):

		super().__init__(line)
		self.value = value