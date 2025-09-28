from cwscript.errors import *

class ScriptValue:

	def __init__(self, runner):

		self._id = ScriptValue._new_id()
		self._runner = runner

	# Casts a value to a string
	# Not every value can do this
	# `isolated` is used to give strings quotes only when
	# not being formatted within something else

	def to_string(self, isolated = True):

		raise CWMiscError("Cannot cast to string", self._runner.get_line())

	_id = -1

	@classmethod
	def _new_id(cls):

		cls._id += 1
		return cls._id