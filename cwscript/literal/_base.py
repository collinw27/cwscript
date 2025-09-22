
# Base class for literals (objects composing an AST)
# The parser converts Tokens into ScriptLiterals

class ScriptLiteral:

	def __init__(self, line):

		self._line = line

	def get_line(self):

		return self._line