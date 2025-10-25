from cwscript.constants import *
from cwscript.errors import *
from cwscript import rules
from cwscript.lexer.token import Token

_code = ""
_c = ""
_line = 0

def lex(code):

	global _code, _c
	_code = code
	_pop_char()
	tokens = []

	while (_c != ''):

		# Ignore whitespace

		if (_c in WHITESPACE):
			_pop_char()
			continue

		# Ignore comments

		if (_c == '#'):
			while (_c != '' and _c not in NEWLINES):
				_pop_char()
			continue

		# Lex grouping symbols (one character exactly)

		if (_c in OPENING_GROUPINGS):
			tokens.append(Token(Token.GROUP_OPEN, _c, _line))
			_pop_char()
			continue
		if (_c in CLOSING_GROUPINGS):
			tokens.append(Token(Token.GROUP_CLOSE, _c, _line))
			_pop_char()
			continue

		# Lex separators (one character exactly)

		if (_c in [',', ';']):
			tokens.append(Token(Token.SEMICOLON if _c == ';' else Token.COMMA, _c, _line))
			_pop_char()
			continue

		# Lex operators
		# Operators have a length between 1 and 3
		# The lexer keeps going until the next character no longer
		# results in a valid operation
		# Binary operators are distinguished from prefix operators
		# by whether they're followed by whitespace

		ops = [op for op in rules.get_op_strings() if op[0] == _c]
		token = ''
		if (ops):

			# Try to match a second and third character

			for i in range(2):
				token += _c
				_pop_char()
				ops = [op for op in rules.get_op_strings() if len(op) > (1 + i) and op[1+i] == _c]
				if (not ops):
					break
				elif (i == 1):
					token += _c
					_pop_char()

			# For binary operators, next character must be whitespace
			# For prefix operators, next character cannot be whitespace

			if (_c in WHITESPACE):
				if (not rules.is_binary_op(token)):
					raise CWLexError(f"Prefix operator '{token}' cannot be followed by whitespace", _line)
				tokens.append(Token(Token.BINARY_OP, token, _line))
			else:
				if (not rules.is_prefix_op(token)):
					raise CWLexError(f"Binary operator '{token}' must be surrounded by whitespace", _line)
				tokens.append(Token(Token.PREFIX_OP, token, _line))
			continue

		# For strings, continue until a closing quote is reached
		# Strings can be multiline, so line breaks will not terminate the string
		# We must ensure that a closing quote is not escaped

		if (_c in QUOTES):

			in_escape = False
			token = _c
			_pop_char()
			while (True):

				if (_c == ''):
					raise CWLexError("Unterminated string literal", _line)

				# Quote can only be closed if not in escape sequence

				if (not in_escape and _c == token[0]):
					token += _c
					_pop_char()
					break

				# Escape sequences start at \ and last exactly one character

				if (not in_escape and _c == '\\'):
					in_escape = True
				elif (in_escape):
					in_escape = False

				# Continue to next iteration

				token += _c
				_pop_char()

			tokens.append(Token(Token.FREE_TYPE, token, _line))
			continue

		# For anything else, keep it as one token
		# Even without whitespace, group symbols and separators can end a token

		token = ''
		while (_c != ''):
			if (_c in WHITESPACE or
				_c in OPENING_GROUPINGS or
				_c in CLOSING_GROUPINGS or
				_c in [',', ';']
			):
				break
			token += _c
			_pop_char()

		# Check if token matches a defined statement root
		# Exception: `else` is replaced with or operator `||`
		# They have the same behavior, but `else` looks better in some circumstances

		if (token == 'else'):
			tokens.append(Token(Token.BINARY_OP, '||', _line))
		elif (rules.is_statement(token)):
			tokens.append(Token(Token.EXPR_ROOT, token, _line))
		else:
			tokens.append(Token(Token.FREE_TYPE, token, _line))

	return tokens

def _pop_char():

	global _code, _c, _line
	old_c = _c
	_c = '' if len(_code) == 0 else _code[0]
	_code = _code[1:]
	if (_c in NEWLINES):
		_line += 1
	return old_c