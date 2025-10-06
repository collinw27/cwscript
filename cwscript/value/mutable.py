from cwscript.errors import *
from cwscript.value.base import ScriptValue

class MutableValue (ScriptValue):

	pass

class ContainerValue (MutableValue):

	def set_field(self, runner, field, value):

		pass

	def get_field(self, runner, field):

		pass

class ObjectValue (ContainerValue):

	def __init__(self, runner):

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

		if (self._values.keys() != other._values.keys()):
			return False
		for field in self._values:
			if not (self._values[field].is_equal(runner, other._values[field])):
				return False
		return True

	def to_bool(self, runner):

		return len(self._values) != 0