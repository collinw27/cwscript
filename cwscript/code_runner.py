from cwscript.constants import *
from cwscript.parser import code_parser
from cwscript import rules

class CodeRunner:

	def __init__(self, code):

		code_parser.parse(code)