# from cwscript.value.stack import *

def print_stack(stack):

	print(">> ", [_print_stack(item) for item in stack])

def _print_stack(item):
	return ("Op: " + type(item).__name__)