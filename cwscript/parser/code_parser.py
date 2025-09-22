from cwscript.constants import *
from cwscript.errors import *
from cwscript.lexer import code_lexer
from cwscript.lexer.token import Token
from cwscript.literal import *
from cwscript import rules

def parse(code):

	# Start by splitting the code into tokens

	tokens = code_lexer.lex(code)
	_parse_block(tokens)

# Returns a BlockLiteral containing an arbitrary number of statements

def _parse_block(tokens):

	# Parse tokens statement-by-statement

	statements = []
	while (tokens):
		this_statement = []
		stack = []
		while (tokens):
			token = tokens.pop(0)
			this_statement.append(token)
			if (token.type == Token.GROUP_OPEN):
				stack.append(token.body)
			elif (token.type == Token.GROUP_CLOSE):
				if (not stack):
					raise CWParseError(f"Unbalanced closing symbol '{token.body}'")
				elif (not rules.check_group_symbols(stack[-1], token.body)):
					raise CWParseError(f"Unexpected closing symbol '{token.body}'")
				else:
					stack.pop()
			elif (token.type == Token.SEMICOLON):
				if (not stack):
					break
		if (this_statement[-1].type != Token.SEMICOLON):
			raise CWParseError("Statement does not end with semicolon")
		statements.append(_parse_group(this_statement[:-1]))

	return BlockLiteral(statements)

# Returns a DynamicLiteral to be used in a BlockLiteral,
# or as an argument in a statement

def _parse_group(tokens):

	# Step 1. Parse groups within this group

	# Process:
	# Move the start pointer through the group until an opening token is found
	# Pop the token at the start pointer, modifying the stack if it's a group token
	# Once the group is closed, parse it
	# Insert the parsed literal at the start pointer
	# Continue incrementing the start pointer as before

	group = []
	pos = 0
	stack = []
	while (pos < len(tokens)):

		token = tokens[pos]

		# Start reading group

		if (_is_token(token, Token.GROUP_OPEN)):
			stack.append(token.body)
			tokens.pop(pos)
			group.append(token)
			while (tokens[pos:]):

				token = tokens.pop(pos)
				group.append(token)

				# Monitor opening/closing groups

				if (_is_token(token, Token.GROUP_OPEN)):
					stack.append(token.body)
				elif (_is_token(token, Token.GROUP_CLOSE)):

					# Close group and push literal

					if (not rules.check_group_symbols(stack[-1], token.body)):
						raise CWParseError(f"Unexpected closing symbol '{token.body}'")
					else:
						stack.pop()
						if (not stack):
							if (group[0].body == '('):
								tokens.insert(pos, _parse_group(group[1:-1]))
							elif (group[0].body == '{'):
								tokens.insert(pos, _parse_block(group[1:-1]))
							elif (group[0].body == '['):
								tokens.insert(pos, _parse_list(group[1:-1]))
							else:
								raise RuntimeError("Invalid grouping type")
							group = []
							break

		elif (_is_token(token, Token.GROUP_CLOSE)):
			raise CWParseError(f"Unbalanced closing symbol '{token.body}'")
		pos += 1

	return ExpressionLiteral()

def _parse_list(tokens):

	return DynamicLiteral.parse("")

# Type-safe method for checking if a value is a specific token

def _is_token(value, token_type):

	return isinstance(value, Token) and value.type == token_type