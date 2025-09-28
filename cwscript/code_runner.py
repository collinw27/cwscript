from cwscript.constants import *
from cwscript.errors import *
from cwscript.parser import code_parser
from cwscript import rules

class CodeRunner:

	def __init__(self, code):

		try:
			self._main = code_parser.parse(code)
		except CWError as error:
			error_line = error.get_line()
			if (error_line is not None):
				error.set_context(code.split('\n')[error_line])
			raise error

		self._stack = [_BlockInstance(self._main)]

	# Keep trying to run a block until an expression is found
	# This function assumes the state is correct,
	# i.e. the block on top has at least one un-executed expression

	def run_next(self):

		self._stack[-1].run_next()
		if (self._stack[-1].has_finished()):
			self._stack.pop(-1)

	def has_finished(self):

		return (not self._stack)

class _BlockInstance:

	def __init__(self, block):

		self._block = block
		self._index = 0

	def run_next(self):

		self._index += 1
		return self._block.run_statement(self._index - 1)

	def has_finished(self):

		return (self._index >= self._block.size())