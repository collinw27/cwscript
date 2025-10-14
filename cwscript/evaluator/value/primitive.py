from cwscript.errors import *
from cwscript.evaluator.value.base import ScriptValue

class NullValue (ScriptValue):

	def __init__(self, evaluator):

		super().__init__(evaluator)

	def to_string(self, evaluator, isolated = True):

		return "null"

	def is_equal(self, evaluator, other):

		return (isinstance(other, NullValue))

	def to_bool(self, evaluator):

		return False

# Both IntValue and FloatValue are derived from this
# Its main purpose is to allow type checking

class NumericValue (ScriptValue):

	pass

# As a NumericValue, bools can be used as if they were 1 or 0
# in numeric expressions

class BoolValue (NumericValue):

	def __init__(self, evaluator, value):

		super().__init__(evaluator)
		self._value = bool(value)

	def get_value(self):

		return int(self._value)

	def to_string(self, evaluator, isolated = True):

		return "true" if self._value else "false"

	def is_equal(self, evaluator, other):

		return (isinstance(other, NumericValue) and self.get_value() == other.get_value())

	def to_bool(self, evaluator):

		return self._value

class IntValue (NumericValue):

	def __init__(self, evaluator, value):

		super().__init__(evaluator)
		self._value = int(value)

	def get_value(self):

		return self._value

	def to_string(self, evaluator, isolated = True):

		return str(self._value)

	def is_equal(self, evaluator, other):

		return (isinstance(other, NumericValue) and self.get_value() == other.get_value())

	def to_bool(self, evaluator):

		return self._value != 0

class FloatValue (NumericValue):

	def __init__(self, evaluator, value):

		super().__init__(evaluator)
		self._value = float(value)

	def get_value(self):

		return self._value

	def to_string(self, evaluator, isolated = True):

		return str(self._value)

	def is_equal(self, evaluator, other):

		return (isinstance(other, NumericValue) and self.get_value() == other.get_value())

	# Could maybe use an epsilon here, but in general,
	# checking for float equality isn't a great idea

	def to_bool(self, evaluator):

		return self._value != 0

class StringValue (ScriptValue):

	def __init__(self, evaluator, value):

		super().__init__(evaluator)
		self._value = value

	def get_value(self):

		return self._value

	def to_string(self, evaluator, isolated = True):

		return str(self._value) if isolated else f'"{self._value}"'

	def is_equal(self, evaluator, other):

		return (isinstance(other, StringValue) and self.get_value() == other.get_value())

	def to_bool(self, evaluator):

		return len(self._value) > 0

class VariableValue (ScriptValue):

	def __init__(self, evaluator, parent, field):

		self._parent = parent
		self._field = field

	def set_var_value(self, evaluator, value):

		self._parent.set_field(evaluator, self._field, value)

	def get_var_value(self, evaluator):

		return self._parent.get_field(evaluator, self._field)

	def extract_parameter_name(self, evaluator):

		if (self._parent != evaluator.get_function_scope()):
			raise CWRuntimeError(f"Invalid scope for parameter: {self._field}", evaluator.get_line())
		if not (isinstance(self._field, str)):
			raise CWRuntimeError(f"Parameter should not be numeric: {self._field}", evaluator.get_line())
		return self._field

	def to_string(self, evaluator, isolated = True):

		return f"VAR:0x{self._id:0x}"

	# Type check is not needed when comparing IDs directly

	def is_equal(self, evaluator, other):

		return other._id == self._id