from cwscript.errors import *
from cwscript.value.base import ScriptValue

class NullValue (ScriptValue):

	def __init__(self, runner):

		super().__init__(runner)

	def to_string(self, runner, isolated = True):

		return "null"

	def is_equal(self, runner, other):

		return (isinstance(other, NullValue))

	def to_bool(self, runner):

		return False

# Both IntValue and FloatValue are derived from this
# Its main purpose is to allow type checking

class NumericValue (ScriptValue):

	pass

# Used to represent both integer and boolean values
# False is 0, True is anything else

class IntValue (NumericValue):

	def __init__(self, runner, value):

		super().__init__(runner)
		self._value = int(value)

	def get_value(self):

		return self._value

	def to_string(self, runner, isolated = True):

		return str(self._value)

	def is_equal(self, runner, other):

		return (isinstance(other, NumericValue) and self.get_value() == other.get_value())

	def to_bool(self, runner):

		return self._value != 0

class FloatValue (NumericValue):

	def __init__(self, runner, value):

		super().__init__(runner)
		self._value = float(value)

	def get_value(self):

		return self._value

	def to_string(self, runner, isolated = True):

		return str(self._value)

	def is_equal(self, runner, other):

		return (isinstance(other, NumericValue) and self.get_value() == other.get_value())

	# Could maybe use an epsilon here, but in general,
	# checking for float equality isn't a great idea

	def to_bool(self, runner):

		return self._value != 0

class StringValue (ScriptValue):

	def __init__(self, runner, value):

		super().__init__(runner)
		self._value = value

	def get_value(self):

		return self._value

	def to_string(self, runner, isolated = True):

		return str(self._value) if isolated else f'"{self._value}"'

	def is_equal(self, runner, other):

		return (isinstance(other, StringValue) and self.get_value() == other.get_value())

	def to_bool(self, runner):

		return len(self._value) > 0

class VariableValue (ScriptValue):

	def __init__(self, runner, parent, field):

		self._parent = parent
		self._field = field

	def set_var_value(self, runner, value):

		self._parent.set_field(runner, self._field, value)

	def get_var_value(self, runner):

		return self._parent.get_field(runner, self._field)

	def extract_parameter_name(self, runner):

		if (self._parent != runner.get_function_scope()):
			raise CWRuntimeError(f"Invalid scope for parameter: {self._field}", runner.get_line())
		if not (isinstance(self._field, str)):
			raise CWRuntimeError(f"Parameter should not be numeric: {self._field}", runner.get_line())
		return self._field

	def to_string(self, runner, isolated = True):

		return f"VAR:0x{self._id:0x}"

	# Type check is not needed when comparing IDs directly

	def is_equal(self, runner, other):

		return other._id == self._id