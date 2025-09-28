from cwscript.value.base import ScriptValue

class NullValue (ScriptValue):

	def __init__(self, runner):

		super().__init__(runner)

	def to_string(self, isolated = True):

		return "null"