from cwscript.constants import *
from cwscript.errors import *
from cwscript.evaluator.operation import *

class ASTNode:

	TYPE_BLOCK = 0
	TYPE_NULL = 1
	TYPE_BOOL = 2
	TYPE_INT = 3
	TYPE_FLOAT = 4
	TYPE_STRING = 5
	TYPE_VARIABLE = 6
	TYPE_LIST = 7
	TYPE_OTHER = 8

	def __init__(self, line):

		self._line = line

	def get_line(self):

		return self._line

	def evaluate(self, evaluator, value_type, eval_vars):

		raise NotImplementedError()

	# See implementation in ASTValue

	def eval_as_parameters(self, evaluator):

		raise CWRuntimeError("Invalid parameter list", self.get_line())

	# Special method for using variable name for catch body

	def eval_as_variable(self, evaluator):

		raise CWRuntimeError("Invalid parameter name", self.get_line())

# Corresponds to basic types whose evaluation method can easily
# be stored in an if-else statement
# In terms of actual evaluation method, there's technically no clear line
# between this class and ASTOperation, since some values from here also
# must return an operation

class ASTValue (ASTNode):

	def __init__(self, line, dtype, value):

		super().__init__(line)
		self._dtype = dtype
		self._value = value

	# Allows negating a numeric value directly instead of applying a negation operation
	# Negating a bool converts it to an int

	def try_negate(self):

		if (self._dtype == ASTNode.TYPE_BOOL):
			self._dtype = ASTNode.TYPE_INT
			self._value = -1 if self._value else 0
			return True
		elif (self._dtype in [ASTNode.TYPE_INT, ASTNode.TYPE_FLOAT]):
			self._value = -self._value
			return True
		return False

	# Special method for using list literal as parameter list
	# Error if wrong type

	def eval_as_parameters(self, evaluator):

		if (self._dtype != ASTNode.TYPE_LIST):
			raise CWRuntimeError("Invalid parameter list", self.get_line())
		output = [node.eval_as_variable(evaluator) for node in self._value]
		if (len(set(output)) != len(output)):
			raise CWRuntimeError("Duplicate function parameter", self.get_line())
		return output

	# Special method for using variable name for catch body

	def eval_as_variable(self, evaluator):

		if (self._dtype != ASTNode.TYPE_VARIABLE):
			raise CWRuntimeError("Invalid parameter name", self.get_line())
		is_global, var_names = self._value
		if (is_global or len(var_names) > 1):
			raise CWRuntimeError("Invalid parameter name", self.get_line())
		return var_names[0]

	def evaluate(self, evaluator, value_type, eval_vars):

		if (self._dtype == self.TYPE_BLOCK):
			return StackBlock(self._value, self._line, value_type, eval_vars)
		elif (self._dtype == self.TYPE_NULL):
			return evaluator.assert_type(NullValue(evaluator), value_type)
		elif (self._dtype == self.TYPE_NULL):
			return evaluator.assert_type(BoolValue(evaluator, self._value), value_type)
		elif (self._dtype == self.TYPE_BOOL):
			return evaluator.assert_type(BoolValue(evaluator, self._value), value_type)
		elif (self._dtype == self.TYPE_INT):
			return evaluator.assert_type(IntValue(evaluator, self._value), value_type)
		elif (self._dtype == self.TYPE_FLOAT):
			return evaluator.assert_type(FloatValue(evaluator, self._value), value_type)
		elif (self._dtype == self.TYPE_STRING):
			return evaluator.assert_type(StringValue(evaluator, self._value), value_type)
		elif (self._dtype == self.TYPE_VARIABLE):

			# Format is self._value = [is_global, values]

			if (self._value[0]):
				parent = evaluator.get_global_scope()
			else:
				parent = evaluator.get_function_scope()
			var_value = VariableValue(evaluator, parent, self._value[1])
			if (eval_vars):
				return evaluator.assert_type(var_value.get_var_value(evaluator), value_type)
			else:
				return evaluator.assert_type(var_value, value_type)
				
		elif (self._dtype == self.TYPE_LIST):
			return StackList(self._value, self._line, value_type, eval_vars)
		elif (self._dtype == self.TYPE_OTHER):
			raise RuntimeError("Invalid ASTValue type")

	@staticmethod
	def parse(line, string):

		# This shouldn't be possible, but it's worth checking just in case

		if (len(string) == 0):
			raise CWParseError(f"Empty expression", line)

		# Search for type using process of elimination

		if (string == "null"):
			return ASTValue(line, ASTNode.TYPE_NULL, None)
		elif (string in BOOLS):
			return ASTValue.parse_bool(line, string)
		elif (string[0] == string[-1] and string[0] in QUOTES):
			return ASTValue.parse_string(line, string)
		elif (string[0] == "." or string[:7] == "global."):
			return ASTValue.parse_variable(line, string)
		elif (string[0] in '1234567890-'):
			if ('.' in string):
				return ASTValue.parse_float(line, string)
			else:
				return ASTValue.parse_int(line, string)
		else:
			raise CWParseError(f"Unable to parse expression '{string}'", line)

	@staticmethod
	def parse_bool(line, string):

		if (string not in BOOLS):
			raise CWParseError(f"Invalid bool '{string}'", line)
		return ASTValue(line, ASTNode.TYPE_BOOL, string[0] == "t")

	@staticmethod
	def parse_int(line, string):

		# Must be an (optional) negative followed by numeric digits
		# Avoided just using python's `int()` method by itself since it allows
		# other characters _ that would be inconsistent with the specification

		if (len(string) == 0):
			raise CWParseError(f"Empty integer", line)
		elif (string[0] not in '1234567890-'):
			raise CWParseError(f"Unexpected character in integer '{string}'", line)
		elif (len([c for c in string[1:] if c not in '1234567890']) > 0):
			raise CWParseError(f"Unexpected character in integer '{string}'", line)

		is_negative = (string[0] == '-')
		if (is_negative):
			if (len(string) == 1):
				raise CWParseError(f"Integer '{string}' missing numeric part", line)
			string = string[1:]
		return ASTValue(line, ASTNode.TYPE_INT, int(string) * (-1 if is_negative else 1))

	@staticmethod
	def parse_float(line, string):

		# Similar to `IntExpression.parse()`, but allows for a single decimal point
		# This method technically accepts floats without a decimal point, although
		# the parser should always resolve that to an integer
		# TODO: Accept scientific notation

		if (len(string) == 0):
			raise CWParseError(f"Empty float", line)
		elif (string[0] not in '1234567890-'):
			raise CWParseError(f"Unexpected character in float '{string}'", line)
		is_negative = (string[0] == '-')
		old_string = string
		if (is_negative):
			if (len(string) == 1):
				raise CWParseError(f"Float '{string}' missing numeric part", line)
			string = string[1:]

		# Do remaning checks now that negative is dealt with
		# One decimal point is allowed, but not at beginning or end

		if (len([c for c in string if c not in '1234567890.']) > 0):
			raise CWParseError(f"Unexpected character in float '{old_string}'", line)
		elif (string.count('.') > 1):
			raise CWParseError(f"Duplicate decimal in float '{old_string}'", line)
		elif (string[0] == '.' or string[-1] == '.'):
			raise CWParseError(f"Decimal cannot begin or end float, '{old_string}'", line)

		return ASTValue(line, ASTNode.TYPE_FLOAT, float(string) * (-1 if is_negative else 1))

	@staticmethod
	def parse_string(line, string):

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
		return ASTValue(line, ASTNode.TYPE_STRING, value)

	@staticmethod
	def parse_variable(line, string):

		if not (len(string) > 0 and (string[0] == '.' or string[:7] == 'global.')):
			raise CWParseError(f"Invalid variable '{string}'", line)
		is_global = (string[:7] == 'global.')

		# Split into strings at each . delimiter
		# Cannot have two adjacent .

		values = (string[7:] if is_global else string[1:]).split('.')
		for value in values:
			if (not value or len([c for c in value if c not in VAR_ALLOWED]) > 0):
				raise CWParseError(f"Invalid variable '{string}'", line)
		return ASTValue(line, ASTNode.TYPE_VARIABLE, [is_global, values])

class ASTOperation (ASTNode):

	def __init__(self, line, operation, args):

		super().__init__(line)
		self._operation = operation
		self._args = args
		self._dtype = ASTNode.TYPE_OTHER

	def evaluate(self, evaluator, value_type, eval_vars):

		return self._operation(self._args, self._line, value_type, eval_vars)