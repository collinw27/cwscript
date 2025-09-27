from cwscript.constants import *
from cwscript.errors import *
from cwscript.expression.base import ScriptExpression

# A "dynamic expression" is any code object that can be evaluated at runtime

class DynamicExpression (ScriptExpression):

	# Converts a compile-time ScriptExpression into a runtime-useable ScriptValue

	def evaluate(self, value_type, eval_vars = True):

		pass

	# Resolve an unknown type to a specific dynamic expression class
	# The class' parse() methods are responsible for validating input,
	# as the checks in this function are only able to rule out certain types

	@staticmethod
	def parse(line, string):

		# This shouldn't be possible, but it's worth checking just in case

		if (len(string) == 0):
			raise CWParseError(f"Empty expression", line)

		# Search for type using process of elimination

		if (string == "null"):
			return NullExpression.parse(line, string)
		elif (string in BOOLS):
			return BoolExpression.parse(line, string)
		elif (string[0] == string[-1] and string[0] in QUOTES):
			return StringExpression.parse(line, string)
		elif (string[0] == "." or string[:7] == "global."):
			return VariableExpression.parse(line, string)
		elif (string[0] in '1234567890-'):
			if ('.' in string):
				return FloatExpression.parse(line, string)
			else:
				return IntExpression.parse(line, string)
		else:
			raise CWParseError(f"Unable to parse expression '{string}'", line)

class NullExpression (DynamicExpression):

	def __init__(self, line):

		super().__init__(line)

	@staticmethod
	def parse(line, string):

		return NullExpression(line)

class BoolExpression (DynamicExpression):

	def __init__(self, line, value):

		super().__init__(line)
		self._value = assert_type(value, bool)

	@staticmethod
	def parse(line, string):

		if (string not in BOOLS):
			raise CWParseError(f"Invalid bool '{string}'", line)
		return BoolExpression(line, string == "true")

class IntExpression (DynamicExpression):

	def __init__(self, line, value):

		super().__init__(line)
		self._value = value

	@staticmethod
	def parse(line, string):

		# Must be an (optional) negative followed by numeric digits
		# Avoided just using python's `int()` method by itself since it allows
		# other characters _ that would be inconsistent with the specification

		if (len(string) == 0):
			raise MCRParseError(f"Empty integer", line)
		elif (string[0] not in '1234567890-'):
			raise MCRParseError(f"Unexpected character in integer '{string}'", line)
		elif (len([c for c in string[1:] if c not in '1234567890']) > 0):
			raise MCRParseError(f"Unexpected character in integer '{string}'", line)

		is_negative = (string[0] == '-')
		if (is_negative):
			if (len(string) == 1):
				raise MCRParseError(f"Integer '{string}' missing numeric part", line)
			string = string[1:]
		return IntExpression(line, int(string) * (-1 if is_negative else 1))

class FloatExpression (DynamicExpression):

	def __init__(self, line, value):

		super().__init__(line)
		self._value = value

	@staticmethod
	def parse(line, string):

		# Similar to `IntExpression.parse()`, but allows for a single decimal point
		# This method technically accepts floats without a decimal point, although
		# the parser should always resolve that to an integer
		# TODO: Accept scientific notation

		if (len(string) == 0):
			raise MCRParseError(f"Empty float", line)
		elif (string[0] not in '1234567890-'):
			raise MCRParseError(f"Unexpected character in float '{string}'", line)
		is_negative = (string[0] == '-')
		if (is_negative):
			if (len(string) == 1):
				raise MCRParseError(f"Float '{string}' missing numeric part", line)
			old_string = string
			string = string[1:]

		# Do remaning checks now that negative is dealt with
		# One decimal point is allowed, but not at beginning or end

		if ([c for c in string if c not in '1234567890.'] > 0):
			raise MCRParseError(f"Unexpected character in float '{old_string}'", line)
		elif (string.count('.') > 1):
			raise MCRParseError(f"Duplicate decimal in float '{old_string}'", line)
		elif (string[0] or string[-1]):
			raise MCRParseError(f"Decimal cannot begin or end float, '{old_string}'", line)

		return FloatExpression(line, float(string) * (-1 if is_negative else 1))

class StringExpression (DynamicExpression):

	def __init__(self, line, value):

		super().__init__(line)
		self._value = value

	@staticmethod
	def parse(line, string):

		if not (string[0] == string[-1] and string[0] in QUOTES and len(string) >= 2):
			raise CWParseError(f"Invalid string ' {string} '", line)
		value = ""
		escaped = False
		for c in string[1:-1]:
			if (not escaped and c == '\\'):
				escaped = True
			elif (escaped):
				if (c in ['\\', "'", "\""]):
					value += c
				elif (c == 'n'):
					value += '\n'
				elif (c == 't'):
					value += '\t'
				elif (c == 'r'):
					value += '\r'
				else:
					raise CWParseError(f"Invalid escape in string {string}", line)
				escaped = False
			else:
				value += c
		return StringExpression(value, line)

class VariableExpression (DynamicExpression):

	# Will need to be updated to include scope information

	def __init__(self, line, value):

		super().__init__(line)
		self._value = value

	@staticmethod
	def parse(line, string):

		if not (len(string) > 0 and (string[0] == '.' or string[:7] == 'global.')):
			raise CWParseError(f"Invalid variable '{string}'", line)
		return VariableExpression(line, string)

# List expressions do not perform any parsing on their own
# They rely on the parsed values from the parser

class ListExpression (DynamicExpression):

	def __init__(self, line, values):

		super().__init__(line)
		self._values = values