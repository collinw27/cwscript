from cwscript.constants import *
from cwscript.errors import *
from cwscript import rules
from cwscript.evaluator.value import *
from cwscript.evaluator.operation import *
from cwscript.testing.stack import print_stack

class CodeEvaluator:

	def __init__(self, root):

		self._main = root

		# The evaluation stack is stored in `main_stack`
		# Instead of evaluating nested expressions like 1 * (2 + 3) with recursive
		# function calls, the operands are evaluated using a stack and sent back
		# to the original operation

		self._main_stack = [self._main.evaluate(self, ScriptValue, True)]
		self._last_value = None
		self._pending_interrupt = None
		self._error_line = 0

		# Scopes are stored separately from the stack, internally as objects

		self._scopes = [ObjectValue(self)]

	# Evaluates the next item in the evaluation stack
	# This sometimes might amount to a trivial operation, like replacing a
	# request for a number with a literal representation of that number
	# This returns false when the stack is empty, i.e. the last line has executed

	def run_next(self):

		# Store the current line of execution
		# This way, we can still trace what line caused an error even if
		# it unwinds the stack

		self._error_line = self._main_stack[-1].get_line()

		# Always operate on the topmost operation
		# It will return a ScriptValue when it's finished, and otherwise returns None
		# If the operation needs to evaluate one of its values, it signals
		# this class through request_value()
		# If the request returns a simple ScriptValue, it'll immediately be passed
		# back to the operation
		# If it relies on another operation, that will be pushed to the top of the
		# stack, and it will be passed to the original operation once it's finished

		# A note on semantics: when an immediate value is received in request_value(),
		# it's stored in the `_last_value` buffer until the next iteration
		# During the next iteration, it's passed as an argument to the topmost operation
		# The same happens when an operation returns a value
		# `_last_value` is reset ahead of evaluation to prepare for a new value

		if (self._pending_interrupt is None):
			top_op = self._main_stack[-1]
			last_value = self._last_value
			self._last_value = None
			output = top_op.evaluate_and_check(self, last_value)
			if (output is not None):
				self._last_value = output
				self._main_stack.pop()

		# If an interrupt is pending, the topmost operation is given a change to handle it
		# If it fails to, it's removed from the stack and the cycle continues
		# When an operation successfully handles an interrupt, it continues execution as normal,
		# but will not receive any value on the next evaluation
		# This is sensible, as you wouldn't expect `return` or `break` to have a return value

		else:
			top_op = self._main_stack[-1]
			self._last_value = None
			top_op.handle_interrupt(self, self._pending_interrupt)
			if (self._pending_interrupt is not None):
				self._main_stack.pop()
			if (len(self._main_stack) == 0):
				raise CWRuntimeError("Unhandled interrupt", self.get_line())

		return len(self._main_stack) > 0

	def request_value(self, node, value_type, eval_vars = True):

		value = node.evaluate(self, value_type, eval_vars)
		if (isinstance(value, ScriptValue)):
			self._last_value = value
		elif (isinstance(value, StackOperation)):
			self._main_stack.append(value)
		else:
			raise RuntimeError("Invalid request output")

	# Returns the line where execution is
	# Note that blocks have a special implementation of get_line()
	# to return the proper line when errors are raised by lone expressions
	# Also, if the stack has fully unwinded, the previous _error_line is used

	def get_line(self):

		if (len(self._main_stack) > 0):
			return self._main_stack[-1].get_line()
		else:
			return self._error_line

	def get_global_scope(self):

		return self._scopes[0]

	def get_function_scope(self):
		
		return self._scopes[-1]

	def add_function_scope(self, scope):

		self._scopes.append(scope)
		if (len(self._scopes) > MAX_RECURSION_DEPTH):
			raise CWRuntimeError("Maximum recursion depth exceeded", self.get_line())

	def pop_function_scope(self):

		self._scopes.pop()

	# Raises an interrupt to be handled on the next iteration
	# If an interrupt is already raised, this will be invalid
	# For situations where an interrupt is thrown while handling another,
	# it should only be possible for the new one to be thrown WHILE
	# handling the other, so the first should be set as handled before
	# throwing the second

	def raise_interrupt(self, interrupt):

		if (self._pending_interrupt is not None):
			raise RuntimeError("Raised interrupt before handling another")
		self._pending_interrupt = interrupt

	def handle_interrupt(self):

		self._pending_interrupt = None

	# Throws an error if an expression receives an incorrect type

	def assert_type(self, value, value_type):

		if (not isinstance(value, value_type)):
			raise CWRuntimeError("Type assertion of type %s failed for value: %s" % (
				value_type.__name__, value.to_string(self, False)), self.get_line()
			)
		return value

	# Simply used for printing an error message
	# The actual type validation should be handled by the function itself
	# (since usually, different types will require different behavior), and this
	# should be thrown in an else block at the end if a valid type wasn't matched

	def unmatched_type_error(self, value, value_types):

		raise CWRuntimeError("Type assertion of types (%s) failed for value: %s" % (
			", ".join([str(v.__name__) for v in value_types]),
			value.to_string(self, False)),
			self.get_line()
		)