from cwscript.constants import *
from cwscript.errors import *
from cwscript.parser import code_parser
from cwscript.value import *
from cwscript import rules

class CodeRunner:

	def __init__(self, code):

		try:
			self._code = code
			self._main = code_parser.parse(self._code)
		except CWError as error:
			self._handle_error(error)

		self._stack = [_BlockInstance(self._main)]
		self._scopes = [ObjectValue(self)]

	# Keep trying to run a block until an expression is found
	# This function assumes the state is correct,
	# i.e. the block on top has at least one un-executed expression
	# TODO: What happens if a block's last statement pushes a new block?

	def run_next(self):

		try:
			self._stack[-1].run_next(self)
			if (self._stack[-1].has_finished()):
				self._stack.pop(-1)
		except CWError as error:
			self._handle_error(error)

	def has_finished(self):

		return (not self._stack)

	def push_block(self, block):

		self._stack.append(_BlockInstance(block))

	# Returns the line where execution is

	def get_line(self):

		return self._stack[-1].get_line()

	def get_global_scope(self):

		return self._scopes[0]

	def get_function_scope(self):
		
		return self._scopes[-1]

	# Throws an error if an expression receives an incorrect type

	def assert_type(self, value, value_type):

		if (not isinstance(value, value_type)):
			raise CWRuntimeError("Type assertion failed for %s with type %s" % (value, value_type), self.get_line())
		return value

	# A wrapper to print debug info when an error is encountered

	def _handle_error(self, error):

		error_line = error.get_line()
		if (error_line is not None):
			error.set_context(self._code.split('\n')[error_line])
		raise error

class _BlockInstance:

	def __init__(self, block):

		self._block = block
		self._index = 0

	def run_next(self, runner):

		self._block.run_expression(self._index, runner)
		self._index += 1

	def has_finished(self):

		return (self._index >= self._block.size())

	def get_line(self):

		return self._block.get_expression_line(self._index)