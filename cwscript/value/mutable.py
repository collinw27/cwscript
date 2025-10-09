from cwscript.errors import *
from cwscript.value.base import ScriptValue

class MutableValue (ScriptValue):

	pass

class FunctionValue (MutableValue):

	def __init__(self, runner, parameters, body):

		# `parameters` should be a list of strings

		super().__init__(runner)
		self._parameters = parameters
		self._body = body

	def get_parameters(self, runner):

		return self._parameters

	def to_string(self, runner, isolated = True):

		return f"FUNC:0x{self._id:0x}"

	def get_body(self):

		return self._body

class ContainerValue (MutableValue):

	def set_field(self, runner, field, value):

		pass

	def get_field(self, runner, field):

		pass

class ListValue (ContainerValue):

	def __init__(self, runner):

		super().__init__(runner)
		self._values = []

	# Returns a mutable reference to the list

	def get_list(self):

		return self._values

	# `field` should be integer

	def set_field(self, runner, field, value):

		if (len(self._values) <= field):
			raise CWRuntimeError("Invalid array index '%s'" % field)
		self._values[field] = value

	def get_field(self, runner, field):

		if (len(self._values) <= field):
			raise CWRuntimeError("Invalid array index '%s'" % field)
		return self._values[field]

	def to_string(self, runner, isolated = True):

		return f"ARR:0x{self._id:0x}"

	# Compare all entries using overloaded equal

	def is_equal(self, runner, other):

		if (not isinstance(other, ListValue)):
			return False
		if (len(self._values) != len(other._values)):
			return False
		for i in range(len(self._values)):
			if not (self._values[i].is_equal(runner, other._values[i])):
				return False
		return True

	def to_bool(self, runner):

		return len(self._values) != 0

class ObjectValue (ContainerValue):

	def __init__(self, runner):

		super().__init__(runner)
		self._values = {}

	# `field` should be string

	def set_field(self, runner, field, value):

		self._values[field] = value

	def get_field(self, runner, field):

		if (field not in self._values):
			raise CWRuntimeError("Invalid variable '%s'" % field, runner.get_line())
		return self._values[field]

	def to_string(self, runner, isolated = True):

		return f"OBJ:0x{self._id:0x}"

	# Compare all entries using overloaded equal

	def is_equal(self, runner, other):

		if (not isinstance(other, ObjectValue)):
			return False
		if (self._values.keys() != other._values.keys()):
			return False
		for field in self._values:
			if not (self._values[field].is_equal(runner, other._values[field])):
				return False
		return True

	def to_bool(self, runner):

		return len(self._values) != 0