
class Token:

	EXPR_ROOT = 0
	EXPR_KEYWORD = 1
	FREE_TYPE = 2
	GROUP_OPEN = 3
	GROUP_CLOSE = 4
	COMMA = 5
	SEMICOLON = 6
	PREFIX_OP = 7
	BINARY_OP = 8

	_type_str = [
		"E_ROOT",
		"E_KWORD",
		"FREE",
		"G_OPEN",
		"G_CLOSE",
		"COMMA",
		"SEMICOLON",
		"PREFIX_OP",
		"BINARY_OP"
	]

	def __init__(self, type_, body):

		self.type = type_
		self.body = body

	def __repr__(self):

		return f"<{self._type_str[self.type]}> \"{self.body}\""