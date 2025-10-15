from cwscript.constants import *
from cwscript.errors import *
from cwscript import rules
from cwscript.parser import code_parser
from cwscript.evaluator.code_evaluator import *

# Runs the evaluator and keeps track of basic debug info

class Program:

	def __init__(self, code, debug):

		try:
			self._code = code
			self._debug = debug
			self._exit_code = 0
			self._evaluator = CodeEvaluator(code_parser.parse(self._code))
		except CWError as error:
			self._handle_error(error)

	def run_next(self):

		if (self._exit_code == 1):
			return False
		try:
			return self._evaluator.run_next()
		except CWError as error:
			self._handle_error(error)

	# A CWException will only propogate past here if in debug mode
	# After an exception is handled, no more code will be run,
	# signaled by setting exit code to != 0

	def _handle_error(self, error):

		error_line = error.get_line()
		if (error_line is not None):
			error.set_context(self._code.split('\n')[error_line])
		self._exit_code = 1
		if (self._debug):
			raise error
		else:
			print(error.str())

	def get_exit_code(self):

		return self._exit_code