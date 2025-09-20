from cwscript.constants import *
from cwscript.lexer import code_lexer
from cwscript.lexer.token import Token
from cwscript import rules

def parse(code):

	# Start by splitting the code into tokens

	tokens = code_lexer.lex(code)
	print(tokens)