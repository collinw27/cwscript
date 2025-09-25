from cwscript.constants import *
from cwscript.errors import *
from cwscript.lexer import code_lexer
from cwscript.lexer.token import Token
from cwscript.literal import *
from cwscript import rules

def parse(code):

	# Start by splitting the code into tokens

	tokens = code_lexer.lex(code)
	return _parse_block(tokens)

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
					raise CWParseError(f"Unbalanced closing symbol '{token.body}'", token.get_line())
				elif (not rules.check_group_symbols(stack[-1], token.body)):
					raise CWParseError(f"Unexpected closing symbol '{token.body}'", token.get_line())
				else:
					stack.pop()
			elif (token.type == Token.SEMICOLON):
				if (not stack):
					break
		if (this_statement[-1].type != Token.SEMICOLON):
			raise CWParseError("Statement does not end with semicolon", this_statement[-1].get_line())
		statements.append(_parse_group(this_statement[:-1]))

	return BlockLiteral(statements[0].get_line(), statements)

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

	pos = 0
	stack = []
	while (pos < len(tokens)):

		token = tokens[pos]

		# Start reading group

		if (_is_token(token, Token.GROUP_OPEN)):
			stack.append(token.body)
			tokens.pop(pos)
			group = [token]
			while (tokens[pos:]):

				token = tokens.pop(pos)
				group.append(token)

				# Monitor opening/closing groups

				if (_is_token(token, Token.GROUP_OPEN)):
					stack.append(token.body)
				elif (_is_token(token, Token.GROUP_CLOSE)):

					# Close group and push literal

					if (not rules.check_group_symbols(stack[-1], token.body)):
						raise CWParseError(f"Unexpected closing symbol '{token.body}'", token.get_line())
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
							break

		elif (_is_token(token, Token.GROUP_CLOSE)):
			raise CWParseError(f"Unbalanced closing symbol '{token.body}'", token.get_line())
		pos += 1

	# Next, parse expressions and prefix operators from right to left
	# Free type operands are parsed if necessary

	pos = len(tokens) - 1
	while (pos >= 0):

		token = tokens[pos]

		# Start reading expression

		if (_is_token(token, Token.EXPR_ROOT)):

			arguments = {}
			tokens.pop(pos)
			for i in range(rules.get_arg_count(token.body)):

				try:
					argument = tokens.pop(pos)
				except IndexError:
					raise CWParseError(f"Expression '{token.body}' is missing argument(s)", token.get_line())

				# Attempt to parse into one of the three literal types
				# At this point, `argument` can be a free type token, a dynamic literal, or a static literal

				arg_name, arg_type = rules.get_arg(token.body, i)
				if (arg_type == rules.ARG_DYNAMIC):
					if (_is_token(argument, Token.FREE_TYPE)):
						argument = _parse_free_type(argument)
					if (not isinstance(argument, DynamicLiteral)):
						raise CWParseError(f"Invalid dynamic literal in expression '{token.body}'", token.get_line())
					arguments[arg_name] = argument
				elif (arg_type == rules.ARG_KEYWORD):
					if (not _is_token(argument, Token.FREE_TYPE) or argument.body != arg_name):
						raise CWParseError(f"Expected keyword '{arg_name}' in expression '{token.body}'", token.get_line())
				else:
					if (not isinstance(argument, BlockLiteral)):
						raise CWParseError(f"Invalid block in expression '{token.body}'", token.get_line())
					arguments[arg_name] = argument

			expression_class = rules.get_expression_class(token.body)
			tokens.insert(pos, expression_class(token.get_line(), arguments))

		# Group prefix operator with successive operand

		elif (_is_token(token, Token.PREFIX_OP)):
			operator = token
			tokens.pop(pos)
			try:
				operand = tokens.pop(pos)
			except IndexError:
				raise CWParseError(f"Prefix operator '{token.body}' is missing operand", token.get_line())
			if (_is_token(operand, Token.FREE_TYPE)):
				operand = _parse_free_type(operand)
			if (not isinstance(operand, DynamicLiteral)):
				raise CWParseError(f"Invalid dynamic literal for operator '{token.body}'", token.get_line())
			operator_class = rules.get_prefix_op_class(token.body)
			tokens.insert(pos, operator_class(token.get_line(), {'operand': operand}))

		pos -= 1

	# Parse binary operators
	# Done group-by-group, starting with highest precedence
	# Must take associativity into account when choosing direction to iterate

	for op_group in rules.get_op_groups():
		l_to_r, current_ops = op_group
		pos = 0 if l_to_r else (len(tokens) - 1)
		while ((pos < len(tokens)) if l_to_r else (pos >= 0)):

			token = tokens[pos]

			# Group operator with surrounding operands

			if (_is_token(token, Token.BINARY_OP) and token.body in current_ops):
				try:
					operand_2 = tokens.pop(pos + 1)
					tokens.pop(pos)
					operand_1 = tokens.pop(pos - 1)
				except IndexError:
					raise CWParseError(f"Binary operator '{token.body}' is missing operand(s)", token.get_line())
				if (_is_token(operand_1, Token.FREE_TYPE)):
					operand_1 = _parse_free_type(operand_1)
				if (_is_token(operand_2, Token.FREE_TYPE)):
					operand_2 = _parse_free_type(operand_2)
				if not (isinstance(operand_1, DynamicLiteral) and isinstance(operand_2, DynamicLiteral)):
					raise CWParseError(f"Invalid dynamic literal for operator '{token.body}'", token.get_line())
				operator_class = rules.get_binary_op_class(token.body)
				tokens.insert(pos, operator_class(token.get_line(), {'operand_1': operand_1, 'operand_2': operand_2}))

			pos += 1 if l_to_r else -1

	# Free types should've been parsed along with their
	# respective operators/expressions
	# The other possiblity is this group contained a single free type by itself
	# In this case, parse the free type
	# At this point, we should only have 1 remaining element, the tree root

	if (len(tokens) == 0):
		raise CWParseError("Empty group", None)
	elif (len(tokens) >= 2):
		raise CWParseError("Could not resolve group operation", tokens[0].get_line())
	if (_is_token(tokens[0], Token.FREE_TYPE)):
		tokens[0] = _parse_free_type(tokens[0])

	return tokens[0]

def _parse_list(tokens):

	return ListLiteral(tokens[0].get_line(), [])

def _parse_free_type(token):

	return DynamicLiteral.parse(token.get_line(), token.body)

# Type-safe method for checking if a value is a specific token

def _is_token(value, token_type):

	return isinstance(value, Token) and value.type == token_type