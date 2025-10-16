from cwscript.errors import *
from cwscript.evaluator.value.base import ScriptValue

class MutableValue (ScriptValue):

	pass

class FunctionValue (MutableValue):

	def __init__(self, evaluator, parameters, body):

		# `parameters` should be a list of strings

		super().__init__(evaluator)
		self._parameters = parameters
		self._body = body

	def get_parameters(self, evaluator):

		return self._parameters

	def to_string(self, evaluator, isolated = True):

		return f"FUNC:0x{self._id:0x}"

	def get_body(self):

		return self._body

class ContainerValue (MutableValue):

	def set_field(self, evaluator, field, value):

		pass

	def get_field(self, evaluator, field):

		pass

class ListValue (ContainerValue):

	def __init__(self, evaluator, values):

		super().__init__(evaluator)
		self._values = values.copy()

	# Returns a mutable reference to the list

	def get_list(self):

		return self._values

	# `field` should be integer

	def set_field(self, evaluator, field, value):

		if not (-len(self._values) <= field < len(self._values)):
			raise CWRuntimeError("List index '%s' out of bounds" % field, evaluator.get_line())
		self._values[field] = value

	def get_field(self, evaluator, field):

		if not (-len(self._values) <= field < len(self._values)):
			raise CWRuntimeError("List index '%s' out of bounds" % field, evaluator.get_line())
		return self._values[field]

	def to_string(self, evaluator, isolated = True):

		return f"[{', '.join([value.to_string(evaluator, False) for value in self._values])}]"

	# Compare all entries using overloaded equal

	def is_equal(self, evaluator, other):

		if (not isinstance(other, ListValue)):
			return False
		if (len(self._values) != len(other._values)):
			return False
		for i in range(len(self._values)):
			if not (self._values[i].is_equal(evaluator, other._values[i])):
				return False
		return True

	def to_bool(self, evaluator):

		return len(self._values) != 0

class ObjectValue (ContainerValue):

	def __init__(self, evaluator):

		super().__init__(evaluator)
		self._values = {}

	# Returns a mutable reference to the dictionary

	def get_dict(self):

		return self._values

	# `field` should be string

	def set_field(self, evaluator, field, value):

		self._values[field] = value

	def get_field(self, evaluator, field):

		if (field not in self._values):
			raise CWRuntimeError("Invalid variable '%s'" % field, evaluator.get_line())
		return self._values[field]

	def to_string(self, evaluator, isolated = True):

		return "{%s}" % (", ".join(
			[f"{key}: {value.to_string(evaluator, False)}" for key, value in self._values.items()]
		))

	# Compare all entries using overloaded equal

	def is_equal(self, evaluator, other):

		if (not isinstance(other, ObjectValue)):
			return False
		if (self._values.keys() != other._values.keys()):
			return False
		for field in self._values:
			if not (self._values[field].is_equal(evaluator, other._values[field])):
				return False
		return True

	def to_bool(self, evaluator):

		return len(self._values) != 0