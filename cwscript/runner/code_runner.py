from cwscript.constants import *
from cwscript.errors import *
from cwscript import rules
from cwscript.parser import code_parser
from cwscript.value import *
from cwscript.expression import *
from cwscript.testing.stack import print_stack

# In this project, 'runner' is used synonymously with 'evaluator'

class CodeRunner:

	def __init__(self, code):

		try:
			self._code = code
			self._main = DoStatement(0, {'body': code_parser.parse(self._code)})
		except CWError as error:
			self._handle_error(error)

		# The evaluation stack is stored in `main_stack`
		# Instead of evaluating nested expressions like 1 * (2 + 3) with recursive
		# function calls, the operands are evaluated using a stack and sent back
		# to the original operation as a static method call
		# Ex. This stack would be [* 4 + 2 3] -> [* 4 5] -> [20]
		# Note that arithmetic operations are used as an example, but any expression
		# type is valid as a stack operation (especially function calls!)
		# Since lists and blocks support an arbitrary number of elements, they
		# use their own special types

		# Note that the entire program is implemented as a DoStatement operation

		self._main_stack = [StackValueRequest(self._main, ScriptValue)]

		# Scopes are stored separately from the stack, internally as dictionary objects

		self._scopes = [ObjectValue(self)]

	# Evaluates the next item in the evaluation stack
	# This sometimes might amount to a trivial operation, like replacing a
	# request for a number with a literal representation of that number
	# This returns false when the stack is empty, i.e. the last line has executed

	def run_next(self):

		try:

			# Move downward from top of stack
			# Evaluate the first item we can (i.e. anything that's not a value)
			# Afterwards, break and wait for next function call
			# Slight caveat: Values are reversed when receiving from get_stack(),
			# and reversed again when sent back to evaluate()
			# This allows their order to be correct from the expression's point of view,
			# but also allows values with precedence to be placed at the top of the stack

			for i, item in reversed(list(enumerate(self._main_stack))):

				# Block: Insert next expression afterwards, remove when empty
				# The value above the block from the previous instruction is removed first
				# Blocks are removed automatically since expressions can create them an
				# arbitrary number of times, and they therefore don't contribute to
				# the argument count

				if (isinstance(item, StackBlock)):
					if (item.has_started()):
						self._main_stack.pop(i + 1)
					next_expression = item.pop_next()
					if (next_expression is None):
						self._main_stack.pop(i)
					else:
						self._main_stack.insert(i + 1, StackValueRequest(next_expression, ScriptValue))
					break

				# List: Consolidate values on top of it into the list

				elif (isinstance(item, StackList)):
					list_values = [a.value for a in reversed(self._main_stack[i + 1 : i + 1 + item.num_items])]
					new_list = item.evaluate(self, list_values)
					self._main_stack[i : i + 1 + item.num_items] = [new_list]
					break

				# Value request: Evaluate, either resulting in a single value
				# or another operation

				elif (isinstance(item, StackValueRequest)):
					self._main_stack.pop(i)
					if (i == len(self._main_stack)):
						self._main_stack += list(reversed(item.evaluate(self)))
					else:
						self._main_stack[i:i] = list(reversed(item.evaluate(self)))
					break

				# Operation: Evaluate using values above it in stack
				# Caveat: If an InterruptableOperation is interrupted, is will return
				# the block it's being interrupted with
				# This should be pushed to the stack instead of removing the operation

				elif (isinstance(item, StackOperation)):
					args = [a.value for a in reversed(self._main_stack[i + 1 : i + 1 + item.num_args])]
					value = item.evaluate(self, args)
					if (isinstance(value, StackBlock)):
						self._main_stack.insert(i + 1, value)
					else:
						self._main_stack[i : i + 1 + item.num_args] = [value]
					break

				# Value: Keep propagating downward

			# When finished, stack should just be the return value of `do`

			return len(self._main_stack) > 1

		except CWError as error:
			self._handle_error(error)

	# Returns the line where execution is
	# Propogates downward until a valid stack item is found

	def get_line(self):

		for item in reversed(self._main_stack):
			if (isinstance(item, StackOperation)):
				return item.get_line()
		return None

	def get_global_scope(self):

		return self._scopes[0]

	def get_function_scope(self):
		
		return self._scopes[-1]

	def add_function_scope(self, scope):

		self._scopes.append(scope)

	def pop_function_scope(self):

		self._scopes.pop()

	# Throws an error if an expression receives an incorrect type

	def assert_type(self, value, value_type):

		if (not isinstance(value, value_type)):
			raise CWRuntimeError("Type assertion of type %s failed for value %s" % (value_type.__name__, value.to_string(self, False)), self.get_line())
		return value

	# A wrapper to print debug info when an error is encountered

	def _handle_error(self, error):

		error_line = error.get_line()
		if (error_line is not None):
			error.set_context(self._code.split('\n')[error_line])
		raise error