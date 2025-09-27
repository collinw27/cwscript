
# Base class for expressions (objects composing an AST)
# The parser converts Tokens into ScriptExpressions

class ScriptExpression:

	def __init__(self, line):

		self._line = line

	def get_line(self):

		return self._line