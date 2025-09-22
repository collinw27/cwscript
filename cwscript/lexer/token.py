
class Token:

	EXPR_ROOT = 0
	FREE_TYPE = 1
	GROUP_OPEN = 2
	GROUP_CLOSE = 3
	COMMA = 4
	SEMICOLON = 5
	PREFIX_OP = 6
	BINARY_OP = 7

	_type_str = [
		"E_ROOT",
		"FREE",
		"G_OPEN",
		"G_CLOSE",
		"COMMA",
		"SEMICOLON",
		"PREFIX_OP",
		"BINARY_OP"
	]

	def __init__(self, type_, body, line):

		self.type = type_
		self.body = body
		self._line = line

	def __repr__(self):

		return f"<{self._type_str[self.type]}: '{self.body}'>"

	def __eq__(self, other):

		return self.type == other.type and self.body == other.body

	def __ne__(self, other):

		return not self == other

	def get_line(self):

		return self._line