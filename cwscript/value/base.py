from cwscript.errors import *

class ScriptValue:

	def __init__(self, runner):

		self._id = ScriptValue._new_id()

	# Casts a value to a string
	# Not every value can do this
	# `isolated` is used to give strings quotes only when
	# not being formatted within something else

	def to_string(self, runner, isolated = True):

		raise CWMiscError("Cannot cast to string", runner.get_line())

	# Returns whether two values are equal

	def is_equal(self, runner, other):

		raise NotImplementedError()

	# Casts a value to a boolean
	# Most non-null values return true no matter what

	def to_bool(self, runner):

		return True

	_id = -1

	@classmethod
	def _new_id(cls):

		cls._id += 1
		return cls._id