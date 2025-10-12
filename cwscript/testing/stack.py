from cwscript.value.stack import *

def print_stack(stack):

	print(">> ", [_print_stack(item) for item in stack])

def _print_stack(item):
	if (isinstance(item, StackValue)):
		return ("Value")
	elif (isinstance(item, StackValueRequest)):
		return ("ValueReq")
	elif (isinstance(item, StackOperation)):
		return ("Op: " + item._op_class.__name__)
	elif (isinstance(item, StackBlock)):
		return ("Block")
	elif (isinstance(item, StackList)):
		return ("List")