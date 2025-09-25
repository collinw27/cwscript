from cwscript.constants import *
from cwscript.errors import *
from cwscript.parser import code_parser
from cwscript import rules

class CodeRunner:

	def __init__(self, code):

		try:
			self.main = code_parser.parse(code)
		except CWError as error:
			error_line = error.get_line()
			if (error_line is not None):
				error.set_context(code.split('\n')[error_line])
			raise error