from cwscript.constants import *
from cwscript.errors import *
from cwscript import rules
from cwscript.parser import code_parser
from cwscript.evaluator.code_evaluator import *

# Pretty much just a wrapper for the evaluator

class Program:

	def __init__(self, code):

		try:
			self._code = code
			self._evaluator = CodeEvaluator(code_parser.parse(self._code))
		except CWError as error:
			self._handle_error(error)

	def run_next(self):

		try:
			return self._evaluator.run_next()
		except CWError as error:
			self._handle_error(error)

	def _handle_error(self, error):

		error_line = error.get_line()
		if (error_line is not None):
			error.set_context(self._code.split('\n')[error_line])
		raise error