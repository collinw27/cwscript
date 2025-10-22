from cwscript.errors import *

class ScriptValue:

	def __init__(self, evaluator):

		self._id = ScriptValue._new_id()

	# Casts a value to a string
	# Not every value can do this
	# `isolated` is used to give strings quotes only when
	# not being formatted within something else

	def to_string(self, evaluator, isolated = True):

		raise CWMiscError("Cannot cast to string", evaluator.get_line())

	# Returns whether two values are equal
	# When unspecified, check if they are the same object

	def is_equal(self, evaluator, other):

		return (self._id == other._id)

	# For primitive types, same as checking equality

	def is_same(self, evaluator, other):

		return self.is_equal(evaluator, other)

	# Casts a value to a boolean
	# Most non-null values return true no matter what

	def to_bool(self, evaluator):

		return True

	_id = -1

	@classmethod
	def _new_id(cls):

		cls._id += 1
		return cls._id